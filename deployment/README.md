# Deployment architecture

The common deployment architectures emerging in K8s environment are of single-tier and dual-tier load balancing.

Citrix ADC with Ingress Controller provides solution for these deployments. The Citrix ingress controller automates the configuration of Citrix ADC load balancing microservices in Kubernetes environment.

**North-South traffic Load balancing**: North-South traffic is the traffic heading in and out of your Kubernetes Cluster. It is the traffic that comes from the client and hits the frontend microservices.

**East-West traffic Load balancing**: East-West traffic is the traffic from one microservice to another inside the Kubernetes Cluster.

In usual k8s environment the E-W traffic is load balanced by kube-proxy and N-S traffic is load balanced by Ingress load balancer like Citrix ADC.

The E-W traffic can also be load balanced by Ingress load balancer with E-W Hairpin mode.

-  [Single Tier Topology](../docs/deployment-topologies.md#single-tier-topology)
-  [Dual Tier Topology](../docs/deployment-topologies.md#dual-tier-topology)
-  [Cloud Topology](../docs/deployment-topologies.md#cloud-topology)
-  [Using the Ingress ADC for East-West traffic](../docs/deployment-topologies.md#using-the-ingress-adc-for-east--west-traffic)

## Citrix ingress controller features

1.  [Ingress Class](../docs/configure/ingress-classes.md)
1.  [TCP Ingress](../docs/how-to/tcp-udp-ingress.md)
1.  [Annotations](../docs/configure/annotations.md)
1.  [Smart Annotations](../docs/configure/annotations.md)
1.  [Network Supports](../docs/network/staticrouting.md)
1.  [Automated Certificate Management with cert-manager](../docs/certificate-management/certificate.md)
1.  [TLS Certificate Handling](../docs/certificate-management/tls-certificate-handling.md)
1.  [Rewrite and Responder Policy Support using CRD](../docs/crds/rewrite-responder.md)

## Deployment solutions

1.  [On-Prem](baremetal)
1.  [Google Cloud](../docs/deploy/deploy-gcp.md)
1.  [Azure Cloud](../docs/deploy/deploy-azure.md)
1.  [Rancher managed Kubernetes cluster](../docs/deploy/deploy-cic-rancher.md)
