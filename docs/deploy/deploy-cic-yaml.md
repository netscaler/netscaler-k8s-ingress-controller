# Deploy Citrix ingress controller using YAML

You can deploy Citrix ingress controller in the following modes on your [bare metal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments:

-  As a standalone pod in the Kubernetes cluster. Use this mode if you are controlling Citrix ADCs (Citrix ADC MPX or Citrix ADC VPX) outside the cluster. For example, with [dual-tier](../deployment-topologies.md#dual-tier-topology) topologies, or [single-tier](../deployment-topologies.md#single-tier-topology) topology where the single tier is a Citrix ADC MPX or VPX.

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) (in the same pod) with Citrix ADC CPX in the Kubernetes cluster. The sidecar controller is only responsible for the associated Citrix ADC CPX within the same pod. This mode is used in [dual-tier](../deployment-topologies.md#dual-tier-topology) or [cloud](../deployment-topologies.md#cloud-topology) topologies.

## Deploy Citrix ingress controller as a standalone pod in the Kubernetes cluster for Citrix ADC MPX or VPX appliances

Use the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file to run the Citrix ingress controller as a standalone pod in your Kubernetes cluster.

!!! note "Note"
    The Citrix ADC MPX or VPX can be deployed in *[standalone](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc.html)*, *[high-availability](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc/configure-ha-first-time.html)*, or *[clustered](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering.html)* modes.

### Prerequisites

-  Determine the NS_IP IP address needed by the controller to communicate with the appliance. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:
    -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html)
    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html)
-  The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. The Citrix ADC appliance must have a system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for Citrix ingress controller in Citrix ADC](#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc)

    You can directly pass the user name and password as environment variables to the controller, or use Kubernetes secrets (recommended). If you want to use Kubernetes secrets, create a secret for the user name and password using the following command:

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

        add cmdpolicy cic-policy ALLOW '^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)'

    **Note**: The system user account would have privileges based on the command policy that you define.
    The command policy mentioned in ***step 3*** is similar to the built-in `sysAdmin` command policy with another permission to upload files.

    The command policy spec provided above have already escaped special characters for easier copy pasting into the Citrix ADC command line.

    For configuring the command policy from Citrix ADC Configuration Wizard (GUI), use the below command policy spec.

        ^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)


1.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

### Deploy Citrix ingress controller as a pod

Perform the following:

1.  Download the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) using the following command:

        wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

