# What is Citrix Ingress Controller?

Citrix provides an Ingress Controller to Citrix ADC MPX (hardware), Citrix ADC VPX (virtualized), and Citrix ADC CPX (containerized) for [bare metal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments. It is built around Kubernetes [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) and automatically configures one or more Citrix ADC based on the Ingress resource configuration.

Clients outside a Kubernetes cluster need a way to access the services provided by pods inside the cluster. For services that provide HTTP(s) access, this access is provided through a [layer-7 proxy](https://en.wikipedia.org/wiki/Proxy_server#Reverse_proxies) also known as Application Delivery Controller (ADC) device or a load balancer device. Kubernetes provides an API object, called [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) that defines rules on how clients access services in a Kubernetes cluster. Service owners create these [Ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/#the-ingress-resource) that define rules for directing HTTP(s) traffic. An [Ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers) watches the Kubernetes API server for updates to the Ingress resource and accordingly reconfigures the Ingress ADC.

Citrix Ingress Controller (CIC) supports topologies and traffic management beyond standard HTTP(s) Ingress. Citrix ADCs with Citrix Ingress Controllers support [Single-Tier](deployment-topologies.md#single-tier-topology) and [Dual-Tier](deployment-topologies.md#dual-tier-topology) traffic load balancing. The service owners can also control ingress TCP/TLS and UDP traffic.

Citrix Ingress Controller automates the configuration of Citrix ADCs to proxy traffic into (*North-South*) and between (*East-West*) the microservices in a Kubernetes cluster. The North-South traffic refers to the traffic from clients outside the cluster to microservices in the Kubernetes cluster. The East-West traffic refers to the traffic between the microservices inside the Kubernetes cluster.

Typically, North-South traffic is load balanced by Ingress devices such as Citrix ADCs while East-West traffic is load balanced by [kube-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy). Since kube-proxy only provides limited layer-4 load balancing, service owners can utilize the Citrix Ingress Controller to achieve sophisticated layer-7 controls for [East-West traffic using the Ingress CPX ADCs](deployment-topologies.md#dual-tier-topology-with-hairpin-e-w-mode).

## Deploying Citrix Ingress Controller

You can deploy Citrix Ingress Controller in the following deployment modes:

1.  As a standalone pod. This mode is used when managing ADCs such as, Citrix ADC MPX or VPX that are outside the Kubernetes cluster.

1.  As a sidecar in a pod along with the Citrix ADC CPX in the same pod. The controller is only responsible for the Citrix ADC CPX that resides in the same pod.

You can deploy Citrix Ingress Controller using Kubernetes YAML or Helm charts. For more information, see [Deploying Citrix Ingress Controller using YAML](deploy/deploy-cic-yaml.md) or [Deploying Citrix Ingress Controller using Helm charts](deploy/deploy-cic-helm.md).
