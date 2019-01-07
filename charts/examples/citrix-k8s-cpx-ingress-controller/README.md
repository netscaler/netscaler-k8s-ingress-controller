# Citrix ADC CPX with inbuilt Ingress Controller  

[Citrix](https://www.citrix.com) ADC CPX with a builtin Ingress Controller agent will configure the CPX that runs as pod in Kubernetes cluster and does N-S load balancing of Guestbook app.


## TL;DR;
``` 
helm install citrix-k8s-cpx-ingress-controller --set license.accept=yes,ingressClass=<ingressClassName>
```
## Introduction
This Chart deploys Citrix ADC CPX with inbuilt Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster using [Helm](https://helm.sh) package manager

### Prerequisites
* Kubernetes 1.6+

## Installing the Chart

To install the chart with the release name ``` my-release```:

```helm install citrix-k8s-cpx-ingress-controller --name my-release --set license.accept=yes,ingressClass=<ingressClassName>```

To run the exporter as sidecar with CPX

```helm install citrix-k8s-cpx-ingress-controller --name my-release --set license.accept=yes,ingressClass=<ingressClassName>,exporter.require=1.0```

The command deploys Citrix ADC CPX with in built ingress controller on the Kubernetes cluster in the default configuration. The configuration section lists the parameters that can be configured during installation.
 
## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:
```
helm delete my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release

## Configuration
The following table lists the configurable parameters of the CPX with inBuilt Ingress Controller chart and their default values.

| Parameter | Description | Default |
| --------- | ----------- | ------- |
|```license.accept```|Set to accept to accept the terms of the Citrix license| ```no``` |
| ``` image.repository ``` | Image Repository| ```us.gcr.io/citrix-217108/citrix-k8s-cpx-ingress```|
| ``` image.tag``` | Image Tag| ```latest``` |
|```  image.pullPolicy```| Image Pull Policy  | ```Always``` |
|```exporter.require```|Exporter to be run as sidecar with CIC|```0```|
|```exporter.image.repository```|Exporter image repository|```quay.io/citrix/netscaler-metrics-exporter```|
|```exporter.image.tag```|Exporter image tag|```v1.0.0 ```|
|```exporter.image.pullPolicy```|Exporter Image Pull Policy|```Always```|
|```exporter.ports.containerPort```|Exporter Container Port|```8888```|
|```ingressClass```| Name of the Ingress Class  | ```Citrix``` |

> Tip: You can use the default [values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples/citrix-k8s-cpx-ingress-controller/values.yaml)

## RBAC
By default the chart will install the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and rolebindings.

## Exporter
[Exporter](https://github.com/citrix/netscaler-metrics-exporter) is running as sidecar with the CPX and pulling metrics from the CPX. It exposes the metrics using Kubernetes NodePort.

## Ingress Class
To know more about Ingress Class refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/ingress-class.md).

## For More Info: https://github.com/citrix/citrix-k8s-ingress-controller

