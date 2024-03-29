# Deploy Netscaler ingress controller in an Azure Kubernetes Service cluster with Netscaler VPX

This topic explains how to deploy the Netscaler ingress controller with Netscaler VPX in an [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-in/services/kubernetes-service/) cluster. You can also configure the Kubernetes cluster on [Azure VMs](https://azure.microsoft.com/en-in/services/virtual-machines/) and then deploy the Netscaler ingress controller with Netscaler VPX.

The procedure to deploy for both AKS and Azure VM is the same. However, if you are configuring Kubernetes on Azure VMs you need to deploy the CNI plug-in for the Kubernetes cluster.

**Prerequisites**

You should complete the following tasks before performing the steps in the procedure.

-  Ensure that you have a Kubernetes cluster up and running.

!!! note "Note"
    For more information on creating a Kubernetes cluster in AKS, see [Guide to create an AKS cluster](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/azure/create-aks/README.md).

## Topology

The following is the sample topology used in this deployment.

![single-tier](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/media/singletopology.png)

## Get a Netscaler VPX instance from Azure Marketplace

You can create Netscaler VPX from the Azure Marketplace.
For more information on how to create a Netscaler VPX instance from Azure Marketplace, see [Get Netscaler VPX from Azure Marketplace](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/deploy/azure-vpx.md).

## Get the Netscaler ingress controller from Azure Marketplace

To deploy the Netscaler ingress controller, an image registry should be created on Azure and the corresponding image URL should be used to fetch the Netscaler ingress controller image.

For more information on how to create a registry and get the image URL, see [Get Netscaler ingress controller from Azure Marketplace](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/deploy/azure-cic-url.md).

Once a registry is created, the Netscaler ingress controller registry name should be attached to the AKS cluster used for deployment.

```
az aks update -n <cluster-name> -g <resource-group-where-aks-deployed> --attach-acr <cic-registry>
```

## Deploy Netscaler ingress controller

Perform the following steps to deploy the Netscaler ingress controller.

1. Create Netscaler VPX login credentials using Kubernetes secret.

    
        kubectl create secret  generic nslogin --from-literal=username=<azure-vpx-instance-username> --from-literal=password=<azure-vpx-instance-password>
    
   **Note:** The Netscaler VPX user name and password should be the same as the credentials set while creating Netscaler VPX on Azure.

2. Using SSH, configure a SNIP in the Netscaler VPX, which is the secondary IP address of the Netscaler VPX. This step is required for the Netscaler to interact with pods inside the Kubernetes cluster.

   
        add ns ip <snip-vpx-instance-private-ip> <vpx-instance-primary-ip-subnet>
    

   -  `snip-vpx-instance-private-ip` is the dynamic private IP address assigned while adding a SNIP during the Netscaler VPX instance creation.

   - `vpx-instance-primary-ip-subnet` is the subnet of the primary private IP address of the Netscaler VPX instance.
  
     To verify the subnet of the private IP address, SSH into the Netscaler VPX instance and use the following command.

    
    
          show ip <primary-private-ip-addess>
    


3. Update the Netscaler VPX image URL, management IP, and VIP in the Netscaler ingress controller YAML file.


   1. Download the Netscaler ingress controller YAML file.

       

          wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/cic.yaml
     
       

       **Note:** If you do not have `wget` installed, you can use the `fetch` or `curl` command.

   2. Update the Netscaler ingress controller image with the Azure image URL in the `cic.yaml` file.

      
            - name: cic-k8s-ingress-controller
              # CIC Image from Azure
              image: "<azure-cic-image-url>"
      

   3. Update the primary IP address of the Netscaler VPX in the `cic.yaml` in the following field with the primary private IP address of the Azure VPX instance.

      
     
          # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled) 
          - name: "NS_IP"
            value: "X.X.X.X"
      

    1. Update the Netscaler VPX VIP in the `cic.yaml` in the following field with the private IP address of the VIP assigned during VPX Azure instance creation.
 
       

            # Set NetScaler VIP for the data traffic
            - name: "NS_VIP"
              value: "X.X.X.X"
        
      

4. Once you have configured the Netscaler ingress controller with the required values, deploy the Netscaler ingress controller using the following command.


            kubectl create -f cic.yaml


## Verify the deployment using a sample application


1. Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.


        kubectl create -f  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/apache.yaml


1. Create the Ingress resource using the following command.

    
        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azurecic/ingress.yaml
    

2. To validate your deployment, use the following command.

    
        $ curl --resolve citrix-ingress.com:80:<Public-ip-address-of-VIP> http://citrix-ingress.com
        <html><body><h1>It works!</h1></body></html>
    

    The response is received from the sample microservice (Apache) which is inside the Kubernetes cluster. Netscaler VPX has load-balanced the request.
