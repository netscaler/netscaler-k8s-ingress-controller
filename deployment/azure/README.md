# Citrix ADC CPX as an Ingress in Azure Kubernetes Engine

This guide explains the deployment of Citrix ADC CPX as an ingress in Azure Kubernetes Engine (AKS) in basic networking mode (kubenet).


#### Prerequisites

Make sure you have a Kubernetes cluster up and running.

**This guide only explains deployment in Azure Kubernetes Engine in Basic Networking Mode.**

**Make sure the AKS is configured
in Basic Networking mode (kubenet) only and not in Advanced Networking mode (Azure CNI)**

Please refer [Guide to create an AKS cluster](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/create-aks/README.md) for any help in creating a Kubernetes cluster in AKS.

### Steps to deploy Citrix CPX as an Ingress:

- **Create a sample application and expose it as service.** In our example, let's use an apache web-server.

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/apache.yaml
```

- **Create a Citrix CPX**

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/standalone_cpx.yaml
```
 
- **Create an ingress object**

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_ingress.yaml
```

- **Expose the Citrix CPX as a service of type Load-balancer.** This would create an Azure LB with an External IP for receiving traffic.
This is supported in kubernetes since v1.10.0.

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_service.yaml
```

After executing the above command, wait for the load-balancer to create an external IP.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
apache        ClusterIP      10.0.103.3     <none>        80/TCP                       2m
cpx-ingress   LoadBalancer   10.0.37.255    <pending>     80:32258/TCP,443:32084/TCP   2m
kubernetes    ClusterIP      10.0.0.1       <none>        443/TCP                      22h
```

Once the IP is available, you may access your resources via the External IP provided by the load-balancer.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
apache        ClusterIP      10.0.103.3     <none>           80/TCP                       3m
cpx-ingress   LoadBalancer   10.0.37.255    <EXTERNAL-IP CREATED>   80:32258/TCP,443:32084/TCP   3m
kubernetes    ClusterIP      10.0.0.1       <none>           443/TCP                      22h
```

The health check for the cloud load-balancer is obtained from the **readinessProbe** configured in the [Citrix CPX deployment yaml file](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/manifest/cpx_service.yaml).
So if the health check fails for some reason, you may need to check the readinessProbe configured for Citrix CPX.


You can read further about 
[readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes)
and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer)

After the External-IP is created in the service, you can do a curl to the external IP using the host header
**citrix-ingress.com**

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```


#### Note:

**_For ease of deployment, the below deployment models have been explained with an all-in-one manifest file that combines all the above explained steps. 
You can modify the manifest to suit your application and configuration._**

## Deployment models

We have the below deployment solutions for deploying Citrix CPX as an ingress device in AKS

- [Standalone Citrix CPX deployment](#standalone-citrix-cpx-deployment)
- [High availability Citrix CPX deployment](#high-availability-citrix-cpx-deployment)
- [Citrix CPX per node deployment](#citrix-cpx-per-node-deployment)


### Standalone Citrix CPX deployment

To deploy Citrix CPX as an Ingress in a standalone deployment model in AKS, we would use the Service Type as LoadBalancer which would create a Load-balancer in
Azure cloud.
This is supported in kubernetes since v1.10.0.


#### Topology for standalone Citrix CPX deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/images/Azure_Standalone_CPX.png" width="500">


#### Steps:

Just execute the below command to create a Citrix CPX ingress with inbuilt Citrix Ingress Controller in your Kubernetes cluster

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one.yaml
```

##### To access the application:

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```

##### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one.yaml
```




### High availability Citrix CPX deployment

In the standalone deployment of Citrix CPX as ingress, if the ingress device fails for some reason, there would be a traffic
outage for a few seconds. To avoid this disruption, instead of deploying a single Citrix CPX ingress, we deploy two Citrix CPX ingress
devices. So that if one Citix CPX fails, the other Citrix CPX is availble to handle traffic till the failed Citrix CPX comes up.


#### Topology for high availability CPX deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/images/Azure_HA_CPX.png" width="500">


#### Steps:

Just execute the below command to create a CPX ingress with inbuilt Citrix Ingress Controller in your Kubernetes cluster

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one-ha.yaml
```

##### To access the application:

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```

##### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one-ha.yaml
```


### Citrix CPX per node deployment

In some cases where cluster nodes are added and removed from the cluster, Citrix CPX can also be deployed as daemonsets so that
every node will have a Citirx CPX ingress in them. This is much more reliable solution than deploying two Citrix CPX as ingress
devices when the traffic is high.


#### Topology for CPX per node deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/images/Azure_CPX_per_node.png" width="500">


#### Steps:

Just execute the below command to create a CPX ingress with inbuilt Citrix Ingress Controller in your kubernetes cluster

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one-reliable.yaml
```

##### To access the application:

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```

##### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/all-in-one-reliable.yaml
```




