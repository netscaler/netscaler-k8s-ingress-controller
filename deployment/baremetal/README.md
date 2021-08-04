# Citrix ingress controller for Kubernetes

You can deploy the Citrix ingress controller in two ways:

## Citrix ingress controller as a standalone pod

In this deployment, the Citrix ingress controller runs as a pod that monitors the Kubernetes API server and configures Citrix ADC VPX and MPX.

**YAML file for deployment:** ***citrix-k8s-ingress-controller.yaml***

## Citrix ADC CPX with the inbuilt Citrix ingress controller

In this deployment, you deploy Citrix ADC CPX with a builtin Citrix ingress controller agent that configures the Citrix ADC CPX. Citrix ADC CPX runs as pod and does North-South load balancing.

**YAML file for deployment:** ***citrix-k8s-cpx-ingress.yaml***

## Deploy Citrix ADC CPX with inbuilt ingress controller on Kubernetes

Perform the following step to deploy a Citrix ADC CPX along with an inbuilt Ingress controller.

   1. Apply the following command to deploy a Citrix ADC CPX with the inbuilt ingress controller.
      ```
          kubectl apply -f  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml
      ```

## Deploy Citrix ingress controller as a standalone pod

Perform the following steps to deploy the Citrix ingress controller as a stand-alone pod.



 1. Download the `citrix-k8s-ingress-controller.yaml` using the following command.
    ```
      wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml
    ```
                        
    This YAML file has four sections, in which the first three sections are for cluster role creation and service account creation. The
    last one is for Citrix ingress controller pod creation.

    * Cluster roles
    * Cluster role bindings
    * Service account
    * Citrix ingress controller pod creation
   
    First three sections are required for the Citrix ingress controller to monitor Kubernetes events. No changes are required for these sections. The next section defines the environment variables required for the Citrix ingress controller to configure the Citrix ADC.

 2. Edit the YAML file and update the following environment variables.

    1. `Mandatory` arguments:
       <details>
       <summary>NS_IP</summary>

         This variable is a must for the Citrix ingress controller to configure the Citrix ADC appliance. Provide,
         ```
            NSIP for standalone Citrix ADC
            SNIP for HA (Management access has to be enabled) 
            CLIP for Cluster
         
         ```
       </details>
       <details>
       <summary>NS_USER and NS_PASSWORD</summary>

         This variable is for authenticating with Citrix ADC if it has non-default user name and password. You can directly pass user name and password or use Kubernetes secrets.
         For configuring a non-default Citrix ADC user name and password, see [Create a system user account for the Citrix ingress controller in Citrix ADC](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/deploy-cic-yaml.md#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc).

         Given YAML uses Kubernetes secrets. The following steps help to create secrets to be used in YAML.

         Create secrets on Kubernetes for NS_USER and NS_PASSWORD
         Kubernetes secrets can be created by using the `kubectl create secret` command.  

                 kubectl create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot'

         >**Note:** If you are using a different secret name rather than `nslogin`, you have to update the `name` field in the YAML file.

       </details>
       <details>
       <summary>EULA</summary>

          This variable is for the end user license agreement (EULA) which has to be set as `YES` for the Citrix ingress controller to up and run.

       </details>
    2. `Optional` arguments:

       <details>
       <summary>kubernetes_url</summary>

          This variable is an optional field for the Citrix ingress controller to register for events. If you do not specify it explicitly, the Citrix ingress controller uses the internal Kubernetes API server IP address.
   
       </details>
       <details>
       <summary>LOGLEVEL</summary>

         This variable is used for controlling the logs generated from the Citrix ingress controller. Following options are available. By default the log level is DEBUG.
         * CRITICAL 
         * ERROR
         * WARNING
         * INFO
         * DEBUG
       </details>
       <details>

       <summary>NS_PROTOCOL and NS_PORT</summary>
                                
         These environment variables define the protocol and port used by the Citrix ingress controller to communicate with the Citrix ADC.

         By default NS_PROTOCOL is HTTPs and NS_PORT is 443. Other option is to use HTTP and port 80.
       </details>
       <details>
       <summary>Ingress Class</summary>

         [Ingress class](../../docs/configure/ingress-classes.md) is used when multiple Ingress load balancers are used to load balance different ingress resources.

         The Citrix ingress controller configures Citrix ADC only with the ingress classes listed under --ingress-classes

                     args:
                          - --ingress-classes
                                Citrix

         Ingress resources should have the same class mentioned:

                    annotations:
                          kubernetes.io/ingress.class: "Citrix"
       </details>
       <details>

       <summary>NS_VIP</summary>

       Citrix ingress controller uses the IP provided in this environment variable to configure a virtual IP address in the Tier-1 ADC which would receive the application traffic from the external world.

       This variable is useful in the case where all Ingresses run in the Virtual IP address. This variable takes precedence over the [frontend-ip](../../docs/configure/annotations.md) annotation.

       **Usage:**

       ```
       - name: "NS_VIP"
         value: "<Virtual IP address of Citrix ADC>"
       ```

       </details>
       <details>

       <summary>NS_APPS_NAME_PREFIX</summary>

       The Citrix ingress controller uses the provided prefix to form the application entity name in the Citrix ADC. This variable is useful in scenarios where a Citrix ADC load balances applications from different clusters. Prefix allows you to segregate the Kubernetes cluster configuration.

       By default, the Citrix ingress controller adds **k8s** as a prefix to the Citrix ADC entities such as, content switching (CS) virtual server, load balancing (LB) virtual server and so on. You can now customize the prefix using the `NS_APPS_NAME_PREFIX` environment variable in the Citrix ingress controller deployment YAML file. You can use alphanumeric characters for the prefix and the prefix length should not exceed eight characters.
       **Usage:**

       ```
       - name: "NS_APPS_NAME_PREFIX"
         value: "<Name of your choice>"
       ```
       </details>
       <details>
       
       <summary>NS_MGMT_USER</summary>

        This is a Citrix ADC CPX specific environment variable that allows you to register the Citrix ADC CPX instances, installed on a Docker host, to Citrix ADM if Citrix ADM does not have default credentials. This environment variable is supported from Citrix ADC CPX 13.0 and later releases.

       </details>
       <details>
        
       <summary>NS_MGMT_PASS</summary>

        This is a Citrix ADC CPX specific environment variable that allows you to register the Citrix ADC CPX instances, installed on a Docker host, to Citrix ADM if Citrix ADM does not have default credentials. This environment variable is supported from Citrix ADC CPX 13.0 and later releases.

       </details>
        
       <details>
        
       <summary>KUBERNETES_TASK_ID</summary>

        This environment variable is used for disabling the in-built ingress controller. The value of this variable must always be “”(null string). This environment variable is deprecated now.
          
        </details>
      
       <details>
        
       <summary>NS_MGMT_SERVER</summary>

        Specifies the Citrix ADM server or the agent IP address that manages the Citrix ADC CPX.
        
       </details>
       <details>
        
       <summary>NS_MGMT_FINGER_PRINT</summary>

        Specifies the fingerprint of the Citrix ADM server or the agent IP address that manages Citrix ADC CPX.
       </details>
        
       <details>
       <summary>NS_HTTP_PORT</summary>

        Specifies the port on which the HTTP service is available in Citrix ADC CPX. It is used by Citrix ADM to trigger NITRO calls to Citrix ADC CPX.
       </details>
       <details>
       <summary>NS_HTTPS_PORT</summary>

        Specify the port on which HTTPS service is available in Citrix ADC CPX. It is used by Citrix ADM to trigger NITRO calls to Citrix ADC CPX.
       </details>
       <details>
       <summary>LOGSTREAM_COLLECTOR_IP</summary>

        Specifies the Citrix ADM IP address for collecting analytics.
       </details>
     

1. Deploy the Citrix ingress controller using the `kubectl create` command.
        
           kubectl create -f citrix-k8s-ingress-controller.yaml

    This command pulls the latest image and brings up the Citrix ingress controller.
                

    The official Citrix ingress controller docker image is available at: <span style="color:red"> `quay.io/citrix/citrix-k8s-ingress-controller:1.17.13` </span>


2. Configure reachability to the pod network using one of the following.

    - **Static routing**:

      For seamless functioning of services deployed in the Kubernetes cluster, the Citrix ADC ingress device should be able to reach the underlying overlay network over which pods are running. The
    `feature-node-watch` argument of the Citrix ingress controller can be used for automatic route configuration on the Citrix ADC towards the pod network.
    See, [Network Configuration](../../docs/network/staticrouting.md) for more information. 

      By default, `feature-node-watch` is false. It must be explicitly set to true if auto route configuration is required.

    - **Citrix node controller**:

      If the Kubernetes cluster and the Ingress Citrix ADC are in different subnets, you cannot establish a route between them using static routing. This scenario requires an overlay mechanism to establish a route between the Kubernetes cluster and the Ingress Citrix ADC.  

      The [Citrix node controller](https://github.com/citrix/citrix-k8s-node-controller) is a microservice that you can use to create a VXLAN based overlay network between the cluster and the Ingress Citrix ADC device.
