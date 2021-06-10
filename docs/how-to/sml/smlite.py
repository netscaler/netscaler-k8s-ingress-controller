#!/usr/bin/python3

'''
This scipt convert application YAMLs into set of YAMLs that can be deployed in Service Mesh lite architecture 
where east-west communication happens via Citrix ADC CPX running with Citrix Ingress Controller as sidecar.
SML yaml for services of an applcation which are already running inside Kubernetes cluster can also be generated using this script.
'''

import sys
import os
import re
import oyaml as yaml
import manifestCreator
import logging
import warnings
import argparse
import subprocess
from ipaddress import ip_address, IPv4Address
from collections import OrderedDict
from kubernetes import client, config
from itertools import chain, repeat
from pathlib import Path

__author__ = "Priyanka"
__version__ = "1.2.0"
__maintainer__ = "Priyanka"
__email__ = "priyanka.sharma@citrix.com"

'''
Initialising logging framework
'''
logger = logging.getLogger('SMLITE')
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


warnings.filterwarnings('ignore', message='Unverified HTTPS request')

ports_used = []
cpx_count = 1
cpx_ingress_class = "tier-2-cpx"
vpx_ingress_class = "tier-1-vpx"
tier1_ingress_name = "tier1-vpx-ingress"
frontend_cpx_count = 1
chart_name = "sml"
output_yaml = "smlite-all-in-one.yaml"


def main():

    global cpx_count
    global output_yaml

    parser = argparse.ArgumentParser(description='Taking service yamls or name as input. And namespace in case service names is provided')
    parser.add_argument('ServiceList', action="store",help='Please provide comma seperated list of service yamls or names to convert into SML')
    parser.add_argument('Namespace', action="store",nargs='?', help='Please provide namespace in which services are deployed')
    svcs = parser.parse_args().ServiceList.split(',')
    namespace = parser.parse_args().Namespace

    converted_yamls_dict_list = []

    if(".yaml" not in svcs[0]):
        '''
        Code for connecting to Kubenetes Cluster
        '''
        if not namespace:
            logger.error("Please provide namespace as well in which services are deployed while starting the script")
            sys.exit(0)
        prompts = chain(["Do you want to connect to a Remote Kubernetes Cluster? (Y/N): "], repeat("Invaild input. Please respond with (Y/N): "))
        remote_access = validate_input(prompts,"yesORno")
        if remote_access.lower() == 'n':
            prompts = chain(['Do you want to use default kubeconfig file present at "/root/.kube/config"? (Y/N): '], repeat("Invaild input. Please respond with (Y/N): "))
            default_kube_config = validate_input(prompts,"yesORno")
            if default_kube_config.lower() == "y":
                kube_config_path = "/root/.kube/config"
            else:
                prompts = chain(["Please provide path of kubeconfig file: "], repeat("This path doesn't exist! Please provide a valid kubeconfig file path: "))
                kube_config_path = validate_input(prompts,"path")
            config.load_kube_config(config_file=kube_config_path)
            v1 = client.CoreV1Api()
        elif remote_access.lower() == 'y':
            prompts = chain(["Do you want to use Bearer Token for connecting to a Remote Kubernetes Cluster? (Y/N): "], repeat("Invaild input. Please respond with (Y/N): "))
            use_bearer_token = validate_input(prompts,"yesORno")
            if use_bearer_token.lower() == "y":
                configuration = client.Configuration()
                bearer_token = input("Please provide bearer token key of SA having permission to access given service: ")
                configuration.api_key = {"authorization": "Bearer " + bearer_token}
                prompts = chain(["Please provide API server <IP:PORT>: "], repeat("Invaild input. Please provide valid IP and port in format <IP:PORT>: "))
                api_server = validate_input(prompts,"apiServerIPPort")
                configuration.host = 'https://'+api_server
                configuration.verify_ssl = False
                v1 = client.CoreV1Api(client.ApiClient(configuration))
            elif use_bearer_token.lower() == "n":
                prompts = chain(["Please provide path of kubeconfig file: "], repeat("This path doesn't exist! Please provide a valid kubeconfig file path: "))
                kube_config_path = validate_input(prompts,"path")
                config.load_kube_config(config_file=kube_config_path)
                v1 = client.CoreV1Api()

    app_frontend_svc_name = input("Please provide name of the service exposed to tier-1: ")
    app_hostname = input("Please provide hostname for exposing \""+ app_frontend_svc_name +"\" service: ")

    if not namespace:
        namespace = "default"


    '''
    Coverting YAMLs to SML YAMLs
    '''
    for svc in svcs:
        if(".yaml" in svc):
            '''
            When applcation YAMLs is provided as input.
            '''
            with open(svc, 'r') as stream:
                try:
                    yaml_dictionaries = yaml.safe_load_all(stream)
                    for yaml_instance in yaml_dictionaries:
                        if yaml_instance:
                            converted_yamls_dict_list.extend(convert_yaml_to_sml(yaml_instance,app_frontend_svc_name,app_hostname))
                except Exception as e:
                    logger.error("Retrieving yaml from service yamls provided failed with error: {}" .format(e))
                    sys.exit("Please ensure service yaml is in proper format")
        else:
            '''
            When service name running in Kubernetes cluster is provided as input.
            '''
            try:
                service = v1.read_namespaced_service(svc,namespace)
            except Exception as e:
                logger.error("Retrieving service from KubeAPI server failed with error: {}" .format(e))
                sys.exit("Please ensure service name and namespace is correct")
            service = service.__dict__
            service = convert_kube_object_to_dict(service)
