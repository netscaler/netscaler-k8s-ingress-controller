import subprocess
import os
import json
import paramiko
import time
import sys

#-------------------------------------------------------------------------------------------#
#                                       FUNCTIONS                                           #
#-------------------------------------------------------------------------------------------#
def usage():
    print '''
Usage:
======
    Execution using CURL:
    ---------------------
        curl -k -s <URL to this script> | python - <options>
        Example:
        curl -k https://code.citrite.net/users/raghulc/repos/cpx-gcp/raw/deployment/first-tier-vpx/vpx-lb-tier-deployment.py | \\
            python - --project=test-project,--zone=asia-southeast1-a,--cluster_name=cpx-cluster-1,\\
            --image=test-vpx-image,--vpx_name=vpx-frontend-ingress,\\
            --public_subnet=public-subnet,--public_ip=10.10.0.10,--public_alias=10.10.0.11,\\
            --private_subnet=default,--private_ip=10.148.0.201,--private_alias=10.148.0.202

    Execution using python directly:
    --------------------------------
        Example:
        python <script> <options>
        python vpx-lb-tier-deployment.py --project=test-project,--zone=asia-southeast1-a,--cluster_name=cpx-cluster-1
'''

def execute_gcloud_command(cmd):
    out = subprocess.check_output(cmd,shell=True)

    j = json.loads(out)
    return(j)

def connect_ns(ip, user, passwd):
    ns = paramiko.SSHClient()
    ns.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection_success=False

    for i in range(1,10):
        try:
            ns.connect(ip, username=user, password=passwd, look_for_keys=False)
            if ns.get_transport() is not None and ns.get_transport().is_active():
                connection_success=True
        except:
            print("NetScaler is still booting up. Waiting to reconnect...")
            time.sleep(10)

        if (connection_success):
            break;
    return(ns)

def exec_ns_cmd(obj,cmd,timeout=30):
    (cmdin, cmdout, cmderr) = obj.exec_command(cmd,timeout=timeout) 
    out = cmdout.read()
    return(out)

def which_gcloud():
    gcloud=subprocess.check_output(['which','gcloud'])
    gcloud=gcloud.rstrip()
    return(gcloud)

def cidr_to_netmask(cidr):
  cidr = int(cidr)
  mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
  return (str( (0xff000000 & mask) >> 24)   + '.' +
          str( (0x00ff0000 & mask) >> 16)   + '.' +
          str( (0x0000ff00 & mask) >> 8)    + '.' +
          str( (0x000000ff & mask)))

