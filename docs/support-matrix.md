# Supported platforms and deployments

This topic provides details about various Kubernetes platforms, deployment topologies, features, and CNIs supported in Cloud-Native deployments that include Citrix ADC and Citrix ingress controller.

## Kubernetes platforms

Citrix ingress controller is supported on the following platforms:

-  Kubernetes v1.10 on bare metal or self-hosted on public clouds such as, AWS, GCP, or Azure.
-  Google Kubernetes Engine (GKE)
-  Elastic Kubernetes Service (EKS)
-  Azure Kubernetes Service (AKS)
-  Red Hat OpenShift version 3.11 and later
-  Pivotal Container Service (PKS)
-  Diamanti Enterprise Kubernetes Platform

## Citrix ADC platforms

The following table lists the Citrix ADC platforms supported by Citrix ingress controller:

| Citrix ADC Platform | Versions |
| ------------------- | -------- |
| Citrix ADC MPX      | 11.1–61.7 and later |
| Citrix ADC VPX      | 11.1–61.7 and later |
| Citrix ADC CPX      | 12.1–51.16 and later |

## Supported deployment topologies on platforms (on-premises)

The following table lists the various deployment topologies supported by Citrix ingress controller on the supported Kubernetes (on-premises) platforms:

| Deployment Topologies | Kubernetes | Red Hat OpenShift | PKS |
| --------------------- | ---------- | --------------------------- | ------------------------- |
| [Single-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#single-tier-topology) (Citrix ADC MPX or VPX in tier-1)| Yes | Yes | Yes |
| [Dual-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#dual-tier-topology) (Citrix ADC MPX or VPX in tier-1 and Citrix ADC CPXs in tier-2) | Yes | Yes | Yes |
| Citrix ADC CPX for [east-west traffic (service mesh-lite)](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#using-the-ingress-adc-for-east-west-traffic) | Yes | Yes | Yes |

## Supported deployment topologies on cloud platforms

The following table lists the various deployment topologies supported by Citrix ingress controller on the supported cloud platforms:

| Deployment Topologies | GKE | EKS | AKS (Basic mode - Kubenet) | AKS (Advanced mode - Azure CNI) |
| --------------------- |  --------------------------- | ------------------------- | --------------- | ----------------- |
| Single-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Citrix ADC VPX in tier-1) | Yes | Yes | Yes | No | |
| Dual-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Citrix ADC VPX in tier-1 and Citrix ADC CPXs in tier-2) | Yes | No | Yes | No |
| Dual-Tier [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (Cloud LB in tier-1 and Citrix ADC CPXs in tier-2) | Yes | No | Yes | No |

## Supported Citrix ingress controller feature on platforms

The following table lists the Citrix ingress controller features supported on various cloud-native platforms:

| Citrix ingress controller features | Kubernetes | GKE | EKS | AKS | Red Hat OpenShift | PKS |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- | ----------------- | --------------------------------|
| [TCP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [UDP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/certificate-management/tls-certificate-handling/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [TCP over SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/#load-balance-ingress-traffic-based-on-tcp-over-ssl) | Yes | Yes | Yes | Yes | Yes | Yes |
| [HTTP, TCP, or SSL profiles](configure/profiles.md) | Yes | Yes | Yes | Yes | Yes | Yes |
| [NodePort support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/nodeport/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Type LoadBalancer support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) | Yes | Yes | Yes | Yes | Yes | Yes |
| [OpenShift Routes](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-openshift/) | N/A | N/A | N/A | N/A | Yes | N/A |
| [OpenShift router sharding](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-openshift-sharding/) | N/A | N/A | N/A | N/A | Yes | N/A |

The following table lists the Citrix ingress controller features supported on respective Citrix Ingress Controller version and Citrix ADC versions:

| Citrix ingress controller features | Citrix ingress controller versions | Citrix ADC MPX or VPX versions | Citrix ADC CPX versions |
| --------------------- | --------------------------- |--------------------------------| -------  |
| [TCP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later  |
| [UDP Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [TCP over SSL Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-udp-ingress/) | 1.1.1 and later | 11.1–61.7 and later| 12.1–51.16 and later |
| [HTTP, TCP, or SSL profiles](configure/profiles.md) | 1.3.0 | 11.1–61.7 and later| 12.1–51.16 and later |
| [NodePort support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/nodeport/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [Type LoadBalancer support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/) | 1.2.0 | 11.1–61.7 and later | 12.1–51.16 and later |
| [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) | 1.1.1 and later | 11.1–61.7 and later | 12.1–51.16 and later |
| [OpenShift Routes](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-openshift/) | 1.1.3 and later | 12.1–51.16 and later | 13.0–36.28 |
| [OpenShift router sharding](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-openshift-sharding/) | 1.2.0 | 12.1–51.16 and later | 13.0–36.28 |

## Container network interface (CNI) for Citrix ADC CPX

The following table lists the Container Network Interface (CNI) supported by Citrix ADC CPX:

| Container Network Interface (CNI) | Citrix ADC CPX versions |
| --------------------------------- | ----------------------- |
| Flannel | 12.1–51.16 and later |
| Kubenet | 12.1–51.16 and later |
| Calico | 13.0–36.28 |
| Calico on GKE | 12.1–51.16 and later |
| OVS | 13.0–36.28 |
| Weave | 12.1–51.16 and later |
