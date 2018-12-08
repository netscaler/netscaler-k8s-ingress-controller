# CPX as an Ingress in Google Cloud Platform

This guide explains the deployment of CPX as an ingress in Google Kubernetes Engine (GKE) and Google Compute Engine
(GCE).


#### Prerequisites

Make sure you have a Kubernetes Cluster up and running.

If you are running your cluster in GKE, then make sure you have configured a cluster-admin cluster role binding.
You can do that using the below command

```
kubectl create clusterrolebinding citrix-cluster-admin --clusterrole=cluster-admin --user=<email-id of your google
account>
```

Get your google account details using the below command

```
gcloud info | grep Account
```


## Deployment models

We have the below deployment solutions for deploying CPX as an ingress device in Google Cloud

- [Standalone CPX deployment](#standalone-cpx-deployment)
- [High availability CPX deployment](#high-availability-cpx-deployment)
- [CPX per node deployment](#cpx-per-node-deployment)




### Standalone CPX deployment

To deploy CPX as an Ingress in a standalone deployment model in GCP, we would use the Service Type as LoadBalancer which would create a Load-balancer in
google cloud.
This is supported in kubernetes since v1.10.0.


#### Topology for standalone CPX deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/images/CPX-GCP-Topology-Standalone.png" width="500">


#### Steps:

Just execute the below command to create a CPX ingress with inbuilt Citrix Ingress Controller in your kubernetes cluster
```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-demo.yaml
```


_**Note**_:
The above command also creates a basic web-server as backend application in this example.

After executing the above command, wait for the load-balancer to create an external IP.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>        80/TCP                       2m
cpx-ingress   LoadBalancer   10.7.241.6     <pending>     80:32258/TCP,443:32084/TCP   2m
kubernetes    ClusterIP      10.7.240.1     <none>        443/TCP                      22h
```

Once the IP is available, you may access your resources via the External IP provided by the load-balancer.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>           80/TCP                       3m
cpx-ingress   LoadBalancer   10.7.241.6     <EXTERNAL-IP CREATED>   80:32258/TCP,443:32084/TCP   3m
kubernetes    ClusterIP      10.7.240.1     <none>           443/TCP                      22h
```


The health check for the cloud load-balancer is obtained from the **readinessProbe** configured in the CPX deployment yaml file.
So if the health check fails for some reason, you may need to check the readinessProbe configured for CPX.


You can read further about 
[readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes)
and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer)

After the External-IP is created in the service, you can do a curl to the external IP using the host header
**citrix-ingress.com**

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```


#### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-demo.yaml
```




### High availability CPX deployment

In the standalone deployment of CPX as ingress, if the ingress device fails for some reason, there would be a traffic
outage for a few seconds. To avoid this disruption, instead of deploying a single CPX ingress, we deploy two CPX ingress
devices. So that if one CPX fails, the other CPX is availble to handle traffic till the failed CPX comes up.


#### Topology for high availability CPX deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/images/CPX-GCP-HA-Solution-Topology.png" width="500">


#### Steps:

Just execute the below command to create a CPX ingress with inbuilt Citrix Ingress Controller in your kubernetes cluster
```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-ha-demo.yaml
```


_**Note**_:
The above command also creates a basic web-server as backend application in this example.

After executing the above command, wait for the load-balancer to create an external IP.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>        80/TCP                       2m
cpx-ingress   LoadBalancer   10.7.241.6     <pending>     80:32258/TCP,443:32084/TCP   2m
kubernetes    ClusterIP      10.7.240.1     <none>        443/TCP                      22h
```

Once the IP is available, you may access your resources via the External IP provided by the load-balancer.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>           80/TCP                       3m
cpx-ingress   LoadBalancer   10.7.241.6     <EXTERNAL-IP CREATED>   80:32258/TCP,443:32084/TCP   3m
kubernetes    ClusterIP      10.7.240.1     <none>           443/TCP                      22h
```


The health check for the cloud load-balancer is obtained from the **readinessProbe** configured in the CPX deployment yaml file.
So if the health check fails for some reason, you may need to check the readinessProbe configured for CPX.


You can read further about 
[readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes)
and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer)

After the External-IP is created in the service, you can do a curl to the external IP using the host header
**citrix-ingress.com**

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```


#### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-ha-demo.yaml
```




### CPX per node deployment

In some cases where cluster nodes are added and removed from the cluster, CPX can also be deployed as daemonsets so that
every node will have a CPX ingress in them. This is much more reliable solution than deploying two CPX as ingress
devices when the traffic is high.


#### Topology for CPX per node deployment:

<img src="https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/images/CPX-GCP-Daemonset-Topology.png" width="500">


#### Steps:

Just execute the below command to create a CPX ingress with inbuilt Citrix Ingress Controller in your kubernetes cluster
```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-reliable-demo.yaml
```


_**Note**_:
The above command also creates a basic web-server as backend application in this example.

After executing the above command, wait for the load-balancer to create an external IP.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>        80/TCP                       2m
cpx-ingress   LoadBalancer   10.7.241.6     <pending>     80:32258/TCP,443:32084/TCP   2m
kubernetes    ClusterIP      10.7.240.1     <none>        443/TCP                      22h
```

Once the IP is available, you may access your resources via the External IP provided by the load-balancer.


```
$ kubectl  get svc 
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
apache        ClusterIP      10.7.248.216   <none>           80/TCP                       3m
cpx-ingress   LoadBalancer   10.7.241.6     <EXTERNAL-IP CREATED>   80:32258/TCP,443:32084/TCP   3m
kubernetes    ClusterIP      10.7.240.1     <none>           443/TCP                      22h
```


The health check for the cloud load-balancer is obtained from the **readinessProbe** configured in the CPX deployment yaml file.
So if the health check fails for some reason, you may need to check the readinessProbe configured for CPX.


You can read further about 
[readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes)
and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer)

After the External-IP is created in the service, you can do a curl to the external IP using the host header
**citrix-ingress.com**

```
curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
```


#### Tear Down

Just execute the below command to delete the complete deployment

```
kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx-gcp-reliable-demo.yaml
```




