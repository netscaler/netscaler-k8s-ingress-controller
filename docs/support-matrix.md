# Supported platforms and deployments

This topic provides details about various Kubernetes platforms, deployment topologies, features, and CNIs supported in Cloud-Native deployments that include Citrix ADC and Citrix ingress controller.

## Kubernetes platforms

Citrix ingress controller is supported on the following platforms:

-  Kubernetes v1.10 (and later) on bare metal or self-hosted on public clouds such as, AWS, GCP, or Azure.
-  Google Kubernetes Engine (GKE)
-  Elastic Kubernetes Service (EKS)
-  Azure Kubernetes Service (AKS)
-  Red Hat OpenShift version 3.11 and later
-  Pivotal Container Service (PKS)
-  Diamanti Enterprise Kubernetes Platform

### Latest support information

For Kubernetes:

- Citrix ingress controller supports `v1` version API.

For Istio and Red Hat OpenShift, the following are the latest validated versions:

| Platform | Latest version (validated)|
| ------------------- | -------- |
| Istio service mesh | version 1.11 |
| Red Hat OpenShift   | version 4.8|

## Citrix ADC platforms

The following table lists the Citrix ADC platforms supported by the Citrix ingress controller:

| Citrix ADC Platform | Versions |
| ------------------- | -------- |
| Citrix ADC MPX      | 11.1–61.7 and later |
| Citrix ADC VPX      | 11.1–61.7 and later |
| Citrix ADC CPX      | 12.1–51.16 and later |

## Supported deployment topologies on platforms (on-premises)

The following table lists the various deployment topologies supported by the Citrix ingress controller on the supported Kubernetes (on-premises) platforms:

