# Netscaler ingress controller for Kubernetes

You can deploy the Netscaler ingress controller in two ways:

## Netscaler ingress controller as a standalone pod

In this deployment, the Netscaler ingress controller runs as a pod that monitors the Kubernetes API server and configures Netscaler VPX and MPX.

**YAML file for deployment:** ***citrix-k8s-ingress-controller.yaml***

## Netscaler CPX with the inbuilt Netscaler ingress controller

In this deployment, you deploy Netscaler CPX with a built-in Netscaler ingress controller agent that configures the Netscaler CPX. Netscaler CPX runs as pod and does North-South load balancing.

**YAML file for deployment:** ***citrix-k8s-cpx-ingress.yaml***

## Deploy Netscaler CPX with inbuilt ingress controller on Kubernetes

Perform the following step to deploy a Netscaler CPX along with an inbuilt Ingress controller.

   1. Apply the following command to deploy a Netscaler CPX with the inbuilt ingress controller.
      ```
          kubectl apply -f  https://raw.githubusercontent.com/netscaler/netscaler-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml
      ```

## Deploy Netscaler ingress controller as a standalone pod

Perform the following steps to deploy the Netscaler ingress controller as a stand-alone pod.



 1. Download the `citrix-k8s-ingress-controller.yaml` using the following command.
    ```
      wget  https://raw.githubusercontent.com/netscaler/netscaler-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml
    ```
                        
    This YAML file has four sections, in which the first three sections are for cluster role creation and service account creation. The
    last one is for Netscaler ingress controller pod creation.

    * Cluster roles
    * Cluster role bindings
    * Service account
    * Netscaler ingress controller pod creation
   
    First three sections are required for the Netscaler ingress controller to monitor Kubernetes events. No changes are required for these sections. The next section defines the environment variables required for the Netscaler ingress controller to configure the Netscaler.

 2. Edit the YAML file and update the following environment variables.

    1. `Mandatory` arguments:
       <details>
       <summary>NS_IP</summary>

         This variable is a must for the Netscaler ingress controller to configure the Netscaler appliance. Provide,
         ```
            NSIP for standalone Netscaler
            SNIP for HA (Management access has to be enabled) 
            CLIP for Cluster
         
         ```
       </details>
       <details>
       <summary>NS_USER and NS_PASSWORD</summary>

         This variable is for authenticating with Netscaler if it has non-default user name and password. You can directly pass user name and password or use Kubernetes secrets.
         For configuring a non-default Netscaler user name and password, see [Create a system user account for the Netscaler ingress controller in Netscaler](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/deploy/deploy-cic-yaml.md#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc).

         Given YAML uses Kubernetes secrets. The following steps help to create secrets to be used in YAML.

         Create secrets on Kubernetes for NS_USER and NS_PASSWORD
         Kubernetes secrets can be created by using the `kubectl create secret` command.  

                 kubectl create secret  generic nslogin --from-literal=username=<username> --from-literal=password=<password>

         >**Note:** If you are using a different secret name rather than `nslogin`, you have to update the `name` field in the YAML file.

       </details>
       <details>
       <summary>EULA</summary>

          This variable is for the end user license agreement (EULA) which has to be set as `YES` for the Netscaler ingress controller to up and run.

       </details>
    2. `Optional` arguments:

       <details>
       <summary>kubernetes_url</summary>

          This variable is an optional field for the Netscaler ingress controller to register for events. If you do not specify it explicitly, the Netscaler ingress controller uses the internal Kubernetes API server IP address.
   
       </details>
       <details>
       <summary>LOGLEVEL</summary>

         This variable is used for controlling the logs generated from the Netscaler ingress controller. Following options are available. By default the log level is DEBUG.
         * CRITICAL 
         * ERROR
         * WARNING
         * INFO
         * DEBUG
       </details>
       <details>

       <summary>NS_PROTOCOL and NS_PORT</summary>
                                
         These environment variables define the protocol and port used by the Netscaler ingress controller to communicate with the Netscaler.

         By default NS_PROTOCOL is HTTPS and NS_PORT is 443.
       </details>
       <details>
       <summary>Ingress Class</summary>

         [Ingress class](../../docs/configure/ingress-classes.md) is used when multiple Ingress load balancers are used to load balance different ingress resources.

         The Netscaler ingress controller configures Netscaler only with the ingress classes listed under --ingress-classes

                     args:
                          - --ingress-classes
                                Citrix

         Ingress resources should have the same class mentioned:

                    annotations:
                          kubernetes.io/ingress.class: "Citrix"
       </details>
       <details>

       <summary>NS_VIP</summary>

       Netscaler ingress controller uses the IP provided in this environment variable to configure a virtual IP address in the Tier-1 ADC which would receive the application traffic from the external world.

       This variable is useful in the case where all Ingresses run in the Virtual IP address. This variable takes precedence over the [frontend-ip](../../docs/configure/annotations.md) annotation.

       **Usage:**

       ```
       - name: "NS_VIP"
         value: "<Virtual IP address of Netscaler>"
       ```

       </details>
       <details>

       <summary>NS_APPS_NAME_PREFIX</summary>

       The Netscaler ingress controller uses the provided prefix to form the application entity name in the Netscaler. This variable is useful in scenarios where a Netscaler load balances applications from different clusters. Prefix allows you to segregate the Kubernetes cluster configuration.

       By default, the Netscaler ingress controller adds **k8s** as a prefix to the Netscaler entities such as, content switching (CS) virtual server, load balancing (LB) virtual server and so on. You can now customize the prefix using the `NS_APPS_NAME_PREFIX` environment variable in the Netscaler ingress controller deployment YAML file. You can use alphanumeric characters for the prefix and the prefix length should not exceed eight characters.
       **Usage:**

       ```
       - name: "NS_APPS_NAME_PREFIX"
         value: "<Name of your choice>"
       ```
       </details>
       <details>
       
       <summary>NS_MGMT_USER</summary>

        This is a Netscaler CPX specific environment variable that allows you to register the Netscaler CPX instances, installed on a Docker host, to Citrix ADM if Citrix ADM does not have default credentials. This environment variable is supported from Netscaler CPX 13.0 and later releases.

       </details>
       <details>
        
       <summary>NS_MGMT_PASS</summary>

        This is a Netscaler CPX specific environment variable that allows you to register the Netscaler CPX instances, installed on a Docker host, to Citrix ADM if Citrix ADM does not have default credentials. This environment variable is supported from Netscaler CPX 13.0 and later releases.

       </details>
        
       <details>
        
       <summary>KUBERNETES_TASK_ID</summary>

        This environment variable is used for disabling the in-built ingress controller. The value of this variable must always be “”(null string). This environment variable is deprecated now.
          
        </details>
      
       <details>
        
       <summary>NS_MGMT_SERVER</summary>

        Specifies the Citrix ADM server or the agent IP address that manages the Netscaler CPX.
        
       </details>
       <details>
        
       <summary>NS_MGMT_FINGER_PRINT</summary>

        Specifies the fingerprint of the Citrix ADM server or the agent IP address that manages Netscaler CPX.
       </details>
        
       <details>
       <summary>NS_HTTP_PORT</summary>

        Specifies the port on which the HTTP service is available in Netscaler CPX. It is used by Citrix ADM to trigger NITRO calls to Netscaler CPX.
       </details>
       <details>
       <summary>NS_HTTPS_PORT</summary>

        Specify the port on which HTTPS service is available in Netscaler CPX. It is used by Citrix ADM to trigger NITRO calls to Netscaler CPX.
       </details>
       <details>
       <summary>LOGSTREAM_COLLECTOR_IP</summary>

        Specifies the Citrix ADM IP address for collecting analytics.
       </details>
       <details>
       <summary>NS_DNS_NAMESERVER</summary>
        Enables adding DNS nameservers on Netscaler VPX.
       </details>

       <details>
       <summary>NS_CONFIG_DNS_REC</summary>
        Enables adding DNS records on Netscaler for Ingress resources. This variable is configured at the boot time and cannot be changed at runtime. Possible values are true or false. The default value is `false` and you need to set it as `true` to enable the DNS server configuration.
       </details>
       
       <details>
       <summary>NS_SVC_LB_DNS_REC</summary>
        Enables adding DNS records on Netscaler for services of type LoadBalancer. Possible values are true or false. This variable is configured at the boot time and cannot be changed at runtime. The default value is `false` and you need to set it as `true` to enable the DNS server configuration.
       </details>
      
       <details>
       <summary> OPTIMIZE_ENDPOINT_BINDING</summary>
      
       Enables or disables binding of back-end endpoints to a service group in a single API call. This variable is recommended when there are a large number of endpoints (pods) per application. Acceptable values are `True` and `False`. This environment variable is applicable only for Netscaler release 13.0–45.7 and higher versions.
       </details>

       <details>
       <summary> SCOPE</summary>
        Enables configuring the scope of Netscaler ingress controller as `Role` or `ClusterRole` binding.
        You can set the value of the `SCOPE` environment variable as `local` or `cluster`. When you set this variable as `local`, Netscaler ingress controller is deployed with `Role` binding that has limited privileges. You can use this option when you want to deploy Netscaler ingress controller with minimal privileges for a particular namespace with `Role` binding. By default, the value of `SCOPE` is set as `cluster` and Netscaler ingress controller is deployed with the `ClusterRole` binding.
       </details>
       <details>
        <summary>POD_IPS_FOR_SERVICEGROUP_MEMBERS</summary>
         By default, while configuring services of type LoadBalancer and NodePort on an external tier-1 Citrix ADC the Citrix ingress controller adds NodeIP and NodePort as service group members. If this variable is set as `True`, pod IP address and port are added instead of NodeIP and NodePort as service group members.
        </details>

1. Deploy the Netscaler ingress controller using the `kubectl create` command.
        
           kubectl create -f citrix-k8s-ingress-controller.yaml

    This command pulls the latest image and brings up the Netscaler ingress controller.
                

    The official Netscaler ingress controller docker image is available at: <span style="color:red"> `quay.io/netscaler/netscaler-k8s-ingress-controller:1.39.6` </span>


2. Configure reachability to the pod network using one of the following.

    - **Static routing**:

      For seamless functioning of services deployed in the Kubernetes cluster, the Netscaler ingress device should be able to reach the underlying overlay network over which pods are running. The
    `feature-node-watch` argument of the Netscaler ingress controller can be used for automatic route configuration on the Netscaler towards the pod network.
    See, [Network Configuration](../../docs/network/staticrouting.md) for more information. 

      By default, `feature-node-watch` is false. It must be explicitly set to true if auto route configuration is required.

    - **Citrix node controller**:

      If the Kubernetes cluster and the Ingress Netscaler are in different subnets, you cannot establish a route between them using static routing. This scenario requires an overlay mechanism to establish a route between the Kubernetes cluster and the Ingress Netscaler.  

      The [Citrix node controller](https://github.com/netscaler/netscaler-k8s-node-controller) is a microservice that you can use to create a VXLAN based overlay network between the cluster and the Ingress Netscaler device.