#           service = OrderedDict([('apiVersion',service['apiVersion']),
#                            ('kind',service['kind']),
#                            ('metadata',service['metadata']),
#                            ('spec',service['spec']),
            converted_yamls_dict_list.extend(convert_yaml_to_sml(service,app_frontend_svc_name,app_hostname))


    '''
    Checking if required HELM is there or not.
    '''
    helm_ver = subprocess.run(["helm version"],shell=True,capture_output=True).stdout.decode('utf-8')
    matchObj = re.search(r'Version:"v3.*', helm_ver, re.M|re.I)
    if not matchObj:
        logger.error("Couldn't find Helm with version 3.x and above.")
        sys.exit("Please install Helm 3.x and put it in the PATH. This https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md can be followed for the same.")

    subprocess.run(["helm repo add citrix https://citrix.github.io/citrix-helm-charts/"],shell=True,capture_output=True)
    

    '''
    Getting ADM details
    '''
    prompts = chain(['Citrix ADM required? (Y/N): '], repeat("Invaild input. Please respond with (Y/N): "))
    adm_required = validate_input(prompts,"yesORno")
    if adm_required.lower() == "y":
        prompts = chain(['Please provide IP of ADM Agent(svcIP of container agent) for Citrix ADC CPX: '], repeat("Invaild IP. Please enter and IPv4 IP: "))
        cpx_adm_agent_ip = validate_input(prompts,"ip")
        adm_secret = input("Please provide name of K8s Secret created using ADM Agent credentials. Press ENTER for 'admlogin': ")
        if not adm_secret:
            adm_secret = "admlogin"


    '''
    Adding CPX yamls
    '''
    for i in range(1,cpx_count+1):
        if adm_required.lower() == "y":
            output = subprocess.run(["helm template "+ chart_name + str(i) + " citrix/citrix-cloud-native --set cpx.enabled=true,cpx.license.accept=yes,cpx.ingressClass[0]="+cpx_ingress_class+str(i)+",cpx.coeConfig.required=true,cpx.coeConfig.timeseries.metrics.enable=true,cpx.coeConfig.distributedTracing.enable=true,cpx.coeConfig.endpoint.server="+ cpx_adm_agent_ip +",cpx.ADMSettings.ADMIP=" + cpx_adm_agent_ip +",cpx.ADMSettings.loginSecret=" + adm_secret + " -n "+namespace+" > temp.yaml"],shell=True,capture_output=True)
