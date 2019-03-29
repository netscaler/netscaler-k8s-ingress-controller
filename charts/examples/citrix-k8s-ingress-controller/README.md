# Citrix Ingress Controller  

[Citrix](https://www.citrix.com) Ingress Controller runs as a pod in Kubernetes cluster and configures the NetScaler VPX/MPX and load balances GuestBook App.


## TL;DR;
``` 
helm install citrix-k8s-ingress-controller --set nsIP= <NSIP>,license.accept=yes,nsVIP=<VIP>
```
## Introduction
This Chart deploys Citrix Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster using [Helm](https://helm.sh) package manager

### Prerequisites
* Kubernetes 1.6+
* Prometheus operator needs to be installed if you want to use exporter along with CIC.

## Installing the Chart

To install the chart with the release name ``` my-release:```

```helm install citrix-k8s-ingress-controller --name my-release --set nsIP= <NSIP>,license.accept=yes,nsVIP=<VIP>,ingressClass[0]=<ingressClassName> ```

If you want to run exporter along with CIC, please install prometheus operator first and then use the following command:

```helm install citrix-k8s-ingress-controller --name my-release --set nsIP=<NSIP>,license.accept=yes,nsVIP=<VIP>,ingressClass=<ingressClassName>,exporter.require=1.0```

If you want to visualize the metrices collected by exporter from Citrix ADC please refer "[Visualization of Metrics](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics)".

The command deploys Citrix Ingress Controller on the Kubernetes cluster in the default configuration. The configuration section lists the parameters that can be configured during installation.
 
## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:
```
helm delete my-release
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
|```loginFileName```| Secret keys for login into NetScaler VPX or MPX Refer Secret Keys|```nslogin```|
|```nsIP```|NetScaler VPX/MPX IP|```x.x.x.x```|
|```nsPort```|Optional:This port is used by Citrix Ingress Controller to communicate with NetScaler. Can use 80 for HTTP |```443```|
|```nsProtocol```|Optional:This protocol is used by Citrix Ingress Controller to communicate with NetScaler. Can use HTTP with nsPort as 80|```HTTPS```|
|```logLevel```|Optional: This is used for controlling the logs generated from Citrix Ingress Controller. options available are CRITICAL ERROR WARNING INFO DEBUG |```DEBUG```|
|```kubernetesURL```| Optional: register for events. If user did not specify it explictly, citrix ingress controller use internal KubeAPIServer IP.|```nil```|
|```nsVIP```| VIP IP |```nil``` 
|```exporter.require```|Exporter to be run as sidecar with CIC|```0```|
|```exporter.image.repository```|Exporter image repository|```quay.io/citrix/netscaler-metrics-exporter```|
|```exporter.image.tag```|Exporter image tag|```v1.0.4 ```|
|```exporter.image.pullPolicy```|Exporter Image Pull Policy|```Always```|
|```exporter.ports.containerPort```|Exporter Container Port|```8888```|
|```ingressClass```| List of name of Ingress Classes |```Citrix```|
> Tip: You can use the default [values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples/citrix-k8s-ingress-controller/values.yaml)

## Route Addition in MPX/VPX

Configure routes for POD reachability

Obtain podCIDR using below options:
``` 
kubectl get nodes -o yaml | grep podCIDR
```
  * podCIDR: 10.244.0.0/24
  * podCIDR: 10.244.1.0/24
  * podCIDR: 10.244.2.0/24

Add Route in Netscaler VPX/MPX

```add route <podCIDR_network> <podCIDR_netmask> <node_HostIP>```

Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which K8S nodes communicate with each other. Usually eth0 IP is from this network).

  Example: 
  * Node1 IP = 10.102.53.101 
  * podCIDR  = 10.244.1.0/24
  * add route 10.244.1.0 255.255.255.0 10.102.53.101
  
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
