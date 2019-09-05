# Deploy the Citrix ingress controller on a PKS managed Kubernetes cluster

[Pivotal Container Service (PKS)](https://pivotal.io/platform/pivotal-container-service) enables operators to provision, operate, and manage enterprise-grade Kubernetes clusters using BOSH and Pivotal Ops Manager.

The [Citrix ingress controller](/docs/index.md) is built around the Kubernetes [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) and it can automatically configure one or more Citrix ADCs based on the Ingress resource configuration. You can deploy the Citrix ingress controller in a PKS managed Kubernetes cluster to extend the advanced load balancing and traffic management capabilities of Citrix ADC to your cluster.

## Prerequisites

Before creating the Kubernetes cluster using PKS. Make sure that for all the plans available on the Pivotal Ops Manager, the following options are set:

-  Enable Privileged Containers
-  Disable DenyEscalatingExec

For detailed information on PKS Framework and other documentation, see [Pivotal Container Service documentation](https://docs.pivotal.io/pks/1-3/index.html).

After you have set the required options, create a Kubernetes cluster using the PKS CLI framework and set the context for the created cluster.

## Deployment options

 You can either deploy Citrix ADC CPXs as pods inside the cluster or deploy a Citrix ADC MPX or VPX appliance outside the Kubernetes cluster.

Based on how you want to use Citrix ADC, there are two ways to deploy the Citrix ingress controller in a Kubernetes cluster on the Rancher platform:

-  As a sidecar container alongside Citrix ADC CPX in the same pod: In this mode, Citrix ingress controller configures the Citrix ADC CPX.
  
-  As a standalone pod in the Kubernetes cluster: In this mode, you can control the Citrix ADC MPX or VPX appliance deployed outside the cluster.

## Deploy Citrix ingress controller as a pod

Follow the instruction provided in topic: [Deploy Citrix ingress controller as a standalone pod in the Kubernetes cluster for Citrix ADC MPX or VPX appliances](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/#deploy-citrix-ingress-controller-as-a-standalone-pod-in-the-kubernetes-cluster-for-citrix-adc-mpx-or-vpx-appliances).

## Deploy Citrix ingress controller as a sidecar with Citrix ADC CPX

Follow the instruction provided in topic: [Deploy Citrix ingress controller as a sidecar with Citrix ADC CPX](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/#deploy-citrix-ingress-controller-as-a-sidecar-with-citrix-adc-cpx).

## Network Configuration

For seamless functioning of the services deployed in the Kubernetes cluster, it is essential that Ingress Citrix ADC device should be able to reach the underlying overlay network over which Pods are running. The Citrix ingress controller allows you to configure network connectivity between the Citrix ADC device and service using [Static Routing](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/staticrouting/), [Citrix node controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/node-controller/), [services of type NodePort](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/nodeport/), or [services of type LoadBalancer](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).
