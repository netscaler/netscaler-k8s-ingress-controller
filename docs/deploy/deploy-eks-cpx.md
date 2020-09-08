# Deploy Citrix ADC CPX as an Ingress device in Elastic Kubernetes Service (EKS)

This topic explains how to deploy Citrix ADC CPX as an ingress device in [Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/) clusters.

![CPX in EKS](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/media/AWS_standalone_cpx.png)

## Deploy Citrix ADC CPX as an ingress device in Elastic Kubernetes Service (EKS)

1.  Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/apache.yaml
  
    !!! note "Note"
        In this example, ``apache.yaml`` is used. You should use the specific YAML file for your application.

1.  Deploy Citrix ADC CPX as an ingress device in the cluster using the following command.

	Citrix ADC CPX requires a Kubernetes Secret to be created for login credentials. Below command would create the required Kubernetes secret.
	

        kubectl create secret generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot'
        
	Deploy Citrix ADC CPX with inbuilt Citrix Ingress Controller.
	
	
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

You can also use our [all-in-one](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/all-in-one.yaml) manifest file to deploy Citrix ADC CPX along with a sample microservice using a single command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/all-in-one.yaml


