# Deploy Citrix ADC CPX as an Ingress device in an Amazon EKS cluster

This topic explains how to deploy Citrix ADC CPX as an ingress device in an [Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html).
Citrix ADC CPX supports the Amazon virtual private cloud (VPC) CNI plug-in provided for Kubernetes. This CNI plug-in allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network. When you deploy Citrix ADC CPX as a pod in Amazon EKS, an IP address is allocated to the Citrix ADC CPX from the same VPC network.

## Deploy Citrix ADC CPX as an Ingress device in an Amazon EKS cluster

Perform the following steps to deploy Citrix ADC CPX as an Ingress device in an Amazon EKS cluster.

>**Note:** In this procedure, Apache web server is used as the sample application.

1. Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl create -f apache.yaml

    >**Note:** In this example, [apache.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/apache.yaml) is used. You must use the specific YAML file for your application.

2. Deploy Citrix ADC CPX as an Ingress device in the cluster using the [standalone_cpx.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/standalone_cpx.yaml) file.

        kubectl create -f standalone_cpx.yaml

1. Create a Kubernetes secret for Citrix ADC CPX as shown in the following example. 
     
       kubectl create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot' 

2. Create the Ingress resource using the [cpx_ingress.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller//blob/master/deployment/aws/manifest/cpx_ingress.yaml) following command.

        kubectl create -f cpx_ingress.yaml

3. Create a service of type LoadBalancer for accessing the Citrix ADC CPX by using the [cpx_service.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/cpx_service.yaml) file.

        kubectl create -f cpx_service.yaml

    This command creates an Elastic Load Balancer (ELB) with an external IP for receiving traffic.

4. Verify the service and check whether the load balancer has created an external IP. Wait for some time if the external IP is not created.

        kubectl  get svc

    | NAME        | TYPE         | CLUSTER-IP  | EXTERNAL-IP | PORT(S)                    | AGE |
    | ----------- | ------------ | ----------- | ----------- | -------------------------- | --- |
    | apache      | ClusterIP    | 10.0.103.3  | none        | 80/TCP                     | 2 m  |
    | cpx-ingress | LoadBalancer | 10.0.37.255 | pending     | 80:32258/TCP,443:32084/TCP | 2 m  |
    | Kubernetes  | ClusterIP    | 10.0.0.1    | none        | 443/TCP                    | 22 h |

5. Once the external IP for the load-balancer is available as follows, you can access your resources using the external IP for the load balancer.

        kubectl  get svc

    | NAME        | TYPE         | CLUSTER-IP  | EXTERNAL-IP | PORT(S)                    | AGE |
    | ----------- | ------------ | ----------- | ----------- | -------------------------- | --- |
    | apache      | ClusterIP    | 10.0.103.3  | none        | 80/TCP                     | 3 m  |
    | cpx-ingress | LoadBalancer | 10.0.37.255 | `<External-ip-of-loadbalancer>`| 80:32258/TCP,443:32084/TCP | 2 m  |
    | Kubernetes  | ClusterIP    | 10.0.0.1    | none        | 443/TCP                    | 22 h |

    >**Note:**  The health check for the cloud load-balancer is obtained from the `readinessProbe` configured in the [Citrix ADC CPX deployment YAML](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/cpx_service.yaml) file.</br>
    If the health check fails, you must check the `readinessProbe` configured for Citrix ADC CPX. For more information, see [readinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#define-readiness-probes) and [external Load balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/).




6. Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com

## Deployment models

You can use the following deployment solutions for deploying Citrix ADC CPX as an ingress device in an Amazon EKS cluster.

-  Standalone Citrix ADC CPX deployment
-  High availability Citrix ADC CPX deployment
-  Citrix ADC CPX per node deployment

>**Note:**
>For the ease of deployment, the deployment models in this topic are explained with an all-in-one manifest file that combines the steps explained in the previous topic. You can modify the manifest file to suit your application and configuration.

### Deploy a standalone Citrix ADC CPX as the Ingress device

To deploy Citrix ADC CPX as an Ingress device in a standalone deployment model in Amazon EKS, you should use the service type as LoadBalancer. This step would create a load balancer in the AWS cloud.

![AWS_Standalone_CPX](AWS_standalone_cpx.png)

Perform the following steps to deploy a stand-alone Citrix ADC CPX as the ingress device.

1. Create a Kubernetes secret for Citrix ADC CPX as shown in the following example.
     
       kubectl create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot' 

1. Deploy a Citrix ADC CPX ingress with in built Citrix ingress controller in your Kubernetes cluster using the [all-in-one.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/all-in-one.yaml).

        kubectl create -f all-in-one.yaml

2. Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'

    >**Note:**
    >To delete the deployment, use the following command:
    </br>
    > ` kubectl delete -f all-in-one.yaml `

### Deploy Citrix ADC CPX for high availability

In the standalone deployment of Citrix ADC CPX as the Ingress, if the Ingress device fails there would be a traffic outage for a few seconds. To avoid this traffic disruption, you can deploy two Citrix ADC CPX Ingress devices instead of deploying a single Citrix ADC CPX Ingress device. In such deployments, even if one Citrix ADC CPX fails the other Citrix ADC CPX handles the traffic until the failed Citrix ADC CPX comes up.

![AWS_HA_CPX](AWS_HA_CPX.png)

Perform the following steps to deploy two Citrix ADC CPX devices for high availability.

1. Create a Kubernetes secret for each Citrix ADC CPX as shown in the following example.
     
       kubectl create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot' 

1. Deploy Citrix ADC CPX ingress devices for high availability in your Kubernetes cluster by using the [all-in-one-ha.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/all-in-one-ha.yaml) file.

        kubectl create -f all-in-one-ha.yaml

2. Access the application using the following command.

        curl http://<External-ip-of-loadbalancer>/ -H 'Host: citrix-ingress.com'

    >**Note:**
    >To delete the deployment, use the following command:
    </br>
    >`kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/aws/manifest/all-in-one-ha.yaml`


