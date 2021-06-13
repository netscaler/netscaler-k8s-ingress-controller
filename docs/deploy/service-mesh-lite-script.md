## Automated deployment of applications in Service Mesh lite

A Service Mesh architecture (like Istio or LinkerD) can be complex to manage. Service Mesh lite architecture is much simpler to get started to achieve the same requirements. To more about Service Mesh lite architecture refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/smlUpdate/docs/deploy/service-mesh-lite.md)

To deploy an application in a Service Mesh lite architecture using Citrix portfolios, you need to perform multiple tasks which include:

- Modifying the existing services to make them headless services
- Creating a service to point to Citrix ADC CPX
- Creating Ingress rules
- Creating Citrix Ingress Controller for Tier-1 ADC if dual-tier topology is required.

However, when you want to deploy multiple applications which consist of several microservices, you may need an easier way you deploy the services in a Service Mesh lite architecture. Citrix provides you an automated way to generate ready to deploy YAMLs out of your application YAMLs for Service Mesh lite deployment.

This topic provides information on how to generate all the necessary YAMLs for Service Mesh lite deployment, where E-W traffic will be handled by Citrix ADC CPX, from your existing YAMLs using the Citrix provided script.

**Prerequisites**

- Ensure python has version 3.7 and above.
- Ensure that pip3 is installed.
- Install the required Python libraries using the following command:
    
      pip3 install -r https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/how-to/sml/requirements.txt

- You need to provide some inputs which are explained in the following section while running the script for your microservice applications.

### Information on required inputs

This section provides information on the inputs you need to provide.

1. Provide one of the following while running the script:

    - Provide the YAML file that contains your application deployments and services. If you are choosing this option, you can directly go to step 2.

    - Provide all service names and the namespace in which they are already running in a Kubernetes cluster. Deployment YAMLs remain the same for running an application in SML architecture, so they can be used as it is. In this case you must provide more inputs as follows:

        You can run the applications from a Kubernetes cluster where the provided services are already running or from a client. Depending on the option you need, choose `Yes` or `No`.

            Do you want to connect to a Remote Kubernetes Cluster? (Y/N):
        
        If you are running the script from a Kubernetes cluster where the services that you want the SML YAML files for are already running then choose which `Kubeconfig` file to use.


        - Choose `Y` if you want to use the default `kubeconfig` file of the Kubernetes cluster.

                    
                     Do you want to use default kubeconfig file present at "/root/.kube/config"? (Y/N):

        - Otherwise, provide the path of the `kubeconfig` file that you want to use:  

                     Please provide path of kubeconfig file:
                    

    
        If you want to run the application from a client, the remote Kubernetes cluster can be accessed either using a bearer token or the `Kubeconfig` file.
      
        - If the remote cluster is accessed using the bearer token, provide the following inputs.
    
        
          1. Choose `Y` if you are using a bearer token to access the remote Kubernetes Cluster:
           
           
           
                    Do you want to use Bearer Token for connecting to a Remote Kubernetes Cluster? (Y/N):
           
        
        
          2. Provide the bearer token.
           
           
                    Please provide Bearer Token key of SA having permission to access given service:

        
          3. Provide API server and port number of the remote Kubernetes cluster.
           
           
                  Please provide API server <IP:PORT>: x.x.x.x:<port>
           
  
        -  If the remote cluster is accessed using the `Kubeconfig` File, provide the following inputs.
  
           1. Choose `N` if you are using `Kubeconfig` File to access the remote Kubernetes Cluster:
          
           
                    Do you want to use bearer token for connecting to a Remote Kubernetes Cluster? (Y/N):
           
    
           2. Provide the path of the `kubeconfig` file of the remote Kubernetes Cluster:
           
           
                    Please provide the path of the kubeconfig file:
        

2. Provide the name of the front-end microservice of the application.
     
     
        Please provide the name of the service exposed to tier-1:

    
3. Provide the host name for the application.

     
        Please provide hostname for exposing the "<frontend-micoservice-name>" service:
     

4. Provide information about the protocol which your microservice is using. The value can be `tcp`,`udp`,`http`,`https`, or `grpc`.
     
     
        Please enter protocol to be used for service "<service-name>" (tcp/udp/http/https/grpc):
     

5. If the Kubernetes service YAML for your microservice is exposing more than one port, then provide the port that is working on the protocol you provided in the previous step.

     
        Found multiple ports in the service "<service-name>". Please enter port to be used <port-list>:
        

6. If the HTTPS protocol is being used by any service, provide the secret to configure TLS certificates for Citrix ADC SSL-based virtual servers. 
     
        Please give secret-name for TLS certificate:
     

For more information on TLS certificate handling by the Citrix ingress controller, see [TLS certificates handling in the Citrix ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/certificate-management/tls-certificates.md).

