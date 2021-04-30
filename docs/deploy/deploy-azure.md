# Deploy Citrix ADC CPX as an Ingress device in an Azure Kubernetes Service cluster

This topic explains how to deploy Citrix ADC CPX as an ingress device in an [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-in/services/kubernetes-service/) cluster. Citrix ADC CPX supports both the [Advanced Networking (Azure CNI)](https://docs.microsoft.com/en-us/azure/aks/concepts-network#azure-cni-advanced-networking) and [Basic Networking (Kubenet)](https://docs.microsoft.com/en-us/azure/aks/concepts-network#kubenet-basic-networking) mode of AKS.


**Note:**

If you want to use Azure repository images for Citrix ADC CPX or the Citrix ingress controller instead of the default quay.io images, then see [Deploy Citrix ADC CPX as an Ingress device in an AKS cluster using Azure repository images](deploy-azure-image.md).

## Deploy Citrix ADC CPX as an ingress device in an AKS cluster

Perform the following steps to deploy Citrix ADC CPX as an ingress device in an AKS cluster.

**Note:**
In this procedure, Apache web server is used as the sample application.

1.  Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/apache.yaml

     **Note:**
       In this example, `apache.yaml` is used. You should use the specific YAML file for your application.

2.  Deploy Citrix ADC CPX as an ingress device in the cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/standalone_cpx.yaml

3.  Create the ingress resource using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_ingress.yaml

4.  Create a service of type LoadBalancer for accessing the Citrix ADC CPX by using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_service.yaml

    This command creates an Azure load balancer with an external IP for receiving traffic.

5.  Verify the service and check whether the load balancer has created an external IP. Wait for some time if the external IP is not created.

        kubectl  get svc

    |NAME|TYPE|CLUSTER-IP|EXTERNAL-IP|PORT(S)| AGE|
    |----|----|-----|-----|----|----|
    |apache |ClusterIP|10.0.103.3|none|   80/TCP | 2m|
    |cpx-ingress |LoadBalancer |10.0.37.255 | pending |80:32258/TCP,443:32084/TCP |2m|
    |Kubernetes |ClusterIP | 10.0.0.1 |none |  443/TCP | 22h |

6.  Once the external IP for the load-balancer is available as follows, you can access your resources using the external IP for the load balancer.

        kubectl  get svc

    |NAME|TYPE|CLUSTER-IP|EXTERNAL-IP|PORT(S)|  AGE|
    |---|---|----|----|----|----|
    |apache|ClusterIP|10.0.103.3 |none|80/TCP|  3m|
    |cpx-ingress |LoadBalancer|10.0.37.255|  EXTERNAL-IP CREATED| 80:32258/TCP,443:32084/TCP |  3m|
    |Kubernetes|    ClusterIP|10.0.0.1 |none| 443/TCP| 22h|

    !!! note "Note"  
        The health check for the cloud load-balancer is obtained from the readinessProbe configured in the [Citrix ADC CPX deployment yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/manifest/cpx_service.yaml) file. 

		If the health check fails, you should check the readinessProbe configured for Citrix ADC CPX. For more information, see [readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes) and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/).

1.  Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com

## Quick Deploy

For the ease of deployment, you can just deploy a single all-in-one manifest that would combine the steps explained in the previous topic.


1. Deploy a Citrix ADC CPX ingress with in built Citrix ingress controller in your Kubernetes cluster using the [all-in-one.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/manifest/all-in-one.yaml).

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one.yaml

2. Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'

    >**Note:**
    >To delete the deployment, use the following command:
    </br>
    > ` kubectl delete -f all-in-one.yaml `