| Deployment Topologies | Kubernetes | Red Hat OpenShift | PKS |
| --------------------- | ---------- | --------------------------- | ------------------------- |
| [Single-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#single-tier-topology) (Citrix ADC MPX or VPX in tier-1)| Yes | Yes | Yes |
| [Dual-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#dual-tier-topology) (Citrix ADC MPX or VPX in tier-1 and Citrix ADC CPXs in tier-2) | Yes | Yes | Yes |
| [Service mesh lite](deployment-topologies.md#service-mesh-lite) | Yes | Yes | Yes |
| [Services of type LoadBalancer](deployment-topologies.md#services-of-type-loadbalancer) | Yes | Yes | Yes |
| [Services of type NodePort](deployment-topologies.md#services-of-type-nodeport) | Yes | Yes | Yes |

## Supported deployment topologies on cloud platforms

The following table lists the various deployment topologies supported by the Citrix ingress controller on the supported cloud platforms:

| Deployment Topologies | GKE | EKS | AKS (Basic mode - Kubenet) | AKS (Advanced mode - Azure CNI) |
| --------------------- |  --------------------------- | ------------------------- | --------------- | ----------------- |
| Single-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Citrix ADC VPX in tier-1) | Yes | Yes | Yes | Yes | |
| Dual-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Citrix ADC VPX in tier-1 and Citrix ADC CPXs in tier-2) | Yes | No | Yes | Yes |
| Dual-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Cloud LB in tier-1 and Citrix ADC CPXs in tier-2) | Yes | No | Yes | Yes |

## Supported Citrix ingress controller feature on platforms

The following table lists the Citrix ingress controller features supported on various cloud-native platforms:

| Citrix ingress controller features | Kubernetes | Google Cloud  | AWS | Azure | Red Hat OpenShift | PKS |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- | ----------------- | --------------------------------|
| [TCP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [UDP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/certificate-management/tls-certificate-handling/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [TCP over SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/#load-balance-ingress-traffic-based-on-tcp-over-ssl) | Yes | Yes | Yes | Yes | Yes | Yes |
| [HTTP, TCP, or SSL profiles](configure/profiles.md) | Yes | Yes | Yes | Yes | Yes | Yes |
| [NodePort support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/nodeport/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Type LoadBalancer support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/) | Yes | No | Yes | No | Yes | Yes |
| [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Rate limit CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rate-limit/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Auth CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/auth/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Advanced content routing](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/content-routing/)| Yes | Yes | Yes | Yes | Yes | Yes |
| [WAF CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/waf/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Bot CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/bot/) | Yes | Yes | Yes | Yes | Yes | Yes |                   | 
| [OpenShift Routes](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-openshift/) | N/A | N/A | N/A | N/A | Yes | N/A |
| [OpenShift router sharding](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-openshift-sharding/) | N/A | N/A | N/A | N/A | Yes | N/A |
| [Simplified canary using Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/canary/canary/#simplified-canary-deployment-using-ingress-annotations) | Yes | Yes | Yes | Yes | Yes | Yes |  

The following table lists the Citrix ingress controller features supported on the respective Citrix Ingress Controller versions and Citrix ADC versions:

| Citrix ingress controller features | Citrix ingress controller versions | Citrix ADC MPX or VPX versions | Citrix ADC CPX versions |
| --------------------- | --------------------------- |--------------------------------| -------  |
| [TCP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later  |
| [UDP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [TCP over SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later| 12.1–51.16 and later |
| [HTTP, TCP, or SSL profiles](configure/profiles.md) | 1.4.392 | 11.1–61.7 and later| 12.1–51.16 and later |
| [NodePort support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/nodeport/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [Type LoadBalancer support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/) | 1.2.0 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [Rate limit CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rate-limit/) | 1.4.392 | 11.1–61.7 and later | 12.1–51.16 and later |
| [Auth CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/auth/) | 1.4.392 | 11.1–61.7 and later | 12.1–51.16 and later |
|  [Advanced content routing](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/content-routing/)| 1.7.46|   12.1–51.16 and later |  12.1–51.16 and later  |
| [WAF CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/waf/) | 1.9.2 | 13.0–65.4 and later  | 13.0–65.4 and later  |
| [Bot CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/bot/)|1.11.3 |Citrix ADC VPX version 13.0.67.39 and later |Not supported |
| [OpenShift Routes](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-openshift/) | 1.1.3 and later | 12.1–51.16 and later | 13.0–36.28 and later |
| [OpenShift router sharding](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-openshift-sharding/) | 1.2.0 and later | 12.1–51.16 and later | 13.0–36.28 and later |
|[Simplified canary using Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/canary/canary/#simplified-canary-deployment-using-ingress-annotations) | Version 1.13.15 and later | 11.1–61.7 and later | 12.1–51.16 and later|
|[Cross-origin resource sharing policies](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/cors/)|Version 1.17.13 and later | 11.1–61.7 and later | 12.1–51.16 and later|

## Container network interfaces (CNIs) for Citrix ADC CPX

The following table lists the Container network interfaces (CNIs) supported by Citrix ADC CPX:

| Container network interfaces (CNI) | Citrix ADC CPX versions |
| --------------------------------- | ----------------------- |
| Flannel | 12.1–51.16 and later |
| Kubenet | 12.1–51.16 and later |
| Calico | 13.0–36.28 |
| Canal | 13.0–36.28 |
| Calico on GKE | 12.1–51.16 and later |
| OVS | 13.0–36.28 |
| Weave | 12.1–51.16 and later |
| Cilium| 13-0-71-40 and later  |
| OVN | 13.0-79.64 and later|

## Supported container runtime interfaces for Citrix ADC CPX

The following table lists the container runtime interfaces (CRIs) supported by Citrix ADC CPX.

| CRI                    | Supported versions of Citrix ADC CPX|
 ----------------------- | ----------------------- |
| Docker| 11.1 and later |
| [CRI-O](https://cri-o.io)| 13.0–47.103 and later|

## Support matrix for cloud native solution components

The following matrix provides information on compatibility between the different components of the cloud native solution offered by Citrix.

For example, the first row of this table explains the versions of Citrix ADC CPX/VPX/MPX which supports different components of the Citrix cloud native solution. In this table NA is marked if the components are not dependent on each other or when the components are the same.

| Product/component| Citrix ADC CPX/VPX/MPX | Citrix ingress controller| Citrix observability exporter (COE)| Citrix istio adaptor (CIA) | Citrix node controller | ADM agent | ADM service | ADM on-prem | Citrix ADC metrics exporter
| ----------------- |------------- | ------------- |--------------------------- | ------------------------- | --------------- | ----------------- | --------------------------------|--------------------------------|--------------------------------|
| Citrix ADC CPX/VPX/MPX| NA | Citrix ingress controller version 1.1.1 onwards is supported with CPX version 12.1+ onwards and VPX/MPX 11.1+ onwards| COE version 1.0.001 onwards is supported with VPX/MPX/CPX: 13.0 onwards  | CIA version 1.0.0-alpha onwards is supported with CPX/VPX/MPX 12.1+ onwards | CPX/VPX/MPX 12.0 onwards|  CPX/VPX/MPX 13.0–47.22 onwards | CPX/VPX/MPX 13.0–47.22 onwards | CPX/VPX/MPX 11.1 onwards|CPX/VPX/MPX 12.1 onwards  |
| [Citrix ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller) | CPX 12.1+ onwards and VPX/MPX 11.1+ onwards supports Citrix ingress controller version 1.1.1 onwards | NA  | COE version 1.0.001 and onwards is supported with Citrix ingress controller version 1.5.6 onwards  | NA |  NA | NA | NA | NA | NA |
| [Citrix observability exporter (COE)](https://github.com/citrix/citrix-observability-exporter)|    CPX/VPX/MPX 13.0 onwards is supported with COE version 1.0.001 onwards | Citrix ingress controller version 1.5.6 onwards is supported with COE version 1.0.001 onwards  | NA|   CIA version 1.2.0-beta onwards is supported with COE version 1.0.001 onwards   |  NA  | NA | NA | NA | NA |
| [Citrix istio adaptor (CIA)](https://github.com/citrix/citrix-istio-adaptor)| CPX/VPX/MPX 12.1+ onwards is supported with CIA version 1.2.0-beta onwards | NA | COE version 1.0.001 is supported with CIA version 1.2.0-beta onwards| NA |  NA  | NA | NA | NA | NA |
| Citrix node controller| CPX/VPX/MPX 12.0 onwards | NA | NA | NA | NA  | NA | NA | NA | NA|
| ADM agent| CPX/VPX/MPX 13.0–47.22 onwards | NA |NA| NA | NA | NA | NA | NA  | NA|
| ADM service| CPX/VPX/MPX 13.0–47.22 onwards | NA | NA | NA | NA | NA  | NA| NA|NA |
| ADM on-prem| CPX/VPX/MPX 11.1 onwards | NA | NA | NA | NA | NA  | NA| NA| NA|
| Citrix ADC metrics exporter |CPX/VPX/MPX 12.1 onwards |NA | NA| NA | NA | NA | NA| NA  | NA|

**Note:** For better use case coverage, use the latest versions of the components provided in the compatibility table.