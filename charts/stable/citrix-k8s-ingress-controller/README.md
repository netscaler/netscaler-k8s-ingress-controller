# Citrix Ingress Controller  

[Citrix](https://www.citrix.com) Ingress Controller runs as a pod in Kubernetes cluster and configures the NetScaler VPX/MPX.


## TL;DR;
```
helm repo add cic https://citrix.github.io/citrix-k8s-ingress-controller/

helm install cic/citrix-k8s-ingress-controller --set nsIP= <NSIP>,license.accept=yes
```
> Note: "license.accept" is a mandatory argument and should be set to "yes" to accept the terms of the Citrix license.

## Introduction
This Chart deploys Citrix Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster using [Helm](https://helm.sh) package manager

### Prerequisites
* Kubernetes 1.6+
* Helm 2.8.x+
* Prometheus operator needs to be installed if you want to use exporter along with CIC.

## Installing the Chart

Add the Citrix Ingress Controller helm chart repository using command:

```
helm repo add cic https://citrix.github.io/citrix-k8s-ingress-controller/
```

To install the chart with the release name ``` my-release:```


```helm install cic/citrix-k8s-ingress-controller --name my-release --set nsIP= <NSIP>,license.accept=yes,ingressClass[0]=<ingressClassName>```

If you want to run exporter along with CIC, please install prometheus operator first and then use the following command:

```helm install cic/citrix-k8s-ingress-controller --name my-release --set license.accept=yes,ingressClass[0]=<ingressClassName>,exporter.require=1.0```

If you want to visualize the metrices collected by exporter from Citrix ADC please refer "[Visualization of Metrics](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics)".

The command deploys Citrix Ingress Controller on the Kubernetes cluster in the default configuration. The configuration lists the parameters that can be configured during installation.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

```
helm delete --purge my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release

## Configuration

The following table lists the configurable parameters of the Citrix Ingress Controller chart and their default values.

| Parameter |    Description | Default |
| --------- |  ---------------- | ------- |
|```license.accept```|Set to accept to accept the terms of the Citrix license|```no```|
| ``` image.repository ``` | Image Repository|```quay.io/citrix/citrix-k8s-ingress-controller```|
| ``` image.tag```  | Image Tag    |```1.1.1```|
|```  image.pullPolicy```| Image Pull Policy  |```Always```|
|```loginFileName```| Secret keys for login into NetScaler VPX or MPX Refer Secret Keys |```nslogin```|
|```nsIP```|NetScaler VPX/MPX IP|```x.x.x.x```|
|```nsPort```|Optional:This port is used by Citrix Ingress Controller to communicate with NetScaler. Can use 80 for HTTP |```443```|
|```nsProtocol```|Optional:This protocol is used by Citrix Ingress Controller to communicate with NetScaler. Can use HTTP with nsPort as 80|```HTTPS```|
|```logLevel```|Optional: This is used for controlling the logs generated from Citrix Ingress Controller. options available are CRITICAL ERROR WARNING INFO DEBUG |```DEBUG```|
|```kubernetesURL```| Optional: register for events. If user did not specify it explictly, citrix ingress controller use internal KubeAPIServer IP.|```nil```|
|```ingressClass```| List of name of Ingress Classes |```nil```|
|```nodeWatch```| Use for automatic route configuration on NetScaler towards the pod network |```false```|
|```exporter.require```|Exporter to be run as sidecar with CIC|```0```|
|```exporter.image.repository```|Exporter image repository|```quay.io/citrix/netscaler-metrics-exporter```|
|```exporter.image.tag```|Exporter image tag|```v1.0.4 ```|
|```exporter.image.pullPolicy```|Exporter Image Pull Policy|```Always```|
|```exporter.ports.containerPort```|Exporter Container Port|```8888```|

> Tip: You can use the default [values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/stable/citrix-k8s-ingress-controller/values.yaml)

> Note: Please provide frontend-ip (VIP) in your application ingress yaml file. For more info refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/annotations.md)

## Route Addition in MPX/VPX
For seamless functioning of services deployed in the Kubernetes cluster, it is essential that Ingress NetScaler device should be able to reach the underlying overlay network over which Pods are running. 
`feature-node-watch` knob of Citrix Ingress Controller can be used for automatic route configuration on NetScaler towards the pod network. Refer [Network Configuration](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network-config.md) for further details regarding the same.
By default, `feature-node-watch` is false. It needs to be explicitly set to true if auto route configuration is required.

## Secret Keys
To generate secret keys use
``` 
kubectl create secret  generic <filename> --from-literal=username='<username>' --from-literal=password='<password>'
```
The created filename can be passed to values.yaml.

## RBAC
By default the chart will install the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and rolebindings.

## Exporter
[Exporter](https://github.com/citrix/netscaler-metrics-exporter) is running along with the CIC and pulling metrics from the VPX/MPX. It exposes the metrics using Kubernetes NodePort.

## Ingress Class
To know more about Ingress Class refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/ingress-class.md).

## For More Info: https://github.com/citrix/citrix-k8s-ingress-controller

