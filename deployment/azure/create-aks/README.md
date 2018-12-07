# Create a Kubernetes cluster using Azure Kubernetes Engine (AKS)

This guide explains the steps to create a basic Kubernetes cluster in AKS using Azure CLI.
There are two ways to create a AKS cluster

- Using Kubenet networking (Basic)
- Using Azure CNI networking (Advanced)

This guide provides commands to create a Kubernetes cluster using both the ways

#### Prerequisites:

Make sure Azure CLI (az) is installed with all its dependencies
Kubectl is installed


## Create a Kubernetes cluster using Kubenet networking (Basic mode in Azure):

#### Steps:

Login to your Azure Account.

```
az login
```

Set the Azure Subscription that you are going to use for the deployment.

The previous command would return a list of subscriptions. You can choose one from that.

```
az account set --subscription "<name of the subscription>"
```

Create an Azure Resource Group for AKS

```
az group create --name AKS_RG --location southindia
```

Create an Kubernetes cluster with just 1 node using AKS

```
az aks create --resource-group AKS_RG --name cpx-cluster-basic-1 --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

Login to the created Kubernetes cluster.

```
az aks get-credentials --resource-group AKS_RG --name cpx-cluster-basic-1
```

Now the kubectl config should be updated with this newly created cluster details.

kubectl commands should now work on the cluster.

```
kubectl get nodes
kubectl get pods
```

## Create a Kubernetes cluster using Azure CNI networking (Advanced mode in Azure):

#### Steps:

Create a Resource Group

```
az group create --name AKS_RG --location southindia
```

Create a VNET and a subnet in that resource Group or in any existing resource group

```
az network vnet create -g AKS_RG -n azurecni_vnet1 --address-prefix 20.0.0.0/8 --subnet-name subnet1 --subnet-prefix 20.0.0.0/16
```

Get the subnet resource ID from the vnet and store in a variable

```
subnet_id=$(az network vnet subnet list --resource-group AKS_RG --vnet-name azurecni_vnet1 --query [].id --output tsv)

#Print the captured subnet_id
echo $subnet_id
/subscriptions/<subscription_ID>/resourceGroups/AKS_RG/providers/Microsoft.Network/virtualNetworks/azurecni_vnet1/subnets/subnet1
```

Create a cluster in AKS using Azure CNI

```
az aks create --resource-group AKS_RG --name cpx-cluster-azurecni-1 --network-plugin azure --vnet-subnet-id $subnet_id --docker-bridge-address 172.17.0.1/16 --dns-service-ip 10.2.0.10 --service-cidr 10.2.0.0/24
```