1.  Edit the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file and enter the values for the following environmental variables:

    | Environment Variable    | Mandatory or Optional | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
    | ----------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | NS_IP                   | Mandatory             | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](#prerequisites).                                                                                                                                                                                                                                                                                                                                                                                                                            |
    | NS_USER and NS_PASSWORD | Mandatory             | The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](#prerequisites).                                                                                                                                                                                                                                                                                                                                                                          |
    | EULA                    | Mandatory             | The End User License Agreement. Specify the value as `Yes`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
    | Kubernetes_url          | Optional              | The kube-apiserver url that Citrix ingress controller uses to register the events. If the value is not specified, Citrix ingress controller uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod).                                                                                                                                                                                                                          |
    | LOGLEVEL                | Optional              | The log levels to control the logs generated by Citrix ingress controller. By default, the value is set to DEBUG. The supported values are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Log Levels](../configure/log-levels.md)                                                                                                                                                                                                                                                                     |
    | NS_PROTOCOL and NS_PORT | Optional              | Defines the protocol and port that is used by the Citrix ingress controller to communicate with Citrix ADC. By default, Citrix ingress controller uses HTTP on port 80. You can also use HTTPS on port 443.                                                                                                                                                                                                                                                                                                                   |
    | ingress-classes         | Optional              | If multiple ingress load balancers are used to load balance different ingress resources. You can use this environment variable to specify the Citrix ingress controller to configure Citrix ADC associated with specific ingress class. For information on Ingress classes, see [Ingress class support](../configure/ingress-classes.md)                                                                                                                                                                                      |
    | NS_VIP                  | Optional              | Citrix ingress controller uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. </br>**Note:** NS_VIP acts as a fallback when the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/annotations.md) annotation is not provided in Ingress yaml. Not supported for Type Loadbalancer service.                                                                                                                                                                                   |
    | NS_APPS_NAME_PREFIX     | Optional              | By default, the Citrix ingress controller adds "**k8s**" as prefix to the Citrix ADC entities such as, content switching (CS) virtual server, load balancing (LB) virtual server and so on. You can now customize the prefix using the `NS_APPS_NAME_PREFIX` environment variable in the Citrix ingress controller deployment YAML file. You can use alphanumeric characters for the prefix and the prefix length should not exceed 8 characters.                                                                             |
    | NAMESPACE               | Optional              | While running a Citrix ingress controller with Role based RBAC, you must provide the namespace which you want to listen or get events. This namespace must be same as the one used for creating the service account. Using the service account, the Citrix ingress controller can listen on a namespace. You can use the  `NAMESPACE` environment variable to specify the namespace. For more information, see [Deploy the Citrix ingress controller for a namespace](#Deploy-the-Citrix-ingress-controller-for-a-namespace). |
    | POD_IPS_FOR_SERVICEGROUP_MEMBERS| Optional| By default, while configuring services of type LoadBalancer and NodePort on an external tier-1 Citrix ADC the Citrix ingress controller adds NodeIP and NodePort as service group members. If this variable is set as `True`, pod IP address and port are added instead of NodeIP and NodePort as service group members.|
    |IGNORE_NODE_EXTERNAL_IP| Optional |While adding NodeIP for services of type LoadBalancer or NodePort on an external tier-1 Citrix ADC, the Citrix ingress controller prioritizes an external IP address over an internal IP address. When you want to prefer an internal IP address over an external IP address for NodeIP, you can set this variable to `True`.|
    | NS_CONFIG_DNS_REC | Optional| Enables the DNS server configuration on Citrix ADC. This variable is configured at the boot time and cannot be changed at runtime. Possible values are true or false. The default value is `false` and you need to set it as `true` to enable the DNS server configuration. When you set the value as 'true', the corresponding command `add dns addrec <abc.com 1.1.1.1>` is executed on Citrix ADC and an address record (mapping of the domain name to IP address)  is created. For more information, see [Create address records for a domain name](https://docs.citrix.com/en-us/citrix-adc/current-release/dns/configure-dns-resource-records/create-address-records.html#:~:text=Add%20an%20Address%20record%20by%20using%20the%20GUI,and%20create%20an%20Address%20record). |


2.  Once you update the environment variables, save the YAML file and deploy it using the following command:

        kubectl create -f citrix-k8s-ingress-controller.yaml

3.  Verify if Citrix ingress controller is deployed successfully using the following command:

        kubectl get pods --all-namespaces

## Deploy Citrix ingress controller as a sidecar with Citrix ADC CPX

Use the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) file to deploy a Citrix ADC CPX with Citrix ingress controller as a sidecar. The YAML file deploys a Citrix ADC CPX instance that is used for load balancing the North-South traffic to the microservices in your Kubernetes cluster.

Perform the following:

1.  Download the [citrix-k8s-cpx-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml) using the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml

2.  Deploy the `citrix-k8s-cpx-ingress.yaml` file using the following command:

        kubectl create -f citrix-k8s-cpx-ingress.yaml

3.  Verify if Citrix ingress controller is deployed successfully using the following command:

        kubectl get pods --all-namespaces

### Deploy Citrix ADC CPX with the Citrix ingress controller as sidecar without the default credentials

Earlier, when you deploy Citrix ADC CPX with the Citrix ingress controller as a sidecar without specifying the login credentials, the Citrix ingress controller considers `nsroot/nsroot` as the default credentials.

With the latest Citrix ADC CPX versions (Citrix ADC CPX 13.0.64.35 and later), the default credentials are removed. So, when you deploy the Citrix ingress controller as a sidecar with the latest versions of Citrix ADC CPX, the Citrix ingress controller can get the credentials from Citrix ADC CPX through the `/var/deviceinfo/random_id` file in the Citrix ADC CPX. This file can be shared between the Citrix ADC CPX and the Citrix ingress controller through the volume mount.

Depending on whether you are using the latest Citrix ADC CPX version or an older version, you need to choose one of the following deployment YAML files. For older versions of Citrix ADC CPX, you need to specify the credentials in the YAML file.

- For Citrix ADC CPX 13.0.64.35 and later versions, use the following YAML:

  [citrix-k8s-cpx-ingress.yml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml)

  As provided in the YAML, the following is a snippet of the volume mount configuration required in the YAML file both for the Citrix ingress controller and Citrix ADC CPX:

        volumeMounts:
        - mountPath: /var/deviceinfo
        name: shared-data

  Following is a snippet of the shared volume configuration common for the Citrix ADC CPX and the Citrix ingress controller.

        volumes:
        - name: shared-data
        emptyDir: {}

- For earlier Citrix ADC CPX versions (versions earlier than 13.0.64.35), use the following YAML:

  [cpx-ingress-previous.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/yaml-cpx-crediential-changes/cpx-cic-previous.yaml)

  Following is a snippet of the credential section in the Citrix ingress controller:

        - name: "NS_USER"
        valueFrom:
        secretKeyRef:
                name: nslogin
                key: username
        - name: "NS_PASSWORD"
        valueFrom:
        secretKeyRef:
                name: nslogin
                key: password

## Deploy the Citrix ingress controller for a namespace

In Kubernetes, a role consists of rules that define a set of permissions that can be performed on a set of resources. In an RBAC enabled Kubernetes environment, you can create two kinds of roles based on the scope you need:

- `Role`
- `ClusterRole`

A role can be defined within a namespace with a `Role`, or cluster-wide with a `ClusterRole`. You can create a `Role` to grant access to resources within a single namespace.

In Kubernetes, you can create multiple virtual clusters on the same physical cluster. Namespaces provides a way to divide cluster resources between multiple users and useful in environments with many users spread across multiple teams, or projects.

By default, the Citrix ingress controller monitors Ingress resources across all namespaces in the Kubernetes cluster. If multiple teams want to manage the same Citrix ADC, they can deploy a `Role` based Citrix ingress controller to monitor only ingress resources belongs to a specific namespace. This namespace must be same as the namespace you have provided for creating the service account.
You need to create a Role and bind the role to the service account for the Citrix ingress controller. In this case, the Citrix ingress controller listens only for events from the specified namespace and then configure the Citrix ADC accordingly.

The following example shows a sample YAML file which defines a Role and RoleBinding for deploying a Citrix ingress controller for a specific namespace.

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
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
apiVersion: rbac.authorization.k8s.io/v1
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
