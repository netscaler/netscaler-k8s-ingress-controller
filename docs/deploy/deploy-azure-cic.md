# Deploy Citrix Ingress Controller in AKS with Citrix ADC VPX

This topic explains how to deploy Citrix Ingress Controller with Citrix ADC VPX in an [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-in/services/kubernetes-service/) cluster. You can also configure the Kubernetes cluster on [Azure VMs](https://azure.microsoft.com/en-in/services/virtual-machines/) and then deploy Citrix Ingress Controller with VPX.

The procedure to deploy for both AKS and Azure VM is the same. However, if you are configuring Kubernetes on Azure VMs you need to deploy the CNI plug-in for the Kubernetes cluster.


## Pre-requisites:

You should complete the following tasks before performing the steps in the procedure.

-  Ensure that you have a Kubernetes cluster up and running.

!!! note "Note"
    For more information on creating a Kubernetes cluster in AKS, see [Guide to create an AKS cluster](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/create-aks/README.md).


## Topology:

![](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/media/singletopology.png)

## Create a Citrix ADC VPX instance from Azure Marketplace

Create a Citrix ADC VPX from the Azure Marketplace. 
For more information on how to create a VPX, see [Get Citrix ADC VPX on Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-vpx.md).


## Create a Citrix Ingress Controller Image URL on Azure

To deploy CIC, an image registry should be created on Azure and the correponding image URL should be used to fetch the CIC image.
For more information on how to create registery and get image URL, see [Get Citrix Ingress Controller Image URL on Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-cic-url.md)

Once registry is created, the CIC registry name should be attched to the aks cluster used for deployment.
```
az aks update -n <cluster-name> -g <resource-group-where-aks-deployed> --attach-acr <cic-registry>
```

## Deploy Citrix Ingress Controller


#### Create Citrix ADC VPX login credentials using Kubernetes secret

```
kubectl create secret  generic nslogin --from-literal=username='<azure-vpx-instance-username>' --from-literal=password='<azure-vpx-instance-password>'
```

The Citrix ADC VPX username and password should be same as the (username, password) set while creating VPX on Azure.


#### Configure SNIP in the Citrix ADC VPX

SSH to the Citrix ADC VPX and configure a SNIP, which is the secondary IP of the VPX.
This is required for Citrix ADC to interact with the pods inside the Kubernetes cluster.

```
add ns ip <snip-vpx-instance-private-ip> <vpx-instance-primary-ip-subnet>
```

"<snip-vpx-instance-private-ip>" is the dynamic private ip address that got assigned while adding a SNIP during VPX instance creation. 
"vpx-instance-primary-ip-subnet" is the subnet of the primary private IP address of the VPX instance. To verify the subnet of the private ip address. SSH into the VPX instance and do "show ip <primary-private-ip-addess>"  


#### Update the Citrix ADC VPX Image URL, management IP and VIP in the Citrix Ingress controller manifest

```
wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/cic.yaml
```

***If you don't have `wget` installed, you can use `fetch` or `curl`***

Update the Citrix CIC image with the Azure Image URL in `cic.yaml`. 
```
- name: cic-k8s-ingress-controller
  # CIC Image from Azure
  image: "<azure-cic-image-url>"
```

Update the Citrix ADC VPX's primary IP in the `cic.yaml` in the below field with the Primary Private IP address of the Azure VPX instance.

```
# Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled) 
- name: "NS_IP"
  value: "X.X.X.X"
```

Update the Citrix ADC VPX VIP in the `cic.yaml` in the below field with the private IP address of the VIP created during VPX azure instance.

```
# Set NetScaler VIP for the data traffic
- name: "NS_VIP"
  value: "X.X.X.X"
```

#### Create the Citrix Ingress Controller

Now that we have configure the Citrix Ingress controller with the required values, let's deploy it.

```
kubectl create -f cic.yaml
```

## Create example microservice and Ingress

#### Example Microservice

In this example, we will deploy an Apache microservice.


```
kubectl create -f  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/apache.yaml
```

#### Ingress

Now let's apply the ingress 

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/ingress.yaml
```

## Test your deployment

To validate your deployment, send a curl to the Public address of the VIP of VPX instance.

```
$ curl --resolve citrix-ingress.com:80:<Public-ip-address-of-VIP> http://citrix-ingress.com
<html><body><h1>It works!</h1></body></html>
```

The response received is from example microservice (apache) which is inside the Kubernetes cluster. Citrix ADC VPX being an ingress has load-balanced the request.

