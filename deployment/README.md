# Deployment Architecture

The common deployment architectures emerging in K8s environment are of single Tier and Dual Tier load balancing.

Citrix ADC with Ingress Controller provides solution for these deployments. Citrix Ingress Controller(CIC) automates the configuration of CITRIX ADC loadbalancing microservices in Kubernetes environment.

**North-South traffic Load balancing**: North/South traffic is the traffic heading in and out of your Kubernetes Cluster. It is the traffic that comes from the client and hits the frontend microservices.

**East-West traffic Load balancing**: East/West traffic is the traffic from one microservice to another inside the Kubernetes Cluster.

In usual k8s environment the E-W traffic is load balanced by kube-proxy and N-S traffic is load balanced by Ingress load balancer like Citrix ADC.

The E-W traffic can also be load balanced by Ingress load balancer with E-W Hairpin mode.

-  [Single Tier Topology](../docs/deployment-topologies.md#single-tier-topology)
-  [Dual Tier Topology](../docs/deployment-topologies.md#dual-tier-topology)
-  [Cloud Topology](../docs/deployment-topologies.md#cloud-topology)
-  [Using the Ingress ADC for East-West traffic](../docs/deployment-topologies.md#using-the-ingress-adc-for-east-west-traffic)

## Citrix Ingress Controller Features

1.  [Ingress Class](../docs/configure/ingress-classes.md)
2.  [Annotations](../docs/configure/annotations.md)
3.  [Smart Annotations](../docs/configure/annotations.md))
4.  [Network Supports](../docs/network/staticrouting.md)
5.  [Automated Certificate Management with cert-manager](../docs/certificate-management/certificate.md)
6.  [TLS Certificate Handling](../docs/certificate-management/tls-certificate-handling.md)
7.  [Rewrite and Responder Policy Support using CRD](../docs/crds/rewrite-responder.md)

## Deployment Solutions

1.  [On-Prem](baremetal)
2.  [Google Cloud](../docs/deploy/deploy-gcp.md)
3.  [Azure Cloud](../docs/deploy/deploy-azure.md)
