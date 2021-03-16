
# Overview

## What is an Ingress controller in Kubernetes

When you are running an application inside a Kubernetes cluster, you need to provide a way for external users to access the applications from outside the Kubernetes cluster. Kubernetes provides an object called [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) which allows you to define the rules for accessing the services with in the Kubernetes cluster. It provides the most effective way to externally access multiple services running inside the cluster using a stable IP address.

An Ingress controller is an application deployed inside the cluster that interprets rules defined in the Ingress. The Ingress controller converts the Ingress rules into configuration instructions for a load balancing application integrated with the cluster. The load balancer can be a software application running inside your Kubernetes cluster or a hardware appliance running outside the cluster.

## What is Citrix ADC ingress controller

Citrix provides an implementation of the [Kubernetes Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers) to manage and route traffic into your Kubernetes cluster using Citrix ADCs (Citrix ADC CPX, VPX, or MPX).

Using Citrix ADC ingress controller, you can configure Citrix ADC CPX, VPX, or MPX according to the Ingress rules and integrate your Citrix ADCs with the Kubernetes environment.

## Why Citrix ADC ingress controller

This topic provides information about some of the key benefits of integrating Citrix ADCs with your Kubernetes cluster using Citrix ADC ingress controller.

### Support for TCP and UDP traffic

Standard Kubernetes Ingress solutions provide load balancing only at layer 7 (HTTP or HTTPS traffic). Some times, you need to expose many legacy applications which rely on TCP or UDP applications and need a way to load balance those applications. Citrix Kubernetes Ingress solution using Citrix ADC ingress controller provides TCP, TCP-SSL, and UDP traffic support apart from the standard HTTP or HTTPS Ingress. Also, it works seamlessly across multiple clouds or on-premises data centers.

### Advanced traffic management policies

Citrix ADC provides enterprise-grade traffic management policies like rewrite and responder policies for efficiently load balancing traffic at layer 7. However, Kubernetes Ingress lacks such enterprise-grade traffic management policies. With the Kubernetes Ingress solution from Citrix, you can apply rewrite and responder policies for application traffic in a Kubernetes environment using CRDs provided by Citrix.

### Flexible deployment topologies

Citrix provides flexible and powerful topologies such as [Single-Tier](deployment-topologies.md#single-tier-topology) and [Dual-Tier](deployment-topologies.md#dual-tier-topology) depending on how you want to manage your Citrix ADCs and Kubernetes environment. For more information on the deployment topologies, see the
[Deployment topologies](deployment-topologies.md) page.

### Layer 7 load balancing support for East-West traffic

For traffic between microservices inside the Kubernetes cluster (East-West traffic), Kubernetes natively provides only limited layer 4 load balancing. Using Citrix ADC CPX along with the Ingress controller, you can achieve advanced layer 7 load balancing for East-West traffic.

### Service of type LoadBalancer on bare metal clusters

There may be several situations where you want to deploy your Kubernetes cluster on bare metal or on-premises rather than deploy it on public cloud. When you are running your applications on bare metal Kubernetes clusters, it is much easier to route TCP or UDP traffic using a service of type `LoadBalancer` than using Ingress. Even for HTTP traffic, it is sometimes more convenient than Ingress. However, there is no load balancer implementation natively available for bare metal Kubernetes clusters. Citrix provides a way to load balance such services using the Ingress controller and Citrix ADC. For more information, see [Expose services of type LoadBalancer](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).

## Deploy Citrix ADC ingress controller

You can deploy Citrix ADC ingress controller in the following deployment modes:

1. As a standalone pod: This mode is used when managing ADCs such as Citrix ADC MPX, or VPX that is outside the Kubernetes cluster.

1. As a sidecar in a pod along with the Citrix ADC CPX in the same pod. The controller is only responsible for the Citrix ADC CPX that resides in the same pod.

You can deploy the ingress controller provided by Citrix using Kubernetes YAML or Helm charts. For more information, see [Deploy Citrix ADC ingress controller using YAML](deploy/deploy-cic-yaml.md) or [Deploy Citrix ADC ingress controller using Helm charts](deploy/deploy-cic-helm.md).