def vpx(var):
  
    #parse variables from dictionary 
    project=var['project']
    image=var['image']
    vpx_name=var['vpx_name']
    vpx_size=var['vpx_size']
    zone=var['zone']
    public_subnet=var['public_subnet']
    public_ip=var['public_ip']
    public_alias=var['public_alias']
    private_subnet=var['private_subnet']
    private_ip=var['private_ip']
    private_alias=var['private_alias']
    vpx_user=var['vpx_user']
    vpx_pass=var['vpx_pass']
    cluster_name=var['cluster_name']

    cmd = "gcloud compute --project="+project+" instances create "+vpx_name+ \
    " --zone="+zone+" --machine-type="+vpx_size+ \
    " --network-interface subnet="+private_subnet+",private-network-ip="+private_ip+ \
    ",address='',aliases="+private_alias+ \
    " --network-interface subnet="+public_subnet+",private-network-ip="+public_ip+",address='',aliases="+public_alias+ \
    " --image="+image+" --image-project="+project+" --boot-disk-size=20GB --format=json --quiet"

    out = execute_gcloud_command(cmd)
    print ("*********************************************************************************************************")
    if ((out[0]['name'] == vpx_name) and (out[0]['status'] == 'RUNNING')):
        print ("VPX: "+vpx_name+" is created successfully")
    else:
        print ("VPX: "+vpx_name+" is creation FAILED")
    print ("*********************************************************************************************************")

    #Parse VPX related Values from output JSON
    vpx_mgmt = out[0]['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    vpx_private_snip = out[0]['networkInterfaces'][0]['aliasIpRanges'][0]['ipCidrRange'].rsplit('/')[0]

    vpx_traffic_public = out[0]['networkInterfaces'][1]['accessConfigs'][0]['natIP']
    vpx_public_snip = out[0]['networkInterfaces'][1]['aliasIpRanges'][0]['ipCidrRange'].rsplit('/')[0]

    time.sleep(100)
    print ("*********************************************************************************************************")
    print ("Connecting to NetScaler")
    print ("*********************************************************************************************************")
    ns = connect_ns(vpx_mgmt, vpx_user, vpx_pass)

    print ("*********************************************************************************************************")
    if (ns):
        print ("Connection to NetScaler was successfull");
    else:
        print ("Connection to NetScaler FAILED");
        exit()
    print ("*********************************************************************************************************")


    print ("*********************************************************************************************************")
    print ("SANITY CONFIGS")
    out = exec_ns_cmd(ns,"clear config -f full")
    time.sleep(2)
    out = exec_ns_cmd(ns,"add ns ip "+vpx_private_snip+" 255.255.255.0")
    out = exec_ns_cmd(ns,"add ns ip "+vpx_public_snip+" 255.255.255.0")
    out = exec_ns_cmd(ns,"enable ns mode MBF")
    out = exec_ns_cmd(ns,"save config")
    time.sleep(2)
    print ("*********************************************************************************************************")

    
    print ("*********************************************************************************************************")
    print ("Parsing GKE Cluster details")
    print ("*********************************************************************************************************")

    cmd = "gcloud container --project="+project+" clusters describe "+cluster_name+" --format=json --zone="+zone
    out = execute_gcloud_command(cmd)
    (pod_net, pod_prefix) = out['clusterIpv4Cidr'].rsplit('/')
    pod_netmask = cidr_to_netmask(pod_prefix)
    cluster_node_count = out['currentNodeCount']
    cluster_node_regex = out['instanceGroupUrls'][0].rsplit('/')[-1].rsplit('-grp')[0]

    cmd = "gcloud compute --project="+project+" instances list --zones "+zone+" --filter=\"name~"+cluster_node_regex+"\" --format=json"
    out = execute_gcloud_command(cmd)

    if (str(len(out)) == str(cluster_node_count)):
        print ("There are "+str(cluster_node_count)+"nodes in Cluster: "+cluster_name)
    else:
        print ("ERROR: Cluster nodes do not match")

    nodes_ip = dict()
    for i in range(len(out)):
        nodes_ip[out[i]['name']] = out[i]['networkInterfaces'][0]['networkIP']

    print ("*********************************************************************************************************")
    print ("Configuring Routes in VPX for POD Network via Cluster nodes") 
    print ("*********************************************************************************************************")
  
    for key, value in nodes_ip.items(): 
        print ("Adding route for node: "+key)
        out = exec_ns_cmd(ns,"add route "+pod_net+" "+pod_netmask+" "+value)

    print ("*********************************************************************************************************")
    print ("                                        CONFIGURATIONS DONE                                              ")
    print ("*********************************************************************************************************")

    print ("The App can now be accessed using the IP: "+vpx_traffic_public+" with the Host Header citrix-ingress.com")
    print ("Curl command:")
    print ("curl http://"+vpx_traffic_public+"/ -H 'Host: citrix-ingress.com")

#-------------------------------------------------------------------------------------------#
#                                       MAIN SCRIPT                                         #
#-------------------------------------------------------------------------------------------#

#Parse Command line arguments to over-ride defaults
args=sys.argv[1:]

args_dict = {}

try:
    #Remove args that does not start with "--"
    for x in args:
        if (x.find('help') != -1 or x.find('usage') != -1):
            usage()
            exit()

        if (x[0:2] != "--"):
            args.remove(x)

    args = ''.join(args) #now args is a string
    args = args.split(',') #now a cleaned up list
    for x in args:
        x=x.split('=')
        args_dict[x[0][2:]] = x[1]

except SystemExit:
    exit()

except:
    pass

default_vars = {'project':'test-project',
                'image':'test-vpx-image',
                'vpx_name':'vpx-frontend-ingress',
                'vpx_size':'n1-standard-4',
                'zone':'asia-southeast1-a',
                'public_subnet':'public-subnet',
                'public_ip':'10.10.0.10',
                'public_alias':'10.10.0.11',
                'private_subnet':'default',
                'private_ip':'10.148.0.201',
                'private_alias':'10.148.0.202',
                'vpx_user':'nsroot',
                'vpx_pass':'nsroot',
                'cluster_name':'cpx-cluster-1'}

#Decide to go with defaults or user-specified
parsed_vars={}
for key in default_vars.keys():
    if key in args_dict:
        parsed_vars[key] = args_dict[key]
    else:
        parsed_vars[key] = default_vars[key]

vpx(parsed_vars)
