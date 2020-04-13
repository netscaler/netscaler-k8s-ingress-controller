# Deployment solutions in Azure Kubernetes Engine

Azure Kubernetes Engine (AKS) provides the following two modes for networking:

-  [Kubenet (basic) networking](https://docs.microsoft.com/en-us/azure/aks/concepts-network#kubenet-basic-networking)
-  [Azure CNI (advanced) networking](https://docs.microsoft.com/en-us/azure/aks/concepts-network#azure-cni-advanced-networking)

## Citrix ADC CPX as an Ingress in Azure Kubernetes Engine

You can deploy Citrix ADC CPX as an Ingress in AKS using these modes. For detailed instructions, refer:

-  [Deploy Citrix ADC CPX as an Ingress device in an Azure Kubernetes Service cluster](../../docs/deploy/deploy-azure.md).
-  [Deploy Citrix ADC CPX as an Ingress device in an Azure Kubernetes Service cluster with advanced networking mode](../../docs/deploy/deploy-azure-cni.md)

## Citrix Ingress Controller in Azure Kubernetes Engine with Citrix ADX VPX

You can deploy Citrix Ingress Controller in AKS with Citrix ADC VPX. For detailed instructions, refer:
-  [Deploy Citrix Ingress Controller with Citrix ADC VPX in an Azure Kubernetes Service cluster](../../docs/deploy/deploy-azure-cic.md).

