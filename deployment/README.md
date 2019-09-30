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
-  [Service Mesh Lite](../docs/deploy/service-mesh-lite.md)

## Citrix ingress controller features

-  [Ingress Class](../docs/configure/ingress-classes.md)
-  [Ingress Configuration](../docs/configure/ingress-config.md)
-  [TCP Ingress](../docs/how-to/tcp-udp-ingress.md)
-  [Annotations](../docs/configure/annotations.md)
    -  [Smart Annotations](../docs/configure/annotations.md)
-  Network configuration:
    -  [Static routing](../docs/network/staticrouting.md)
    -  [Establish network between K8s nodes and Ingress Citrix ADC using Citrix node controller](../docs/network/node-controller.md)
    -  [Expose services using NodePort](../docs/network/nodeport.md)
    -  [Expose services using LoadBalancer](../docs/network/type_loadbalancer.md)
-  [Automated Certificate Management with cert-manager](../docs/certificate-management/certificate.md)
-  [HTTP, TCP, or SSL Profiles support](../docs/configure/profiles.md)
-  [TLS Certificate Handling](../docs/certificate-management/tls-certificates.md)
-  [Rewrite and Responder](../docs/crds/rewrite-responder.md)
-  [Canary deployment support](../docs/canary/canary.md)
-  [OpenShift router plug-in](../docs/deploy/deploy-cic-openshift.md)
-  [Openshift router sharding support](../docs/deploy/deploy-openshift-sharding.md)

## Deployment solutions

1.  [On-Prem](baremetal)
1.  [Google Cloud](../docs/deploy/deploy-gcp.md)
1.  [Azure Cloud](../docs/deploy/deploy-azure.md)
1.  [Rancher managed Kubernetes cluster](../docs/deploy/deploy-cic-rancher.md)
1.  [Pivotal Container Service (PKS)](../docs/deploy/deploy-pks.md)

## Use cases

-  [Securing ingress](../docs/how-to/secure-ingress.md)
-  [TCP and HTTP use cases](../docs/how-to/tcp-use-cases.md)  
-  [Load balance Ingress traffic to TCP or UDP based application](../docs/how-to/tcp-udp-ingress.md)
-  [Set up dual-tier deployment](../docs/how-to/deploy-cic-dual-tier.md)
