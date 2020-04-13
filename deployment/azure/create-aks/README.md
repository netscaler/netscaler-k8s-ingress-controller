# Create a Kubernetes cluster using Azure Kubernetes Engine (AKS)

This guide explains the steps to create a basic Kubernetes cluster in AKS using Azure CLI.
There are two ways to create a AKS cluster:

- Using Kubenet CNI (Basic networking)
- Using Azure CNI (Advanced networking)

#### Prerequisites:

- Make sure Azure CLI (az) is installed with all its dependencies
- Kubectl is installed


## Create a Kubernetes cluster using Kubenet CNI (Basic networking mode in Azure):

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
az aks create --resource-group AKS_RG --name cpx-cluster-basic-1 --node-count 3 --enable-addons monitoring --generate-ssh-keys --kubernetes-version 1.17.3
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
