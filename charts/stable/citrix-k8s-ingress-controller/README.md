# Citrix Ingress Controller  

[Citrix](https://www.citrix.com/en-in/) provides an Ingress Controller for Citrix ADC MPX (hardware), Citrix ADC VPX (virtualized), and [Citrix ADC CPX](https://docs.citrix.com/en-us/citrix-adc-cpx/13/about.html) (containerized) for [bare metal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments. It configures one or more Citrix ADC based on the Ingress resource configuration in [Kubernetes](https://kubernetes.io/) or in [OpenShift](https://www.openshift.com) cluster.

## TL;DR;

### For Kubernetes
```
   helm repo add cic https://citrix.github.io/citrix-k8s-ingress-controller/

   helm install cic/citrix-k8s-ingress-controller --set nsIP=<NSIP>,license.accept=yes
```

### For OpenShift

```
   helm repo add cic https://citrix.github.io/citrix-k8s-ingress-controller/

   helm install cic/citrix-k8s-ingress-controller --set nsIP=<NSIP>,license.accept=yes,openshift=true
```
> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the Citrix license.

## Introduction
This Helm chart deploys Citrix ingress controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 3.11.x or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version is 2.8.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/charts/Helm_Installation_Kubernetes.md) to install Helm in Kubernetes environment and [here](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/charts/Helm_Installation_OpenShift.md) for OpenShift platform.
-  You determine the NS_IP IP address needed by the controller to communicate with Citrix ADC. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).

-  You have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator), if you want to view the metrics of the Citrix ADC CPX collected by the [metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics).

-  The user name and password of the Citrix ADC VPX or MPX appliance used as the ingress device. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

    You can pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret  generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'
    ```

#### Create system User account for Citrix ingress controller in Citrix ADC

Citrix ingress controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission configure the following on the Citrix ADC:

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

> **Note:**
>
> The system user account would have privileges based on the command policy that you define.

To create the system user account, do the following:

1.  Log on to the Citrix ADC appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.

    2.  Log on to the appliance by using the administrator credentials.

2.  Create the system user account using the following command:

    ```
       add system user <username> <password>
    ```

    For example:

    ```
       add system user cic mypassword
    ```

3.  Create a policy to provide required permissions to the system user account. Use the following command:

    ```
       add cmdpolicy cic-policy ALLOW "(^\S+\s+cs\s+\S+)|(^\S+\s+lb\s+\S+)|(^\S+\s+service\s+\S+)|(^\S+\s+servicegroup\s+\S+)|(^stat\s+system)|(^show\s+ha)|(^\S+\s+ssl\s+certKey)|(^\S+\s+ssl)|(^\S+\s+route)|(^\S+\s+monitor)|(^show\s+ns\s+ip)|(^\S+\s+system\s+file)"
    ```

4.  Bind the policy to the system user account using the following command:

    ```
       bind system user cic cic-policy 0
    ```

## Installing the Chart
Add the Citrix Ingress Controller helm chart repository using command:

```
   helm repo add cic https://citrix.github.io/citrix-k8s-ingress-controller/
```

### For Kubernetes:
#### 1. Citrix Ingress Controller
To install the chart with the release name, `my-release`, use the following command:
```
    helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,ingressClass[0]=<ingressClassName>
```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix ingress controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

#### 2. Citrix Ingress Controller with Exporter
[Metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics) can be deployed along with Citrix ingress controller and collects metrics from the Citrix ADC instances. You can then [visualize these metrics](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/metrics/promotheus-grafana/) using Prometheus Operator and Grafana.

> **Note:**
> Ensure that you have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator).

Use the following command for this:
```
   helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,ingressClass[0]=<ingressClassName>,exporter.required=true
```

### For Openshift:
If Citrix ingress controller needs to be deployed in the OpenShift platform please install Helm and Tiller using instruction given [here](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/charts/Helm_Installation_OpenShift.md). It will make sure Helm and Tiller have the proper permission that is needed to install Citrix ingress controller on OpenShift.

Add the service account named "cic-k8s-role" to the privileged Security Context Constraints of OpenShift:

```
   oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:cic-k8s-role
