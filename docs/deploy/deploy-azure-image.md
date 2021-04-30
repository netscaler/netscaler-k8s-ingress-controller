# Deploy Citrix ADC CPX as an Ingress device in an Azure Kubernetes Service cluster using Azure repository images

This topic explains how to deploy Citrix ADC CPX as an ingress device in an [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-in/services/kubernetes-service/) cluster.


## Get Citrix ADC CPX from Azure Marketplace

To deploy Citrix ADC CPX, an image registry should be created on Azure and the corresponding image URL should be used to fetch the Citrix ADC CPX image.
For more information on how to create a registry and get image URL, see [Get Citrix ADC CPX from Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-cpx-url.md).

Once the registry is created, the Citrix ADC CPX registry name should be attached to the AKS cluster used for deployment.

```
az aks update -n <cluster-name> -g <resource-group-where-aks-deployed> --attach-acr <cpx-registry>
```

## Get Citrix Ingress Controller from Azure Marketplace

To deploy the Citrix ingress controller, an image registry should be created on Azure and the corresponding image URL should be used to fetch the CIC image.
For more information on how to create registry and get image URL, see [Get Citrix ingress controller from Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-cic-url.md).

Once the registry is created, the Citrix ingress controller registry name should be attached to the AKS cluster used for deployment.

```
az aks update -n <cluster-name> -g <resource-group-where-aks-deployed> --attach-acr <cic-registry>
```

## Deploy Citrix ADC CPX as an ingress device in an AKS cluster

Perform the following steps to deploy Citrix ADC CPX as an ingress device in an AKS cluster.

**Note:**
In this procedure, Apache web server is used as the sample application.

1.  Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/apache.yaml

    **Note:**
        In this example, `apache.yaml` is used. You should use the specific YAML file for your application.

2.  Deploy Citrix ADC CPX as an ingress device in the cluster using the following steps:
   
    1. Download the YAML file using the following command.

        
            wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/azureimage-standalone_cpx.yaml
        

    2. Update the Citrix ADC CPX image with the Azure image URL in `azureimage-standalone_cpx.yaml` file. 

        

           - name: cpx-ingress
             image: "<azure-cpx-instance-url>"
        
        

    3. Update the Citrix ingress controller image with the Azure Image URL in `azureimage-standalone_cpx.yaml` file.

        

           - name: cic
             image: "<azure-cic-instance-url>"


    4. After updating the required values, deploy the `azureimage-standalone_cpx.yaml` file.

        

           kubectl create -f azureimage-standalone_cpx.yaml
        
        

3.  Create the ingress resource using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_ingress.yaml

4.  Create a service of type LoadBalancer for accessing the Citrix ADC CPX by using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_service.yaml

    This command creates an Azure load balancer with an external IP for receiving traffic.

5.  Verify the service and check whether the load balancer has created an external IP. Wait for some time if the external IP is not created.

        kubectl  get svc

    |NAME|TYPE|CLUSTER-IP|EXTERNAL-IP|PORT(S)| AGE|
    |----|----|-----|-----|----|----|
    |apache |ClusterIP|10.0.103.3|none|   80/TCP | 2 m|
    |cpx-ingress |LoadBalancer |10.0.37.255 | pending |80:32258/TCP,443:32084/TCP |2 m|
    |Kubernetes |ClusterIP | 10.0.0.1 |none |  443/TCP | 22 h |

6.  Once the external IP for the load-balancer is available as follows, you can access your resources using the external IP for the load balancer.

        kubectl  get svc

    |NAME|TYPE|CLUSTER-IP|EXTERNAL-IP|PORT(S)|  AGE|
    |---|---|----|----|----|----|
    |apache|ClusterIP|10.0.103.3 |none|80/TCP|  3 m|
    |cpx-ingress |LoadBalancer|10.0.37.255|  EXTERNAL-IP CREATED| 80:32258/TCP,443:32084/TCP |  3 m|
    |Kubernetes|    ClusterIP|10.0.0.1 |none| 443/TCP| 22 h|

    **Note:**
    The health check for the cloud load-balancer is obtained from the readinessProbe configured in the [Citrix ADC CPX deployment yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/manifest/cpx_service.yaml) file. If the health check fails, you should check the readinessProbe configured for Citrix ADC CPX. For more information, see [readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes) and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/).

7.  Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com

