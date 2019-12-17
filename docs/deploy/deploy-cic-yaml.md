# Deploy Citrix ingress controller using YAML

You can deploy Citrix ingress controller in the following modes on your [bare metal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments:

-  As a standalone pod in the Kubernetes cluster. Use this mode if you are controlling Citrix ADCs (Citrix ADC MPX or Citrix ADC VPX) outside the cluster. For example, with [dual-tier](../deployment-topologies.md#dual-tier-topology) topologies, or [single-tier](../deployment-topologies.md#single-tier-topology) topology where the single tier is a Citrix ADC MPX or VPX.

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) (in the same pod) with Citrix ADC CPX in the Kubernetes cluster. The sidecar controller is only responsible for the associated Citrix ADC CPX within the same pod. This mode is used in [dual-tier](../deployment-topologies.md#dual-tier-topology) or [cloud](../deployment-topologies.md#cloud-topology) topologies.

## Deploy Citrix ingress controller as a standalone pod in the Kubernetes cluster for Citrix ADC MPX or VPX appliances

Use the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file to run Citrix ingress controller as a standalone pod in your Kubernetes cluster.

!!! note "Note"
    The Citrix ADC MPX or VPX can be deployed in *[standalone](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc.html)*, *[high-availability](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc/configure-ha-first-time.html)*, or *[clustered](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering.html)* modes.

### Prerequisites

-  Determine the NS_IP IP address needed by the controller to communicate with the appliance. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:
    -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html)
-  The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. The Citrix ADC appliance must have a system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for Citrix ingress controller in Citrix ADC](#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc)

    You can directly pass the username and password as environment variables to the controller, or use Kubernetes secrets (recommended). If you want to use Kubernetes secrets, create a secret for the username and password using the following command:

        kubectl create secret  generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'

#### Create System User Account for Citrix ingress controller in Citrix ADC

Citrix ingress controller configures the Citrix ADC appliance (MPX or VPX) using a system user account of the Citrix ADC. The system user account should have certain privileges so that the Citrix ingress controller has permission to configure the following on the Citrix ADC:

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

        add cmdpolicy cic-policy ALLOW "^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^(add|show)\s+system\s+file)"

    !!! note "Note"
        The system user account would have privileges based on the command policy that you define. The command policy mentioned in ***step 3*** is similar to the built-in `sysAdmin` command policy with additional permission to upload files.

1.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

### Deploy Citrix ingress controller as a pod

Perform the following:

1.  Download the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) using the following command:

        wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