#            output = subprocess.run(["helm template "+ chart_name + str(i) + " citrix/citrix-cloud-native --set cpx.enabled=true,cpx.license.accept=yes,cpx.ingressClass[0]="+cpx_ingress_class+str(i)+",cpx.coeConfig.required=true,cpx.coeConfig.timeseries.metrics.enable=true,cpx.coeConfig.distributedTracing.enable=true,cpx.coeConfig.endpoint.server="+ cpx_adm_agent_ip +",cpx.ADMSettings.ADMIP=" + cpx_adm_agent_ip +",cpx.ADMSettings.loginSecret=" + adm_secret + " -n "+namespace+" > temp.yaml"],shell=True,capture_output=True)
            if output.stderr:
                logger.error("Helm chart command failed with error {}" .format(output.stderr))
                sys.exit("Please ensure you have provided proper inputs.")
        else:
            output = subprocess.run(["helm template "+ chart_name + str(i) + " citrix/citrix-cloud-native --set cpx.enabled=true,cpx.license.accept=yes,cpx.ingressClass[0]="+cpx_ingress_class+str(i)+ " -n "+namespace+" > temp.yaml"],shell=True,capture_output=True)
            if output.stderr:
                logger.error("Helm chart command failed with error {}" .format(output.stderr))
                sys.exit("Please ensure you have provided proper inputs.")
        
        with open('temp.yaml', 'r') as stream:
            yaml_dictionaries = list(yaml.safe_load_all(stream))
        if i > 1:
            list_to_remove = []
            for yaml_instance in yaml_dictionaries:
                if yaml_instance['kind'] == "ServiceAccount" or yaml_instance['kind'] == "ClusterRole" or yaml_instance['kind'] == "ClusterRoleBinding":
                    list_to_remove.append(yaml_instance)
                elif yaml_instance['kind'] == "Deployment":
                    yaml_instance['spec']['template']['spec']['serviceAccountName'] = re.sub("sml"+str(i),"sml1",yaml_instance['spec']['template']['spec']['serviceAccountName'])
            yaml_dictionaries = [x for x in yaml_dictionaries if x not in list_to_remove]
            converted_yamls_dict_list.extend(yaml_dictionaries)
        else:
            converted_yamls_dict_list.extend(yaml_dictionaries)

#    rbac = manifestCreator.rbac()
#    rbac = rbac.createRbac()
#    converted_yamls_dict_list.extend(rbac)
#        cpx_cic_yaml = manifestCreator.cpxCic({"name":chart_name+str(i),"ingressClass":cpx_ingress_class+str(i)})
#        cpx_cic_yaml = cpx_cic_yaml.create()
#        converted_yamls_dict_list.extend(cpx_cic_yaml)

    '''
    Getting details for Tier-1 ADC
    '''
    prompts = chain(['Citrix Ingress Controller for tier-1 ADC required? (Y/N): '], repeat("Invaild input. Please respond with (Y/N): "))
    create_cic = validate_input(prompts,"yesORno")
    if create_cic.lower() == "y":
        prompts = chain(['Please provide tier-1 ADC NSIP: '], repeat("Invaild IP. Please enter and IPv4 IP: "))
        ns_ip = validate_input(prompts,"ip")
        prompts = chain(['Please provide tier-1 ADC VIP: '], repeat("Invaild IP. Please enter and IPv4 IP: "))
        ns_vip = validate_input(prompts,"ip")
        ns_secret = input("Please provide name of K8s Secret created using ADC credentials. Press ENTER for 'nslogin': ")
        if not ns_secret:
            ns_secret = "nslogin"
        if adm_required.lower() == "y":
            prompts = chain(['Please provide IP of ADM Agent(podIP of container agent) for Citrix ADC VPX/MPX: '], repeat("Invaild IP. Please enter and IPv4 IP: "))
            vpx_adm_agent_ip = validate_input(prompts,"ip")

        app_frontend_svc_port = input("Please provide port used to expose CPX service to Tier-1 ADC: ")
        prompts = chain(["Please provide protocol used to expose CPX service to Tier-1 ADC (tcp/udp/http/https/grpc): "], repeat("Invaild protocol. Please choose a protocol from (tcp/udp/http/https/grpc): "))
        app_frontend_svc_protocol = validate_input(prompts,"protocol")

        if app_frontend_svc_protocol == "grpc":
            app_frontend_svc_protocol = "tcp"

        if app_frontend_svc_protocol == "https":
            tls = input("Please give secret-name for TLS certificate for \""+ app_frontend_svc_name +"\" svc: ")
        else:
            tls = ""


        if adm_required.lower() == "y":
            output = subprocess.run(["helm template "+ chart_name + " citrix/citrix-cloud-native --set cic.enabled=true,cic.nsIP="+ ns_ip +",cic.nsVIP="+ ns_vip +",cic.license.accept=yes,cic.adcCredentialSecret="+ ns_secret +",cic.ingressClass[0]="+vpx_ingress_class+",cic.coeConfig.required=true,cic.coeConfig.timeseries.metrics.enable=true,cic.coeConfig.timeseries.port=5563,cic.coeConfig.distributedTracing.enable=true,cic.coeConfig.transactions.enable=true,cic.coeConfig.transactions.port=5557,cic.coeConfig.endpoint.server="+ vpx_adm_agent_ip +" -n "+ namespace +" > temp.yaml"],shell=True,capture_output=True)
            if output.stderr:
                logger.error("Helm chart command failed with error {}" .format(output.stderr))
                sys.exit("Please ensure you have provided proper inputs.")

            ingress_yaml = manifestCreator.ingress({"name":tier1_ingress_name,"protocol":app_frontend_svc_protocol.lower(),
                                                    "ingressClass":vpx_ingress_class,"tls":tls,"admRequired":True,
                                                    "serviceDetails":{app_hostname:[{"serviceName":"sml"+str(frontend_cpx_count)+"-cpx-service",
                                                                                     "servicePort":app_frontend_svc_port}]}})
        else:
            output = subprocess.run(["helm template "+ chart_name + " citrix/citrix-cloud-native --set cic.enabled=true,cic.nsIP="+ ns_ip +",cic.nsVIP="+ ns_vip +",cic.license.accept=yes,cic.adcCredentialSecret="+ ns_secret +",cic.ingressClass[0]="+vpx_ingress_class+" -n "+ namespace +" > temp.yaml"],shell=True,capture_output=True)
            if output.stderr:
                logger.error("Helm chart command failed with error {}" .format(output.stderr))
                sys.exit("Please ensure you have provided proper inputs.")

            ingress_yaml = manifestCreator.ingress({"name":tier1_ingress_name,"protocol":app_frontend_svc_protocol.lower(),
                                                    "ingressClass":vpx_ingress_class,"tls":tls,
                                                    "serviceDetails":{app_hostname:[{"serviceName":"sml"+str(frontend_cpx_count)+"-cpx-service",
                                                                                     "servicePort":app_frontend_svc_port}]}})
        with open('temp.yaml', 'r') as stream:
            yaml_dictionaries = list(yaml.safe_load_all(stream))
        converted_yamls_dict_list.extend(yaml_dictionaries)

        ingress_yaml = ingress_yaml.create()
        converted_yamls_dict_list.append(ingress_yaml)

    '''
    Deleting temp.yaml which got created via Helm
    '''
    my_file = Path("temp.yaml")
    if my_file.is_file():
        os.remove("temp.yaml")
    
    '''
    Writing dictionay of YAML into a .yaml file
    '''
    write_dictionaries_into_yaml(converted_yamls_dict_list,output_yaml)


