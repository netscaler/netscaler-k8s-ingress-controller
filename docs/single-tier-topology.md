# Single Tier Topology

In Single Tier deployment mode the Tier-1 Citrix ADC directly load balances the frontend microservice applications.
Citrix ingress Controller automates the configuration of CITRIX ADC(VPX/MPX) with the help of ingress which exposes these applications.
Citrix Ingress Controller is deployed as a deployment in kubernetes cluster and manages the configuration of Tier-1 Citrix ADC(VPX/MPX).
Citrix Ingress Controller provides features like SSL Offload, Fine-Tuning CS/LB Vserver configuration with the help of annotations.

![Single Tier Topology](../Images/single-tier-topology.png)
