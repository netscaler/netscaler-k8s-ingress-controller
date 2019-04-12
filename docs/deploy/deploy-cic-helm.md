# Deploy Citrix Ingress Controller using Helm charts

You can deploy Citrix Ingress Controller (CIC) in the following modes:

-  As a standalone pod in the Kubernetes cluster. Use this mode if you are controlling Citrix ADCs (Citrix ADC MPX or Citrix ADC VPX) outside the cluster. For example, with [dual-tier](../deployment-topologies.md#dual-tier-topology) topologies, or [single-tier](../deployment-topologies.md#single-tier-topology) topology where the single tier is a Citrix ADC MPX or VPX.

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) (in the same pod) with Citrix ADC CPX in the Kubernetes cluster. The sidecar controller is only responsible for the associated Citrix ADC CPX within the same pod. This mode is used in [dual-tier](../deployment-topologies.md#dual-tier-topology) or [cloud](../deployment-topologies.md#cloud-topology)) topologies.

The helm charts for CIC is available on [Helm Hub](https://hub.helm.sh).

## Deploy CIC as a standalone pod in the Kubernetes cluster

Use the [citrix-k8s-ingress-controller](https://hub.helm.sh/charts/cic/citrix-k8s-ingress-controller) chart to run Citrix Ingress Controller (CIC) as a pod in your Kubernetes cluster. The chart deploys CIC as a pod in your Kubernetes cluster and configures the Citrix ADC VPX or MPX ingress device.

### Prerequisites

-  Determine the NS_IP address needed by the controller to communicate with the appliance. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:

    -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).

-  The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that CIC can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

    You can directly pass the username and password or use Kubernetes secrets. If you want to use Kubernetes secrets, create a secrete for the username and password using the following command:

        kubectl create secret  generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'

#### Create System User Account for CIC in Citrix ADC

Citrix Ingress Controller (CIC) configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission to configure the following on the Citrix ADC:

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

**To create the system user account, perform the following:**

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
        The system user account would have privileges based on the command policy that you define.

1.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

**To deploy CIC as a standalone pod:**

To deploy CIC as standalone pod, follow the instructions provided in the CIC [Helm Hub](https://hub.helm.sh/charts/cic/citrix-k8s-ingress-controller).

## Deploy CIC as a sidecar with Citrix ADC CPX in the Kubernetes cluster

Use the [citrix-k8s-cpx-ingress-controller](https://hub.helm.sh/charts/cic/citrix-k8s-cpx-ingress-controller) chart to deploy a Citrix ADC CPX with CIC as a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/). The chart deploys a Citrix ADC CPX instance that is used for load balancing the North-South traffic to the microservices in your Kubernetes cluster and the sidecar CIC configures the Citrix ADC CPX.

To deploy Citrix ADC CPX with CIC as a sidecar, follow the instruction provided in the CIC [Helm Hub](ttps://hub.helm.sh/charts/cic/citrix-k8s-cpx-ingress-controller).

