# Dual Tier Topology

In Dual Tier deployment mode the Tier-1 Citrix ADC load balances the  Tier-2 Citrix ADCs(CPX) and CPX load balances the frontend microservices.
Citrix Ingress Controller automates the configuration of Citrix ADC(VPX/MPX) with the help of Ingress resources which exposes these microservices.
CPX has inbuilt controller that configures the CPX based upon the Ingress config.

![dual-tier-topology](../Images/dual-tier-topology.png)
