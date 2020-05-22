#!/usr/bin/python3

'''
This scipt convert application YAMLs into set of YAMLs that can be deployed in Service Mesh lite architecture 
where east-west communication happens via Citrix ADC CPX running with Citrix Ingress Controller as sidecar.
SML yaml for services of an applcation which are already running inside Kubernetes cluster can also be generated using this script.
'''

import sys
import re
import oyaml as yaml
import manifestCreator
import logging
import warnings
import argparse
from collections import OrderedDict
from kubernetes import client, config
from itertools import chain, repeat
from pathlib import Path

__author__ = "Priyanka"
__version__ = "1.1.0"
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
ingress_class = "tier-2-cpx"
cpx_ingress_name = "cpx-ingress"
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
    
    for svc in svcs:
        if(".yaml" in svc):
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
    Adding CPX yamls
    '''
    rbac = manifestCreator.rbac()
    rbac = rbac.createRbac()
    converted_yamls_dict_list.extend(rbac)
    for i in range(1,cpx_count+1):
        cpx_cic_yaml = manifestCreator.cpxCic({"name":cpx_ingress_name+str(i),"ingressClass":ingress_class+str(i)})
        cpx_cic_yaml = cpx_cic_yaml.create()
        converted_yamls_dict_list.extend(cpx_cic_yaml)

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
    global ingress_class
    global cpx_ingress_name
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
        service_yaml = manifestCreator.service({"name":service_name,"appLabel":cpx_ingress_name+str(cpx_count),"ports":ports})
        service_yaml = service_yaml.create()
        list_of_sml_yamls.append(service_yaml)

        '''
        Creating ingress for each microservice so they get configured in CPX
        '''
        if (protocol.lower() == "tcp" or protocol.lower() == "udp"):
            ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
                                                    "ingressClass":ingress_class+str(cpx_count),"tls":tls,
                                                    "serviceDetails":{"serviceName":service_name+headless_svc_tag,
                                                                      "servicePort":  port_details["port"]}})
            if frontend == service_name:
                frontend_ingress_yaml = manifestCreator.ingress({"name":service_name+ns_ing_tag,"protocol":protocol.lower(),
                                                                 "ingressClass":ingress_class+str(cpx_count),"tls":tls,
                                                                 "serviceDetails":{"serviceName":service_name+headless_svc_tag,
                                                                                   "servicePort": port_details["port"]}})

        else:
            ingress_yaml = manifestCreator.ingress({"name":service_name+ew_ing_tag,"protocol":protocol.lower(),
                                                    "ingressClass":ingress_class+str(cpx_count),"tls":tls,
                                                    "serviceDetails":{service_name:[{"serviceName":service_name+headless_svc_tag,
                                                                                     "servicePort":port_details["port"]}]}})
#                                                                      service_name+"."+namespace+request_other_namespace:[{
#                                                                                     "serviceName":service_name+headless_svc_tag,
#                                                                                     "servicePort":port_details["port"]}]}})
            if frontend == service_name:
                frontend_ingress_yaml = manifestCreator.ingress({"name":service_name+ns_ing_tag,"protocol":protocol.lower(),
                                                                 "ingressClass":ingress_class+str(cpx_count),"tls":tls,
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
            logger.info("ServiceMesh Lite YAMLs are created and is present in \"smlite-all-in-one.yaml\" file.")

class QuotedString(str):  # just subclass the built-in str
    pass

def quoted_scalar(dumper, data):  # a representer to force quotations on scalars
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

if __name__== "__main__":
  main()
