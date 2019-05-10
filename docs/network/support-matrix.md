# Supported platforms and deployments

This topic provides details about the platforms, Citrix ADC platforms, deployment topologies, features, and CNIs supported in Cloud-Native deployments that include Citrix ADC and Citrix ingress controller.

## Supported platforms

Citrix ingress controller is supported on the following platforms:

-  Kubernetes version 1.?? or later
-  Google Cloud Platform (GCP)
-  Amazon Web Services (AWS)
-  Microsoft Azure
-  Red Hat OpenShift version ?? or later
-  Pivotal Container Service (PKS)
-  Diamanti ?
-  Rancher ?

## Supported Citrix ADC platforms

The following lists the Citrix ADC platforms supported by Citrix ingress controller:

| Citrix ADC Platform | Versions |
| ------------------- | -------- |
| Citrix ADC CPX      | 12.1–51.16 or later |
| Citrix ADC VPX      |   ?  |
| Citrix ADC MPX      |   ?  |
| Citrix ADC SDX      |   ?  |
| Citrix ADC BLX      |   ?  |

## Supported deployment topologies on the platforms

The following table lists the various deployment topologies supported by Citrix ingress controller on the supported cloud-native platforms:

| Deployment Topologies | Kubernetes | Google Cloud Platform (GCP) | Amazon Web Services (AWS) | Microsoft Azure | Red Hat OpenShift | Pivotal Container Service (PKS) |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- | ----------------- | --------------------------------|
| [Single-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#single-tier-topology) (With Citrix ADC MPX or VPX in tier-1)| Yes | Yes | Yes | Yes | Yes |   |
| [Dual-Tier](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#dual-tier-topology) (With Citrix ADC MPX or VPX in tier-1 and Citrix ADC CPXs in tier-2) | Yes | Yes | Yes | Yes | Yes | |
| [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (With Citrix ADC VPX in tier-1) | N/A | Yes | Yes | Yes | Yes | |
| [Cloud](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#cloud-topology) topology (With Citrix ADC VPX in tier-1 and Citrix ADC CPXs in tier-2) | N/A | Yes | Yes | Yes | Yes | |
| [Citrix ADC CPX for east-west traffic](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/#using-the-ingress-adc-for-east-west-traffic) | Yes | Yes | | | | |

## Supported Citrix ingress controller feature on platforms

The following table lists the Citrix ingress controller features supported on various cloud-native platforms:

| Citrix ingress controller features | Kubernetes | Google Cloud Platform (GCP) | Amazon Web Services (AWS) | Microsoft Azure | Red Hat OpenShift | Pivotal Container Service (PKS) |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- | ----------------- | --------------------------------|
| TCP Ingress | Yes | Yes | Yes | Yes | Yes | Need info |
| SSL Ingress | Yes | Yes | Yes | Yes | Yes | Need info |
| TCP over SSL Ingress | Yes | Yes | Yes | Yes | Yes | Need info |
| [Annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/) | Yes | Yes | Yes | Yes | Yes | Need info |
| [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) | Yes | Yes | Yes | Yes | Yes | Need info |
| Routes | N/A | N/A | N/A | N/A | Yes | Need info |

## Supported container network interface for Citrix ADC CPX

The following table lists the Container Network Interface (CNI) supported by Citrix ADC CPX:

| Container Network Interface (CNI) | Citrix ADC CPX versions |
| --------------------------------- | ----------------------- |
| Flannel | 12.1–51.16 or later |
| Kubenet | 12.1–51.16 or later |
| Calico (With 32-bit mask) | 13.0 (preview) |
| Calico (with normal mask) | 12.1–51.16 or later |
| OVS | 13.0 (preview) |
| AWS CNI | 13.0 (preview) |
| Azure CNI | need info |
| Weave | need info |
| Contiv | need info |