def validate_input(prompts, input_type, port_list=None):

    protocols = {'tcp','udp','http','https','grpc'}
    options = {'y','n'}
    replies = map(input, prompts)
    replies = map(str.strip, replies)
    if input_type != "path":
        replies = map(str.lower, replies)
    if input_type == "yesORno":
        valid_response = next(filter(options.__contains__, replies))
    elif input_type == "protocol":
        valid_response = next(filter(protocols.__contains__, replies))
    elif input_type == "path":
        paths = map(Path, replies)
        valid_response = next(filter(Path.exists, paths))
        valid_response = str(valid_response)
    elif input_type == "port":
        replies = map(int, replies)
        valid_response = next(filter(port_list.__contains__, replies))
    elif input_type == "apiServerIPPort":
        ip_port_re = re.compile(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$')
        valid_response = next(filter(ip_port_re.match, replies))
    elif input_type == "ip":
        replies = map(str, replies)
        def check_ip(ip):
            try:
                return True if type(ip_address(ip)) is IPv4Address else False
            except ValueError:
                return False 
        valid_response = next(filter(check_ip, replies))
        valid_response = str(valid_response)
    return valid_response

'''
Pre Process dictionary of application yaml for converting those into SML yaml dictionary
''' 
def convert_yaml_to_sml(yaml_dict,app_frontend_svc_name,app_hostname):
    entries_to_remove = {'metadata' : ['creationTimestamp','namespace','resourceVersion','selfLink','uid','clusterName','generation',
                                       'generateName','deletionTimestamp','ownerReferences'],
                         'spec'    :  ['publishNotReadyAddresses','sessionAffinityConfig','loadBalancerSourceRanges',
                                       'loadBalancerIp','healthCheckNodePort','externalTrafficPolicy','externalIPs','clusterIp',
                                       'sessionAffinity','type', {'ports': ports_scan}],
                         'status': []}

    yaml_dict = remove_empty_entries(yaml_dict)
    yaml_dict = remove_unwanted_entries(yaml_dict,entries_to_remove)
    yaml_dict = create_smlite_yamls(yaml_dict,app_frontend_svc_name,app_hostname)
    return yaml_dict

'''
Take dictionary of application yaml in input, converts those into SML yaml dictionary
'''
def create_smlite_yamls(yaml_instance,frontend,hostname):

    global ports_used
    global cpx_count
    global cpx_ingress_class
    global chart_name
    global frontend_cpx_count
    headless_svc_tag = "-headless"
    ew_ing_tag = "-ingress"
    ns_ing_tag = "-ns-ingress"
    request_other_namespace = ".svc.cluster.local"
    restricted_ports = [9080,9443,3010,5555,8080]
    protocols_supported = ['tcp','udp','http','https','grpc']

    list_of_sml_yamls = []
    
    if yaml_instance["kind"] == "Service":
        service_name = yaml_instance["metadata"]["name"]

        prompts = chain(["Please enter protocol to be used for service \""+ service_name + "\" (tcp/udp/http/https/grpc): "], repeat("Invaild protocol. Please choose a protocol from (tcp/udp/http/https/grpc): "))
        protocol = validate_input(prompts,"protocol")

        ports = yaml_instance["spec"]["ports"]
        if len(ports) > 1:
            port_list = []
            for p in ports:
                port_list.append(p["port"])
            prompts = chain(["Found multiple ports in the service \""+ service_name + "\". Please enter port to be used "+ str(port_list)[1:-1] + ": "], repeat("Invaild port. Please provide a valid port to be used from "+ str(port_list)[1:-1] + ": "))
            service_port = validate_input(prompts,"port",port_list)
            port_details = ports[port_list.index(service_port)]
        else:
            port_details =  yaml_instance["spec"]["ports"][0]

        if port_details["port"] in restricted_ports:
            logger.error("Microservice "+ service_name +" using CPX restricted port "+ str(port_details["port"]) +". So, can't be converted into SML YAMLs")
            sys.exit(0)

        if (protocol.lower() == "tcp" or protocol.lower() == "udp" or protocol.lower() == "grpc") and port_details["port"] in ports_used:
            cpx_count = cpx_count+1

        if protocol == "grpc":
            protocol = "tcp"

        if protocol == "https":
            tls = input("Please give secret-name for TLS certificate: ")
        else:
            tls = ""

        '''
        Creating Headless Service pointing to appication deployment 
        '''
        yaml_instance["metadata"]["name"] = service_name+headless_svc_tag
        yaml_instance["spec"]["clusterIP"] = "None"

        list_of_sml_yamls.append(yaml_instance)

        '''
        Creating service for appication so that FQDN of the microservice points to Citrix ADC CPX IP address
        '''
        service_yaml = manifestCreator.service({"name":service_name,"appLabel":chart_name+str(cpx_count)+"-cpx","ports":ports})
        service_yaml = service_yaml.create()
        list_of_sml_yamls.append(service_yaml)

        '''
        Creating ingress for each microservice so they get configured in CPX
        '''
        if (protocol.lower() == "tcp" or protocol.lower() == "udp"):
#            if "targetPort" in port_details:
#                ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
#                                                    "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
#                                                    "serviceDetails":{"serviceName":service_name+headless_svc_tag,
#                                                                      "servicePort":  port_details["targetPort"]}})
#            else:
            ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
                                                    "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
                                                    "serviceDetails":{"serviceName":service_name+headless_svc_tag,
                                                                      "servicePort":  port_details["port"]}})
            if frontend == service_name:
                frontend_ingress_yaml = manifestCreator.ingress({"name":service_name+ns_ing_tag,"protocol":protocol.lower(),
                                                                 "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
                                                                 "serviceDetails":{"serviceName":service_name+headless_svc_tag,
                                                                                   "servicePort": port_details["port"]}})

        else:
