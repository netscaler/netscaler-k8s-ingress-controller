# Deployment Architecture

The common deployment architectures emerging in K8s environment are of single Tier and Dual Tier load balancing.
Citrix ADC with Ingress Controller provides solution for these deployments. Citrix Ingress Controller(CIC) automates the configuration of CITRIX ADC loadbalancing microservices in Kubernetes environment.


**North-South traffic Loadbalancing**: North/South traffic is the traffic heading in and out of your Kubernetes Cluster. It is the traffic that comes from the client and hits the frontend microservices. 

**East-West traffic Loadbalancing**: East/West traffic is the traffic from one microservice to another inside the Kubernetes Cluster. 

In usual k8s environment the E-W traffic is load balanced by kube-proxy and N-S traffic is load balanced by Ingress load balancer like Citrix ADC. 

The E-W traffic can also be load balanced by Ingress load balancer with E-W Hairpin mode.

1. [Single Tier Topology](../docs/single-tier-topology.md)
2. [Dual Tier Topology](../docs/dual-tier-topology.md)
3. [Dual Tier Topology with Hairpin E-W](../docs/dual-tier-topology-with-hairpin-E-W.md)

# Citrix Ingress Controller Features

1.  [Ingress Class](../docs/ingress-class.md)
2.  [Annotations](../docs/annotations.md)
3.  [Smart Annotations](../docs/smart-annotations.md)
4.  [Network Supports](../docs/network-config.md)
5.  [Automated Certificate Management with cert-manager](../docs/certificate.md)

# Deployment Solutions

1.  [On-Prem](baremetal)
2.  [Google Cloud](gcp/README.md)
3.  [Azure Cloud](azure/README.md)
