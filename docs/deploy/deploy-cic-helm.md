# Deploy the Netscaler ingress controller using Helm charts

You can deploy the Netscaler ingress controller in the following modes on your [bare metal](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/deployment) deployments:

-  As a standalone pod in the Kubernetes cluster. Use this mode if you are controlling Netscalers (Netscaler MPX or Netscaler VPX) outside the cluster. For example, with [dual-tier](../deployment-topologies.md#dual-tier-topology) topologies, or [single-tier](../deployment-topologies.md#single-tier-topology) topology where the single tier is a Netscaler MPX or VPX.

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) (in the same pod) with Netscaler CPX in the Kubernetes cluster. The sidecar controller is only responsible for the associated Netscaler CPX within the same pod. This mode is used in [dual-tier](../deployment-topologies.md#dual-tier-topology) or [cloud](../deployment-topologies.md#cloud-topology)) topologies.

The helm charts for the Netscaler ingress controller are available on [Artifact Hub](https://artifacthub.io/).

 When you deploy using the Helm charts, you can use a `values.yaml` file to specify the values of the configurable parameters instead of providing each parameter as an argument. For ease of use, Citrix provides the [Citrix deployment builder](https://netscaler.github.io/netscaler-k8s-ingress-controller/) which is a GUI for generating the `values.yaml` file for Citrix cloud native deployments.

## Deploy the Netscaler ingress controller as a standalone pod in the Kubernetes cluster

Use the [citrix-ingress-controller](https://artifacthub.io/packages/helm/netscaler/netscaler-ingress-controller) chart to run the Netscaler ingress controller as a pod in your Kubernetes cluster. The chart deploys the Netscaler ingress controller as a pod in your Kubernetes cluster and configures the Netscaler VPX or MPX ingress device.

### Prerequisites

-  Determine the NS_IP address needed by the controller to communicate with the appliance. The IP address might be anyone of the following depending on the type of Netscaler deployment:

    -  (Standalone appliances) NSIP - The management IP address of a standalone Netscaler appliance. For more information, see [IP Addressing in Netscaler](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Netscaler](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Netscaler deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).

-  The user name and password of the Netscaler VPX or MPX appliance used as the Ingress device. The Netscaler appliance needs to have a system user account (non-default) with certain privileges so that the Netscaler ingress controller can configure the Netscaler VPX or MPX appliance. For instructions to create the system user account on Netscaler, see[Create System User Account for Netscaler ingress controller in Netscaler](#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc).

    You can directly pass the user name and password or use Kubernetes secrets. If you want to use Kubernetes secrets, create a secret for the user name and password using the following command:

        kubectl create secret  generic nslogin --from-literal=username=<username> --from-literal=password=<password>

#### Create a system user account for the Netscaler ingress controller in Netscaler

The Netscaler ingress controller configures the Netscaler using a system user account of the Netscaler. The system user account should have certain privileges so that the Netscaler ingress controller has permission to configure the following on the Netscaler:

-  Add, delete, or view content switching (CS) virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure service groups
-  Cofigure SSL certkeys
-  Configure routes
-  Configure user monitors
-  Add system file (for uploading SSL certkeys from Kubernetes)
-  Configure Virtual IP address (VIP)
-  Check the status of the Netscaler appliance

**To create the system user account, perform the following:**

1.  Log on to the Netscaler appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Netscaler appliance.

    2.  Log on to the appliance by using the administrator credentials.

2.  Create the system user account using the following command:

        add system user <username> <password>

    For example:

        add system user cic mypassword

3.  Create a policy to provide required permissions to the system user account. Use the following command:

        add cmdpolicy cic-policy ALLOW '^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)'

    **Note**: The system user account would have privileges based on the command policy that you define.

    The command policy mentioned in ***step 3*** is similar to the built-in `sysAdmin` command policy with additional permission to upload files.  For more information on command policy, see the [Netscaler documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/system/authentication-and-authorization-for-system-user/user-usergroups-command-policies.html#configure-command-policies).

    In the command policy specification provided, special characters which need to be escaped are already omitted to easily copy-paste into the Netscaler command line.

    For configuring the command policy from Netscaler configuration wizard (GUI), use the following command policy specification.

        ^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)


4.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

**To deploy the Netscaler ingress controller as a standalone pod:**

To deploy the Netscaler ingress controller as standalone pod, follow the instructions provided in the Netscaler ingress controller [Artifact Hub](https://artifacthub.io/packages/helm/netscaler/netscaler-ingress-controller).

## Deploy the Netscaler ingress controller as a sidecar with Netscaler CPX in the Kubernetes cluster

Use the [citrix-cpx-with-ingress-controller](https://artifacthub.io/packages/helm/netscaler/citrix-cpx-with-ingress-controller) chart to deploy a Netscaler CPX with Netscaler ingress controller as a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/). The chart deploys a Netscaler CPX instance that is used for load balancing the North-South traffic to the microservices in your Kubernetes cluster. The sidecar Netscaler ingress controller configures the Netscaler CPX.

To deploy Netscaler CPX with the Netscaler ingress controller as a sidecar, follow the instruction provided in the Netscaler ingress controller [Helm Hub](https://artifacthub.io/packages/helm/netscaler/citrix-cpx-with-ingress-controller).
