# **Citrix Ingress Controller for kubernetes:**
Citrix Ingress Controller is available in two flavours.
## **Citrix Ingress Controller:**
This runs as a POD that monitors the Kubernetes API server and configure NetScaler VPX and MPX. 

**YAML to be used:** ***citrix-k8s-ingress-controller.yaml***
## **CPX with inbuilt Ingress Controller:**
CPX with a builtin Citrix Ingress Controller agent that configures the CPX. CPX runs as pod and does N-S load balancing. 

**YAML to be used:** ***citrix-k8s-cpx-ingress.yaml***

```
   Citrix Ingress Controller will do "clear config -f basic" on the NetScaler. Please refer [here](https://support.citrix.com/article/CTX112695/#basic) for more details.
   Fix  will be avilable soon.
```

# **Install Citrix Ingress Controller on Kubernetes:**
 1. Download or copy the YML file "citrix-k8s-ingress-controller.yaml" from the deployment Directory.
                        
    This yaml has four section, in which first three is for cluster role creation and service account creation and the 
    next one is for citrix ingress controller pod creation. 
    * Cluster roles
    * Cluster role bindings
    * Service account
    * Citrix Ingress Controller pod creation
   
    First three are required for citrix ingress controller to monitor k8s events. No changes required.
    Next section defines environment variables required for Citrix Ingress Controller to configure the NetScaler.

 2. Update the following env variables, for Citrix Ingress Controller bringup.

    1. "Mandatory" Arguments:
       <details>
       <summary>NS_IP</summary>

         This is must for Citrix Ingress Controller to configure the NetScaler appliance. Provide,
         ```
            NSIP for standalone NetScaler  
            SNIP for HA (Management access has to be enabled) 
            CLIP for Cluster
         
         ```
       </details>
       <details>
       <summary>NS_USER and NS_PASSWORD</summary>

         This is for authenticating with NetScaler if it has non default username and password. We can directly pass username/password or use Kubernetes secrets.
         Given Yaml uses k8s secrets. Following steps helps to create secrets to be used in yaml.

         Create secrets on Kubernetes for NS_USER and NS_PASSWORD
         Kubernetes secrets can be created by using 'kubectl create secret'.  

                 kubectl create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot'

         >**Note:** If you are using different secret name rather than nslogin, you have to update the "name" field in the yaml. 

       </details>
       <details>
       <summary>EULA</summary>

         This is end user license agreement which has to be YES for Citrix Ingress Controller to up and run.
                
       </details>
    2. "Optional" Arguments:

       <details>
       <summary>kubernetes_url</summary>

         This is an optional field for Citrix Ingress Controller to register for events. If user did not specify it explictly, citrix ingress controller use internal KubeAPIServer IP. 
   
       </details>
       <details>
       <summary>LOGLEVEL</summary>

         This is used for controlling the logs generated from Citrix Ingress Controller. Following options are available. By default log level is DEBUG. 
         * CRITICAL 
         * ERROR
         * WARNING
         * INFO
         * DEBUG
       </details>
       <details>

       <summary>NS_PROTOCOL and NS_PORT</summary>
                                
         These enviornment variables defines protocol and port used by Citrix Ingress Controller  to communicate with NetScaler.

         By default NS_PROTOCOL is https and NS_PORT is 443. Other option is to use HTTP and port 80. 
       </details>
       <details>
       <summary>Ingress Class</summary>

         Ingress class is used when multiple Ingress Loadbalancers are used to load balance different ingress resources. 

         Citrix Ingress Controller  will configure NetScaler only with the ingress classes listed under --ingress-classes

                     args:
                          - --ingress-classes
                                Citrix

         Ingress resources should have the same class mentioned:

                    annotations:
                          kubernetes.io/ingress.class: "Citrix"

3. Create using kubectl command. 

   Create Citrix Ingress Controller  on kubernetes by using 'kubectl create' command
        
           kubectl create -f citrix-k8s-ingress-controller.yaml

   This pulls the latest image and brings up the Citrix Ingress Controller.
                
   Official Citrix Ingress Controller docker images is <span style="color:red"> `gcr.io/citrix-k8s-ingress-controller/citrix-ingress-controller:latest` </span> 

4. Configure routes for POD reachability
```
  Obtain podCIDR using below options:
  # kubectl get nodes -o yaml | grep podCIDR
     podCIDR: 10.244.0.0/24
     podCIDR: 10.244.1.0/24
     podCIDR: 10.244.2.0/24

  Add Route to Netscaler
  # add route <podCIDR_network> <podCIDR_netmask> <node_HostIP>
```     
  Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which K8S nodes communicate with each other. Usually eth0 IP is from this network).
 
```       
  Example: 
  Node1 IP = 10.102.53.101 
  podCIDR  = 10.244.1.0/24
  add route 10.244.1.0 255.255.255.0 10.102.53.101
```
# **Install CPX with inbuilt Ingress Controller on Kubernetes:**
   This is end user license agreement which has to be YES for CPX to up and run.
   This pulls image from `us.gcr.io/citrix-217108/citrix-k8s-cpx-ingress:latest` which has both cpx and citrix ingress controller in built and start configuring itself.
   ```
           kubectl create -f citrix-k8s-cpx-ingress.yml
   ```
# **Annotations**


List of annotations supported by Citrix Ingress Controller:

* ingress.citrix.com/frontend-ip 
```
            Custom VIP. This IP will be configured in NetScaler as VIP. 
            Default Value : NSIP of NetScaler.
```
* ingress.citrix.com/secure-port 
```
            Port for https traffic 
            This port will be configured in NetScaler CS Vserver. 
            Default Value : 443.
```
* ingress.citrix.com/insecure-port
```
            Port for http traffic 
            This port will be configured in NetScaler CS Vserver. 
            Default Value : 80.
```
* ingress.citrix.com/insecure-termination 
```
            Use "allow" to permit http traffic
            Use "redirect" to redirect http to https
            Use "disallow" to drop http traffic. 
            Default Value : disallow.
```
* ingress.citrix.com/secure-backend  
```
            Set secure-backend as True, to have SSL backend
            Default Value : False.
```


                        
