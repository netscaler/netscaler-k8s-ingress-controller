# Citrix ADC CPX with inbuilt Ingress Controller  

[Citrix](https://www.citrix.com) ADC CPX with the Citrix Ingress Controller running in side-car mode will configure the CPX that runs as pod in Kubernetes cluster and does N-S load balancing of Guestbook app.


## TL;DR;
``` 
git clone https://github.com/citrix/citrix-k8s-ingress-controller.git
cd citrix-k8s-ingress-controller/charts/examples/

helm install citrix-k8s-cpx-ingress-controller --set license.accept=yes
```
> Note: "license.accept" is a mandatory argument and should be set to "yes" to accept the terms of the Citrix license.

## Introduction
This Chart deploys Citrix ADC CPX with inbuilt Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster using [Helm](https://helm.sh) package manager

### Prerequisites
* Kubernetes 1.6+
* Helm 2.8.x+
* Prometheus operator needs to be installed if you want to use exporter along with CIC.

## Installing the Chart

To install the chart with the release name ``` my-release```:

```helm install citrix-k8s-cpx-ingress-controller --name my-release --set license.accept=yes,ingressClass[0]=<ingressClassName>```

To run the exporter as sidecar with CPX, please install prometheus operator first and then use the following command:

```helm install citrix-k8s-cpx-ingress-controller --name my-release --set license.accept=yes,ingressClass=<ingressClassName>,exporter.required=true```

If you want to visualize the metrices collected by exporter from Citrix ADC CPX please refer "[Visualization of Metrics](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics)".

The command deploys Citrix ADC CPX with Citrix Ingress Controller running in side-car mode on the Kubernetes cluster in the default configuration. The configuration section lists the parameters that can be configured during installation.
 
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
|```cpx.image```| CPX Image Repository| ```quay.io/citrix/citrix-k8s-cpx-ingress:13.0-36.29```|
|```cpx.pullPolicy```| CPX Image Pull Policy  | ```Always``` |
|```cic.image```| CIC Image Repository| ```quay.io/citrix/citrix-k8s-ingress-controller:1.5.25```|
|```cic.pullPolicy```| CIC Image Pull Policy  | ```Always``` |
|```cic.required```| CIC to be run as sidecar with Citrix ADC CPX| ```true```|
|```exporter.required```|Exporter to be run as sidecar with Citrix ADC CPX and CIC|```false```|
|```exporter.image```|Exporter image repository|```quay.io/citrix/citrix-adc-metrics-exporter:1.4.0```|
|```exporter.pullPolicy```|Exporter Image Pull Policy|```Always```|
|```exporter.ports.containerPort```|Exporter Container Port|```8888```|
|```ingressClass```| List of name of the Ingress Classes  | ```Citrix``` |

> Tip: You can use the default [values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples/citrix-k8s-cpx-ingress-controller/values.yaml)

## RBAC
By default the chart will install the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and rolebindings.

## Exporter
[Exporter](https://github.com/citrix/citrix-adc-metrics-exporter) is running as sidecar with the CPX and pulling metrics from the CPX. It exposes the metrics using Kubernetes NodePort.

## Ingress Class
To know more about Ingress Class refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/ingress-class.md).

## For More Info: https://github.com/citrix/citrix-k8s-ingress-controller

