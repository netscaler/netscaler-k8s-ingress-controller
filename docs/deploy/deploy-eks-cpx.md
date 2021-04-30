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
        

	An Ingress class named **citrix-ingress** is used in this example. Please see our [detailed Ingress class documentation](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/ingress-classes.md).

1.  Create a service of type LoadBalancer for accessing the Citrix ADC CPX by using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/cpx_service.yaml

    !!! note "Note"
        This command creates a load balancer with an external IP/Hostname for receiving traffic.

1.  Verify the service and check whether the load balancer has created an external IP/Hostname.

        kubectl  get svc cpx-ingress

    |NAME | TYPE | CLUSTER-IP | EXTERNAL-IP | PORT(S) | AGE |
    | --- | ---| ----| ----| ----| ----|
    |cpx-ingress |LoadBalancer | 10.7.241.6 |  EXTERNAL-HOSTNAME | 80:32258/TCP,443:32084/TCP | 2m|


1.  Access the application using the following command.

        curl http://<External-hostname-of-loadbalancer>/ -H 'Host: citrix-ingress.com'


## Quick Deploy

For the ease of deployment, you can just deploy a single all-in-one manifest that would combine the steps explained in the previous topic.


1. Deploy a Citrix ADC CPX ingress with in built Citrix ingress controller in your Kubernetes cluster using the [all-in-one.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/all-in-one.yaml).

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/all-in-one.yaml

2. Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'

    >**Note:**
    >To delete the deployment, use the following command:
    </br>
    > ` kubectl delete -f all-in-one.yaml `
