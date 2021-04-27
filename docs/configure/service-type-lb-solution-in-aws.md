# Deploy Citrix solution for service of type LoadBalancer in AWS

A service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) is a simpler and faster way to expose a microservice running in a Kubernetes cluster to the external world. In cloud deployments, when you create a service of type LoadBalancer, a cloud managed load balancer is assigned to the service. The service is, then, exposed using the load balancer. For more information about services of type LoadBalancer, see [Services of type LoadBalancer](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).

With the Citrix solution for service of type LoadBalancer, you can use Citrix ADC to directly load balance and expose a service instead of the cloud managed load balancer. Citrix provides this solution for service of type LoadBalancer for on-prem and cloud. Services of type LoadBalancer are natively supported in Kubernetes deployments on public clouds such as AWS, GCP, and Azure.

When you deploy a service in AWS, a load balancer is created automatically and the IP address is allocated to the external field of the service. In this Citrix solution, Citrix IPAM controller allocates the IP address and that IP address is the VIP of Citrix ADC VPX. Citrix ingress controller, deployed in a Kubernetes cluster, configures a Citrix ADC deployed outside the cluster to load balance the incoming traffic. So, the service is accessed through Citrix ADC VPX instead of the cloud load balancer.

 You need to specify the service `type` as `LoadBalancer` in the service definition. Setting the `type` field to `LoadBalancer` provisions a load balancer for your service on AWS.

Citrix IPAM controller is used to automatically allocate IP addresses to services of type LoadBalancer from a specified range of IP addresses. For more information about the Citrix solution for services of type LoadBalancer, see [Expose services of type LoadBalancer](https://github.com/citrix/citrix-k8s-ingress-controller/blob/ef929526a1bd23f30a8677d4494c600f21b7b2a8/docs/network/type_loadbalancer.md).

**Prerequisites**

 -  Ensure that the Elastic Kubernetes Service (EKS) cluster version 1.18 or later is running.
 -  Ensure that Citrix ADC VPX and EKS are deployed and running in the same VPC. For information about creating Citrix ADC VPX in AWS, see [Create a Citrix ADC VPX instance from AWS Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/ef929526a1bd23f30a8677d4494c600f21b7b2a8/deployment/aws/quick-deploy-cic/README.md#create-a-citrix-adc-vpx-instance-from-aws-marketplace).

## Deploy Citrix solution for service of type LoadBalancer in AWS using Helm charts

Perform the following steps to configure the Citrix solution for service of type LoadBalancer using Helm charts.

1.  Download the [unified-lb-values.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/how-to/typeLB/aws/unified-lb-values.yaml) file and edit the YAML file for specifying the following details:

      -  Citrix ADC VPX NSIP. For more information, see [Citrix ingress controller Helm chart](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ingress-controller)
    
      -  Secret created using the Citrix ADC VPX credentials. For more information, see [Citrix ingress controller Helm chart](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ingress-controller).

      -  List of VIPs to be used in IPAM controller. For more information, see [IPAM Helm chart](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ipam-controller).

1.  Deploy Citrix IPAM controller and Citrix ingress controller on your Amazon EKS cluster using the edited YAML file. Use the following commands:

        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install serviceLB citrix/citrix-cloud-native -f values.yaml
    
1.  Deploy the application and service in Amazon EKS:

      1.  Add the following annotation in the service manifest:

              beta.kubernetes.io/aws-load-balancer-type: "external"

      1.  Deploy the application and service with the modified annotation using the following command:

              kubectl create -f https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/how-to/typeLB/aws/guestbook-all-in-one-lb.yaml

            **Note**: The `guestbook` microservice is a sample used in this procedure. You can deploy an application of your choice. Ensure that the service should be of type LoadBalancer and the service manifest should contain the annotation.
      
      1.  Associate an elastic IP address with the VIP of Citrix ADC VPX.

      1.  Access the application using a browser. For example, `http://EIP-associated-with-vip`.

## Deploy Citrix solution for service of type LoadBalancer in AWS using YAML

Perform the following steps to deploy the Citrix solution for service of type LoadBalancer using YAML.

1.  Download the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file and specify the following details.

      -  [Citrix ADC VPX NSIP](https://docs.citrix.com/en-us/citrix-adc/current-release/networking/ip-addressing/configuring-citrix-adc-owned-ip-addresses/configuring-citrix-adc-ip-address.html)
    
      -  Secret created using the Citrix ADC VPX credentials. For information about creating the secret, see [Create a secret](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/secret-credentials/#create-a-kubernetes-secret).

      -  Specify the argument for Citrix IPAM controller:

              args:
                - --ipam
                  citrix-ipam-controller

1. Deploy the Citrix ingress controller using the modified YAML.

        kubectl create -f citrix-k8s-ingress-controller.yaml

1. Deploy the Citrix VIP CRD which enables communication between the Citrix ingress controller and the IPAM controller using the following command.

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/vip/vip.yaml

    For more information about deploying Citrix VIP CRD, see [Deploy the VIP CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/c683c72457e1be74718f72c2f26bbe57105133a2/docs/network/type_loadbalancer.md#step1-deploy-the-vip-crd).

1. Deploy the IPAM controller. For information about deploying the IPAM controller, see [Deploy the IPAM controller](https://github.com/citrix/citrix-k8s-ingress-controller/blob/c683c72457e1be74718f72c2f26bbe57105133a2/docs/network/type_loadbalancer.md#step3-deploy-the-ipam-controller).

    **Note**: Specify the list of Citrix ADC VPX VIPs in the **VIP_RANGE** field of the IPAM deployment YAML file.

1.  Deploy the application with service type LoadBalancer in Amazon EKS using the following steps:

      1.  Add the following annotation in the service manifest.

              beta.kubernetes.io/aws-load-balancer-type: "external"

      1.  Deploy the application and service with the modified annotation using the following command.

              kubectl create -f https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/how-to/typeLB/aws/guestbook-all-in-one-lb.yaml

            **Note**: The `guestbook` microservice is a sample used in this procedure. You can deploy an application of your choice. Ensure that the service should be of type LoadBalancer and the service manifest should contain the annotation.
      
      1.  Associate an elastic IP address with the VIP of Citrix ADC VPX.

      1.  Access the application using a browser. For example, `http://EIP-associated-with-vip`.