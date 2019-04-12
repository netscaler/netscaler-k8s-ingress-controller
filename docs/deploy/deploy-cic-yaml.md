# Deploy Citrix Ingress Controller using YAML

You can deploy Citrix Ingress Controller (CIC) in the following modes:

-  As a standalone pod in the Kubernetes cluster. Use this mode if you are controlling Citrix ADCs (Citrix ADC MPX or Citrix ADC VPX) outside the cluster. For example, with [dual-tier](../deployment-topologies.md#dual-tier-topology) topologies, or [single-tier](../deployment-topologies.md#single-tier-topology) topology where the single tier is a Citrix ADC MPX or VPX.

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) (in the same pod) with Citrix ADC CPX in the Kubernetes cluster. The sidecar controller is only responsible for the associated Citrix ADC CPX within the same pod. This mode is used in [dual-tier](../deployment-topologies.md#dual-tier-topology) or [cloud](../deployment-topologies.md#cloud-topology) topologies.

## Deploy CIC as a standalone pod in the Kubernetes cluster for Citrix ADC MPX or VPX appliances

Use the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file to run Citrix Ingress Controller (CIC) as a standalone pod in your Kubernetes cluster.

!!! note "Note"
    The Citrix ADC MPX or VPX can be deployed in *[standalone](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc.html)*, *[high-availability](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc/configure-ha-first-time.html)*, or *[clustered](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering.html)* modes.

### Prerequisites

-  Determine the NS_IP IP address needed by the controller to communicate with the appliance. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:
    -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html)
-  The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. The Citrix ADC appliance must have a system user account (non-default) with certain privileges so that CIC can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc)

    You can directly pass the username and password as environment variables to the controller, or use Kubernetes secrets (recommended). If you want to use Kubernetes secrets, create a secret for the username and password using the following command:

        kubectl create secret  generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'

#### Create System User Account for CIC in Citrix ADC

Citrix Ingress Controller (CIC) configures the Citrix ADC appliance (MPX or VPX) using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission to configure the following on the Citrix ADC:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Cofigure SSl certkeys
-  Configure routes
-  Configure user monitors
-  Add system file (for uploading SSL certkeys from Kubernetes)
-  Configure Virtual IP address (VIP)
-  Check the status of the Citrix ADC appliance

To create the system user account, perform the following:

1.  Log on to the Citrix ADC appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.

    1.  Log on to the appliance by using the administrator credentials.

1.  Create the system user account using the following command:

        add system user <username> <password>

    For example:

        add system user cic mypassword

1.  Create a policy to provide required permissions to the system user account. Use the following command:

        add cmdpolicy cic-policy ALLOW "(^\S+\s+cs\s+\S+)|(^\S+\s+lb\s+\S+)|(^\S+\s+service\s+\S+)|(^\S+\s+servicegroup\s+\S+)|(^stat\s+system)|(^show\s+ha)|(^\S+\s+ssl\s+certKey)|(^\S+\s+ssl)|(^\S+\s+route)|(^\S+\s+monitor)|(^show\s+ns\s+ip)|(^\S+\s+system\s+file)"

    !!! note "Note"
        The system user account would have the privileges based on the command policy that you define.

1.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

### Deploy CIC as a pod

Perform the following:

1.  Download the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) using the following command:

        wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

1.  Edit the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file and enter the values for the following environmental variables:

    | Environment Variable | Mandatory or Optional | Description |
    | ---------------------- | ---------------------- | ----------- |
    | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](#prerequisites). |
    | NS_USER and NS_PASSWORD | Mandatory | The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](#prerequisites). |
    | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
    | Kubernetes_url | Optional | The kube-apiserver url that CIC uses to register the events. If the value is not specified, CIC uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
    | LOGLEVEL | Optional | The log levels to control the logs generated by CIC. By default, the value is set to DEBUG. The supported values are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Log Levels](../configure/log-levels.md)|
    | NS_PROTOCOL and NS_PORT | Optional | Defines the protocol and port that must be used by CIC to communicate with Citrix ADC. By default, CIC uses HTTPS on port 443. You can also use HTTP on port 80. |
    | ingress-classes | Optional | If multiple ingress load balancers are used to load balance different ingress resources. You can use this environment variable to specify CIC to configure Citrix ADC associated with specific ingress class. For information on Ingress classes, see [Ingress class support](../configure/ingress-classes.md)|
    | NS_IP | Optional | CIC uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. **Note:** NS_VIP takes precedence over the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/annotations.md) annotation. |

1.  Once you update the environment variables, save the YAML file and deploy it using the following command:

        kubectl create -f citrix-k8s-ingress-controller.yaml

1.  Verify if CIC is deployed successfully using the following command:

        kubectl get pods --all-namespaces

## Deploy CIC as a sidecar with Citrix ADC CPX

Use the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) file to deploy a Citrix ADC CPX with CIC as a sidecar. The YAML file deploys a Citrix ADC CPX instance that is used for load balancing the North-South traffic to the microservices in your Kubernetes cluster.

Perform the following:

1.  Download the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) using the following command:

        wget https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml

1.  Edit the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) file and enter the values for the following environmental variables:

    | Environment Variable | Mandatory or Optional | Description |
    | ---------------------- | ---------------------- | ----------- |
    | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](#prerequisites). |
    | NS_USER and NS_PASSWORD | Mandatory | The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](#prerequisites). |
    | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
    | NS_PROTOCOL and NS_PORT | Optional | Defines the protocol and port that must be used by CIC to communicate with Citrix ADC. By default, CIC uses HTTPS on port 443. You can also use HTTP on port 80. |

1.  Once you update the environment variables, save the YAML file and deploy it using the following command:

        kubectl create -f citrix-k8s-cpx-ingress.yaml

1.  Verify if CIC is deployed successfully using the following command:

        kubectl get pods --all-namespaces