```

#### 1. Citrix Ingress Controller
To install the chart with the release name, `my-release`, use the following command:
```
   helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,openshift=true
```
The command deploys Citrix ingress controller on your Openshift cluster in the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

#### 2. Citrix Ingress Controller with Exporter
[Metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics) can be deployed along with Citrix ingress controller and collects metrics from the Citrix ADC instances. You can then [visualize these metrics](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/metrics/promotheus-grafana/) using Prometheus Operator and Grafana.

> **Note:**
> Ensure that you have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator)

Use the following command for this:
```
   helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,openshift=true,exporter.required=true
```

### Installed components

The following components are installed:

-  [Citrix ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller)
-  [Exporter](https://github.com/citrix/netscaler-metrics-exporter) (if enabled)

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the CIC end user license agreement. |
| cic.image | Mandatory | `quay.io/citrix/citrix-k8s-ingress-controller:1.1.3` | The CIC image. |
| cic.pullPolicy | Mandatory | Always | The CIC image pull policy. |
| loginFileName | Mandatory | nslogin | The secret key to log on to the Citrix ADC VPX or MPX. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| nsIP | Mandatory | N/A | The IP address of the Citrix ADC device. For details, see [Prerequisites](#prerequistes). |
| nsVIP | Optional | N/A | The Virtual IP address on the Citrix ADC device. |
| nsPort | Optional | 443 | The port used by CIC to communicate with Citrix ADC. You can port 80 for HTTP. |
| nsProtocol | Optional | HTTPS | The protocol used by CIC to communicate with Citrix ADC. You can also use HTTP on port 80. |
| logLevel | Optional | DEBUG | The loglevel to control the logs generated by CIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Logging](/Docs/Logging.md).|
| kubernetesURL | Optional | N/A | The kube-apiserver url that CIC uses to register the events. If the value is not specified, CIC uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
| ingressClass | Optional | N/A | If multiple ingress load balancers are used to load balance different ingress resources. You can use this parameter to specify CIC to configure Citrix ADC associated with specific ingress class. For more information on Ingress class, see [Ingress class support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/ingress-classes/). |
| nodeWatch | Optional | false | Use the argument if you want to automatically configure network route from the Ingress Citrix ADC VPX or MPX to the pods in the Kubernetes cluster. For more information, see [Automatically configure route on the Citrix ADC instance](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/staticrouting/#automatically-configure-route-on-the-citrix-adc-instance).
| exporter.required | Optional | false | Use the argument, if you want to run the [Exporter for Citrix ADC Stats](https://github.com/citrix/netscaler-metrics-exporter) along with CIC to pull metrics for the Citrix ADC VPX or MPX|
| exporter.image    | Optional | `quay.io/citrix/netscaler-metrics-exporter:v1.0.4` | The Exporter image. |
| exporter.pullPolicy | Optional | Always | The Exporter image pull policy. |
| exporter.ports.containerPort | Optional | 8888 | The Exporter container port. |
| openshift | Optional | false | Set this argument if OpenShift environment is being used. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
```
   helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,ingressClass[0]=<ingressClassName> -f values.yaml
```

> **Tip:** 
>
> The [values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/stable/citrix-k8s-cpx-ingress-controller/values.yaml) contains the default values of the parameters.

> **Note:**
> 
> Please provide frontend-ip (VIP) in your application ingress yaml file. For more info refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/annotations.md)

## Route Addition in MPX/VPX
For seamless functioning of services deployed in the Kubernetes cluster, it is essential that Ingress NetScaler device should be able to reach the underlying overlay network over which Pods are running. 
`feature-node-watch` knob of Citrix Ingress Controller can be used for automatic route configuration on NetScaler towards the pod network. Refer [Network Configuration](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network-config.md) for further details regarding the same.
By default, `feature-node-watch` is false. It needs to be explicitly set to true if auto route configuration is required.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

```
   helm delete --purge my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

-  [Citrix ingress controller Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/)