#            if "targetPort" in port_details:
#                ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
#                                                    "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
#                                                    "serviceDetails":{service_name:[{"serviceName":service_name+headless_svc_tag,
#                                                                                     "servicePort":port_details["targetPort"]}]}})
#            else:
            ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
                                                    "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
                                                    "serviceDetails":{service_name:[{"serviceName":service_name+headless_svc_tag,
                                                                                     "servicePort":port_details["port"]}]}})
#                                                                      service_name+"."+namespace+request_other_namespace:[{
#                                                                                     "serviceName":service_name+headless_svc_tag,
#                                                                                     "servicePort":port_details["port"]}]}})
            if frontend == service_name:
                frontend_cpx_count = str(cpx_count)
                frontend_ingress_yaml = manifestCreator.ingress({"name":service_name+ns_ing_tag,"protocol":protocol.lower(),
                                                                 "ingressClass":cpx_ingress_class+str(cpx_count),"tls":tls,
                                                                 "serviceDetails":{hostname:[{"serviceName":service_name+headless_svc_tag,
                                                                                              "servicePort":port_details["port"]}]}})

        ingress_yaml = ingress_yaml.create()
        list_of_sml_yamls.append(ingress_yaml)
        if frontend == service_name: 
            ingress_yaml = frontend_ingress_yaml.create()
            list_of_sml_yamls.append(ingress_yaml)
        if (protocol.lower() == "tcp" or protocol.lower() == "udp"):
            ports_used.append(port_details["port"])

    '''
    Keeping Deployment YAML as it is.
    '''
    if yaml_instance["kind"] == "Deployment":
        list_of_sml_yamls.append(yaml_instance)

    return list_of_sml_yamls