7. If you want to enable Citrix ADCs to send data to the Citrix Application Delivery Management, please select yes:

       Citrix ADM required? (Y/N):

   - Provide Citrix ADM agent IP for CPX to communicate with ADM, this is generally the service IP of the ADM container agent:

       Please provide IP of ADM Agent(svcIP of container agent) for Citrix ADC CPX:

   - Provide Kubernetes Secret created using Citrix ADM agent credentials, default value for this is "admlogin":

       Please provide name of K8s Secret created using ADM Agent credentials. Press ENTER for 'admlogin': 

8. If you want to use Citrix ingress controller for Tier1 Citix ADC VPX/MPX, please select yes:

       Citrix Ingress Controller for tier-1 ADC required? (Y/N): 

   - Provide Tier-1 Citrix ADC VPX/MPX NSIP:

       Please provide tier-1 ADC NSIP:

   - Provide Tier-1 Citrix ADC VPX/MPX VIP:

       Please provide tier-1 ADC VIP:

   - Provide Kubernetes Secret created using Citrix ADM agent credentials, default value for this is "nslogin":

       Please provide name of K8s Secret created using ADC credentials. Press ENTER for 'nslogin':

   - If have you opted to use ADM in step 7, provide Citrix ADM agent IP for VPX/MPX to communicate with ADM, this is generally the pod IP of the ADM container agent:

       Please provide IP of ADM Agent(podIP of container agent) for Citrix ADC VPX/MPX:

   - Provide the port on which you want to expose frontend microservice of your application:

       Please provide port used to expose "<frontend-micoservice-name>" service to Tier-1 ADC:

   - Provide the which protocol you want to expose frontend microservice of your application:

       Please provide protocol used to expose "<frontend-micoservice-name>" service to Tier-1 ADC (tcp/udp/http/https/grpc):

>**Note:**
>You must create the Kubernetes secret used for the certificates and accessing Citrix ADC or Citric ADM agent before applying the service mesh lite YAMLs.

### Create Service Mesh lite YAMLs

1. Get the required files the citrix-k8s-ingress-controller repository from GitHub using the following command.

         wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/how-to/sml/manifestCreator.py
         wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/how-to/sml/smlite.py


2. Run one of the following commands.


        python3 smlite.py <list-of-path-of-application-yaml-seperated-by-comma>

        or

        python3 smlite.py <list-of-service-names-deployed-in-the-cluster-seperated-by-comma> <namespace>


    For example:

        python3 smlite.py example/netflix.yaml
        Please provide name of the service exposed to tier-1: netflix-frontend-service
        Please provide hostname for exposing "netflix-frontend-service" service: netflix.citrix
        Please enter protocol to be used for service "netflix-frontend-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "tv-shows-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "movies-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "metadata-store-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "recommendation-engine-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "trending-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "similarity-calculator-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "mutual-friends-interests-service" (tcp/udp/http/https/grpc): http
        Please enter protocol to be used for service "telemetry-store-service" (tcp/udp/http/https/grpc): http
        Citrix ADM required? (Y/N): y
        Please provide IP of ADM Agent(svcIP of container agent) for Citrix ADC CPX: 1.1.1.1
        Please provide name of K8s Secret created using ADM Agent credentials. Press ENTER for 'admlogin':
        Citrix Ingress Controller for tier-1 ADC required? (Y/N): y
        Please provide tier-1 ADC NSIP: 2.2.2.2
        Please provide tier-1 ADC VIP: 3.3.3.3
        Please provide name of K8s Secret created using ADC credentials. Press ENTER for 'nslogin': nscred
        Please provide IP of ADM Agent(podIP of container agent) for Citrix ADC VPX/MPX: 4.4.4.4
        Please provide port used to expose CPX service to Tier-1 ADC: 80
        Please provide protocol used to expose CPX service to Tier-1 ADC (tcp/udp/http/https/grpc): http
        2021-06-09 16:18:07,466 - SMLITE - INFO - Please note Tier-1 ADC VPX ingress tier1-vpx-ingress is created with basic config. Please edit it as per your requirements
        2021-06-09 16:18:07,466 - SMLITE - INFO - ServiceMesh Lite YAMLs are created and is present in "smlite-all-in-one.yaml" file.

    A YAML named `smlite-all-in-one.yaml`  gets created with all the YAML files of your application for Service Mesh lite architecture.

    **Note:** If you have used service names which are running inside a cluster to generate the Service Mesh lite YAMLs for them, the `smlite-all-in-one.yaml` file will not contain the deployment YAML files of the application. In that case, you must deploy the deployment YAML files in the application along with the `smlite-all-in-one.yaml` file for running your application in the SML architecture.

    **Note:** This script creates an ingress to expose one of the CPX (CPX handling your frontend microservice) to the tier-1 Citrix ADC VPX. This ingress contains basic config only so please update this ingress if some additonal config is required. For more information on features supported by Citrix ingress contoller see [this](https://github.com/citrix/citrix-k8s-ingress-controller).

### Limitations

The following limitations apply to the automation procedure to generate YAMLs for the Service Mesh lite deployment.

  - Multiple namespaces are not supported while using this automation script. All YAMLs created by the script work only for the single namespace.

  - Only [dual-tier deployment](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#dual-tier-topology) architecture is supported.
