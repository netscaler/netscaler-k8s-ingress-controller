# Deploy Citrix ADC CPX as an Ingress device in Elastic Kubernetes Service (EKS)

This topic explains how to deploy Citrix ADC CPX as an ingress device in [Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/) clusters.

![CPX in EKS](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/media/AWS_standalone_cpx.png)

## Deploy Citrix ADC CPX as an ingress device in Elastic Kubernetes Service (EKS)

1.  Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/apache.yaml
  
    !!! note "Note"
        In this example, ``apache.yaml`` is used. You should use the specific YAML file for your application.

1.  Deploy Citrix ADC CPX as an ingress device in the cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/standalone_cpx.yaml

1.  Create the ingress resource using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/cpx_ingress.yaml

1.  Create a service of type LoadBalancer for accessing the Citrix ADC CPX by using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/cpx_service.yaml

    !!! note "Note"
        This command creates a load balancer with an external IP for receiving traffic.

1.  Verify the service and check whether the load balancer has created an external IP. Wait for some time if the external IP is not created.

        kubectl  get svc

    |NAME | TYPE | CLUSTER-IP | EXTERNAL-IP | PORT(S) | AGE |
    | --- | ---| ----| ----| ----| ----|
    |apache | ClusterIP |10.7.248.216 |none |  80/TCP | 2m |
    |cpx-ingress |LoadBalancer | 10.7.241.6 |  pending | 80:32258/TCP,443:32084/TCP | 2m|
    |kubernetes |ClusterIP |10.7.240.1 |none | 443/TCP | 22h|

1.  Once the external IP for the load-balancer is available as follows, you can access your resources using the external IP for the load balancer.

        kubectl  get svc

    |Name | Type | Cluster-IP | External IP| Port(s) | Age |
    |-----| -----| -------| -----| -----| ----|
    |apache| ClusterIP|10.7.248.216|none|80/TCP |3m|
    |cpx-ingress|LoadBalancer|10.7.241.6|EXTERNAL-IP CREATED|80:32258/TCP,443:32084/TCP|3m|
    |kubernetes| ClusterIP| 10.7.240.1|none|443/TCP|22h|`

    !!! note "Note"
        The health check for the cloud load-balancer is obtained from the readinessProbe configured in the [Citrix ADC CPX service YAML](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/cpx_service.yaml) file. If the health check fails, you should check the readinessProbe configured for Citrix ADC CPX.
        For more information, see [readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes) and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/).

1.  Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'
        
## Quick Deploy

You can also use our [all-in-one](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/all-in-one.yaml) manifest file to deploy Citrix ADC CPX along with a sample microservice using a single command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/all-in-one.yaml