'''
Removes NULL or empty entries form the application YAML
'''
def remove_empty_entries(dictionary):
    if not isinstance(dictionary,dict) and not isinstance(dictionary,OrderedDict):
        return
    try:
        for i in dictionary.copy():
            if isinstance(dictionary[i], dict):
                dictionary[i] = remove_empty_entries(dictionary[i])
                if not dictionary[i]:
                    del dictionary[i]
            elif isinstance(dictionary[i], list):
                for list_intance in dictionary[i]:
                    remove_empty_entries(list_intance)
                if all(not d for d in dictionary[i]):
                    del dictionary[i]
            else:
                if dictionary[i] is None or dictionary[i] == 'None':
                    del dictionary[i]
        return dictionary
    except Exception as e:
        logger.info(e)

'''
Removes extra entries form the application YAML which gets added 
after yaml is deployed in the cluster
'''
def remove_unwanted_entries(service,entries_to_remove):
    for e in entries_to_remove.keys():
        if e in service:
            if isinstance(entries_to_remove[e], list):
                if entries_to_remove[e]:
                    for list_instance in entries_to_remove[e]:
                        if isinstance(list_instance, dict):
                            for key in list_instance:
                                if key in service[e]:
                                    service[e] = list_instance[key](service[e])
                        else:
                            if list_instance in service[e]:
                                del service[e][list_instance]
                else:
                    del service[e]
    return service

def ports_scan(ports_dict):
    if "ports" in ports_dict:
        for port_instance in ports_dict["ports"]:
            if 'nodePort' in port_instance:
                del port_instance['nodePort']
    return ports_dict

def capitalize(match):
    return match.group(1).upper()

'''
Converts kube Object returned from Kube API server into dictionary
'''
def convert_kube_object_to_dict(dictionary):
    dictionary = {re.sub("^_", "", x): v for x, v in dictionary.items()}
    dictionary = {re.sub('\_(.)', capitalize , x): v for x, v in dictionary.items()}
    if isinstance(dictionary, dict):
        for key in dictionary:
            try:
                dictionary[key] = convert_kube_object_to_dict(dictionary[key].__dict__)
            except:
                if isinstance(dictionary[key], list):
                    new_list = []
                    for list_instance in dictionary[key]:
                        try:
                            list_instance = convert_kube_object_to_dict(list_instance.__dict__)
                            list_instance = {re.sub("^_", "", x): v for x, v in list_instance.items()}
                            list_instance = {re.sub('\_(.)', capitalize , x): v for x, v in list_instance.items()}
                            new_list.append(list_instance)
                        except:
                            new_list.append(list_instance)
                    dictionary[key] = new_list
    return dictionary

'''
Writes dictionay of YAML into a .yaml file
'''
def write_dictionaries_into_yaml(yaml_dict,output_file):
    yaml.add_representer(QuotedString, quoted_scalar)
    if(yaml_dict):
        with open(output_file, 'w') as stream_write:
            for y in yaml_dict:
                if y["kind"] == "Ingress":
                    if y["metadata"]["annotations"] is not None:
                        for k,v in y["metadata"]["annotations"].items():
                            if k == "ingress.citrix.com/secure-backend":
                                continue
                            y["metadata"]["annotations"][k] = QuotedString(v)
            stream_write.write(yaml.dump_all(yaml_dict, default_flow_style=False, sort_keys=False))
            logger.info("Please note Tier-1 ADC VPX ingress "+tier1_ingress_name+" is created with basic config. Please edit it as per your requirements")
            logger.info("ServiceMesh Lite YAMLs are created and is present in \"smlite-all-in-one.yaml\" file.")

class QuotedString(str):  # just subclass the built-in str
    pass

def quoted_scalar(dumper, data):  # a representer to force quotations on scalars
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

if __name__== "__main__":
  main()