1.  Edit the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file and enter the values for the following environmental variables:

    | Environment Variable | Mandatory or Optional | Description |
    | ---------------------- | ---------------------- | ----------- |
    | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](#prerequisites). |
    | NS_USER and NS_PASSWORD | Mandatory | The username and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](#prerequisites). |
    | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
    | Kubernetes_url | Optional | The kube-apiserver url that Citrix ingress controller uses to register the events. If the value is not specified, Citrix ingress controller uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
    | LOGLEVEL | Optional | The log levels to control the logs generated by Citrix ingress controller. By default, the value is set to DEBUG. The supported values are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Log Levels](../configure/log-levels.md)|
    | NS_PROTOCOL and NS_PORT | Optional | Defines the protocol and port that must be used by Citrix ingress controller to communicate with Citrix ADC. By default, Citrix ingress controller uses HTTPS on port 443. You can also use HTTP on port 80. |
    | ingress-classes | Optional | If multiple ingress load balancers are used to load balance different ingress resources. You can use this environment variable to specify Citrix ingress controller to configure Citrix ADC associated with specific ingress class. For information on Ingress classes, see [Ingress class support](../configure/ingress-classes.md)|
    | NS_VIP | Optional | Citrix ingress controller uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. </br>**Note:** NS_VIP takes precedence over the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/annotations.md) annotation. |
    | NS_APPS_NAME_PREFIX | Optional | By default, the Citrix ingress controller adds "**k8s**" as prefix to the Citrix ADC entities such as, content switching (CS) virtual server, load balancing (LB) virtual server and so on. You can now customize the prefix using the `NS_APPS_NAME_PREFIX` environment variable in the Citrix ingress controller deployment YAML file. You can use alphanumberic charaters for the prefix and the prefix length should not exceed 8 characters. |
    | NS_NETPROFILE | Optional | [Citrix node controller](https://github.com/citrix/citrix-k8s-node-controller) uses the network profile (netprofile) provided in this environment variable to establish network connectivity between the Kubernetes nodes and Ingress Citrix ADC. </br> **Note:** Ensure that you provide the same netprofile name while deploying the Citrix node controller. For more information on how to deploy Citrix node controller, see [Deploy the Citrix k8s node controller](https://github.com/citrix/citrix-k8s-node-controller/tree/master/deploy) |
     | NAMESPACE | Optional | While running a Citrix ingress controller with Role based RBAC, you need to provide the namespace which you want to listen or get events. This namespace must be same as the one used for creating the service account. Using the service account, the Citrix ingress controller can listen on a namespace. You can use the  `NAMESPACE` environment variable to specify the namespace. see [Deploy the Citrix Ingress controller for a namespace](#Deploy-the-Citrix-Ingress-controller-for-a-namespace) |

2.  Once you update the environment variables, save the YAML file and deploy it using the following command:

        kubectl create -f citrix-k8s-ingress-controller.yaml

3.  Verify if Citrix ingress controller is deployed successfully using the following command:

        kubectl get pods --all-namespaces

## Deploy Citrix ingress controller as a sidecar with Citrix ADC CPX

Use the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) file to deploy a Citrix ADC CPX with Citrix ingress controller as a sidecar. The YAML file deploys a Citrix ADC CPX instance that is used for load balancing the North-South traffic to the microservices in your Kubernetes cluster.

Perform the following:

1.  Download the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) using the following command:

        wget https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml

1.  Deploy the `citrix-k8s-cpx-ingress.yaml` file using the following command:

        kubectl create -f citrix-k8s-cpx-ingress.yaml

1.  Verify if Citrix ingress controller is deployed successfully using the following command:

        kubectl get pods --all-namespaces

## Deploy the Citrix Ingress controller for a namespace

In Kubernetes, a role consists of rules that define a set of permissions that can be performed on a set of resources. In an RBAC enabled Kubernetes environment, you can create two kinds of roles based on the scope you need:

- `Role`
- `ClusterRole`

A role can be defined within a namespace with a `Role`, or cluster-wide with a `ClusterRole`. You can create a `Role` to grant access to resources within a single namespace.

In Kubernetes, you can create multiple virtual clusters on the same physical cluster. Namespaces provides a way to divide cluster resources between multiple users and useful in environments with many users spread across multiple teams, or projects.

By default, the Citrix ingress controller monitors Ingress resources across all namespaces in the Kubernetes cluster. If multiple teams want to manage the same Citrix ADC, they can deploy a `Role` based Citrix ingress controller to monitor only ingress resources belongs to a specific namespace. This namespace must be same as the namespace you have provided for creating the service account.
You need to create a Role and bind the role to the service account for the Citrix ingress controller. In this case, the Citrix ingress controller listens only for events from the specified namespace and then configure the Citrix ADC accordingly.

The following example shows a sample YAML file which defines a Role and RoleBinding for deploying a Citrix ingress controller for a specific namespace.

```yml

kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cic-k8s-role
rules:
  - apiGroups: [""]
    resources: ["endpoints", "ingresses", "pods", "secrets", "nodes", "routes", "namespaces"]
    verbs: ["get", "list", "watch"]
  # services/status is needed to update the loadbalancer IP in service status for integrating
  # service of type LoadBalancer with external-dns
  - apiGroups: [""]
    resources: ["services/status"]
    verbs: ["patch"]
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["get", "list", "watch", "patch"]
  - apiGroups: ["extensions"]
    resources: ["ingresses", "ingresses/status"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]

---

kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cic-k8s-role
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: cic-k8s-role

subjects:
- kind: ServiceAccount
  name: cic-k8s-role
  namespace: default

---

```

### Restrictions

When the Citrix ingress controller runs with a Role (scope with in a namespace), the following functionalities are not supported as they require global scope.

- configuring static routes
- watching on all namespaces
- CRDs