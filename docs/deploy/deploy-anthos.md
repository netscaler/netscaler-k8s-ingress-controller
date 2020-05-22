# Deploy the Citrix ingress controller in Anthos

[Anthos](https://cloud.google.com/anthos) is a hybrid and multi cloud platform that lets you run your applications on existing on-prem hardware or in the public cloud. It provides a consistent development and operation experience for cloud and on-premises environments.

The Citrix ingress controller can be deployed in Anthos GKE on-premises using the following deployment modes:

- Exposing Citrix ADC CPX with the sidecar ingress controller as a service of type `LoadBalancer`.
- Dual-tier Ingress deployment

## Expose Citrix ADC CPX as a service of type `LoadBalancer` in Anthos GKE on-prem

In this deployment, Citrix ADC VPX or MPX is deployed outside the cluster at Tier-1 and Citrix ADC CPX at Tier-2 inside the Anthos cluster similar to a dual-tier deployment. However instead of using Ingress, the Citrix ADC CPX is exposed using the Kubernetes service of type `LoadBalancer`.
The Citrix ingress controller automates the process of configuring the IP address provided in the `LoadBalancerIP` field of the service specification.

**Prerequisites**

- You must deploy a Tier-1 Citrix ADC VPX or MPX in the same subnet as the Anthos GKE on-prem user cluster.

- You must configure a subnet IP address (SNIP) on the Tier-1 Citrix ADC and Anthos GKE on-prem cluster nodes should be reachable using the IP address.

- To use a Citrix ADC VPX or MPX from a different network, use [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller) to enable communication between the Citrix ADC and the Anthos GKE on-prem cluster.

- You must set aside a virtual IP address (VIP) to be used as a Load Balancer IP address.

### Deploy Citrix ADC CPX as service of type `LoadBalancer` in Anthos GKE on-premises

Perform the following steps to deploy Citrix ADC CPX as a service of type `LoadBalancer` in Anthos GKE on-premises.

1. Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.


        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/anthos/manifest/anthos/service-type-lb-wo-ipam/apache.yaml

   **Note:** In this example, `apache.yaml` is used. You should use the specific YAML file for your application.

2. Deploy Citrix ADC CPX with the sidecar Citrix ingress controller as Tier-2 Ingress device using the [cpx-cic.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/cpx-cic.yaml) file.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/cpx-cic.yaml

3. (Optional) Create a self-signed SSL certificate and a key to be used with the Ingress for TLS configuration.

  
        openssl req -subj '/CN=anthos-citrix-ingress.com/O=Citrix Systems Inc/C=IN' -new -newkey rsa:2048 -days 5794 -nodes -x509 -keyout $PWD/anthos-citrix-certificate.key -out $PWD/anthos-citrix-certificate.crt;openssl rsa -in $PWD/anthos-citrix-certificate.key -out $PWD/anthos-citrix-certificate.key

   **Note:** If you already have an SSL certificate, you can create a Kubernetes secret using the same. This is just an example command to create a self-signed certificate and also this command assumes the host name of the application to be `anthos-citrix-ingress.com`.


4. Create a Kubernetes secret with the created SSL cert-key pair.

        kubectl --kubeconfig user-cluster-1-kubeconfig create secret tls anthos-citrix --cert=$PWD/anthos-citrix-certificate.crt --key=$PWD/anthos-citrix-certificate.key

5. Create an Ingress resource for Tier-2 using the [tier-2-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/tier-2-ingress.yaml) file.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/tier-2-ingress.yaml

6.  Create a Kubernetes secret for the Tier-1 Citrix ADC.

        kubectl --kubeconfig user-cluster-1-kubeconfig create secret  generic nslogin --from-literal=username='nsroot' --from-literal=password='nsroot'

7. Deploy the Citrix ingress controller as a Tier-1 ingress controller.

   1. Download the [cic.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/cic.yaml) file.
   
   2. Enter the management IP address of Citrix ADC. Update the Tier-1 Citrix ADC's management IP address in the placeholder `Tier-1-Citrix-ADC-IP` specified in the `cic.yaml` file.
   
   3. Save and deploy the `cic.yaml` using the following command. 

                kubectl --kubeconfig user-cluster-1-kubeconfig create -f cic.yaml

8.  Expose Citrix ADC CPX as a Kubernetes service of type `LoadBalancer`.
    
    1. Download the [cpx-service-type-lb.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/anthos/manifest/service-type-lb-wo-ipam/cpx-service-type-lb.yaml) file.
    
    2. Edit the YAML file and specify the value of `VIP-for-accessing-microservices` as the VIP address which is to be used for accessing the applications inside the cluster. This VIP address is the one set aside to be used as a Load Balancer IP address. 
    
    3. Save and deploy the `cpx-service-type-lb.yaml` file using the following command.

                kubectl --kubeconfig user-cluster-1-kubeconfig create -f cpx-service-type-lb.yaml

9.  Update the DNS records with the IP address of `VIP-for-accessing-microservices`  for accessing the microservice. In this example, to access the Apache microservice, you must have the following DNS entry.

        `<VIP-for-accessing-microservices> anthos-citrix-ingress.com`

10. Use the following command to access the application.

        curl -k --resolve anthos-citrix-ingress.com:443:<VIP-for-accessing-microservices> https://anthos-citrix-ingress.com/ <html><body><h1>It works!</h1></body></html>

    **Note:** In this command, `--resolve anthos-citrix-ingress.com:443:<VIP-for-accessing-microservices>` is used to override the DNS configuration part in step 9 for demonstration purpose. 

### Clean up the installation: Expose Citrix ADC CPX as service of type `LoadBalancer`

To clean up the installation, use the `kubectl --kubeconfig delete` command to delete each deployment.

To delete the Citrix ADC CPX service deployment (CPX+CIC service) use the following command:

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cpx-service-type-lb.yaml

To delete the Tier-2 Ingress object, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f tier-2-ingress.yaml

To delete the Citrix ADC CPX deployment along with the sidecar Citrix ingress controller, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cpx-cic.yaml

To delete the stand-alone Citrix ingress controller, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cic.yaml

To delete the Apache microservice, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f apache.yaml

To delete the Kubernetes secret, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete secret anthos-citrix

To delete the `nslogin` secret, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete secret nslogin

## Dual tier Ingress deployment

In a dual-tier Ingress deployment, Citrix ADC VPX or MPX is deployed outside the Kubernetes cluster (Tier-1) and Citrix ADC CPXs are deployed inside the Kubernetes cluster (Tier-2).

Citrix ADC MPX or VPX devices in Tier-1 proxy the traffic (North-South) from the client to Citrix ADC CPXs in Tier-2. The Tier-2 Citrix ADC CPX then routes the traffic to the microservices in the Kubernetes cluster. The Citrix ingress controller deployed as a standalone pod configures the Tier-1 Citrix ADC. The sidecar Citrix ingress controller in one or more Citrix ADC CPX pods configures the associated Citrix ADC CPX in the same pod.

**Prerequisites**

- You must deploy a Tier-1 Citrix ADC VPX or MPX in the same subnet as the Anthos GKE on-prem user cluster.

- You must configure a subnet IP address (SNIP) on the Tier-1 Citrix ADC and Anthos GKE on-prem cluster nodes should be reachable using the IP address.

- To use a Citrix ADC VPX or MPX from a different network, use the [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller) to enable communication between the Citrix ADC and the Anthos GKE on-prem cluster.
  
- You must set aside a virtual IP address to be used as a front-end IP address in the Tier-1 Ingress manifest.

### Dual-tier Ingress deployment in Anthos GKE on-prem

Perform the following steps to deploy a dual-tier Ingress deployment of Citrix ADC in Anthos GKE on-prem.

1. Deploy the required application in your Kubernetes cluster and expose it as a service in your cluster using the following command.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/apache.yaml
   
   **Note:** In this example, `apache.yaml` is used. You should use the specific YAML file for your application.

2. Deploy Citrix ADC CPX with the Citrix ingress controller as Tier-2 Ingress using the [cpx-cic.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/cpx-cic.yaml) file.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/cpx-cic.yaml

3. Expose Citrix ADC CPX as a Kubernetes service using the `cpx-service.yaml` file.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/cpx-service.yaml

4. (Optional) Create a self-signed SSL certificate and a key to be used with the Ingress for TLS configuration.
     
     **Note:** If you already have an SSL certificate, you can create a Kubernetes secret using the same.

        openssl req -subj '/CN=anthos-citrix-ingress.com/O=Citrix Systems Inc/C=IN' -new -newkey rsa:2048 -days 5794 -nodes -x509 -keyout $PWD/anthos-citrix-certificate.key -out $PWD/anthos-citrix-certificate.crt;openssl rsa -in $PWD/anthos-citrix-certificate.key -out $PWD/anthos-citrix-certificate.key

     **Note:** This is just an example command to create a self-signed certificate and also this command assumes that the hostname of the application to be `anthos-citrix-ingress.com`.

5. Create a Kubernetes secret with the created SSL cert-key pair. 

        kubectl --kubeconfig user-cluster-1-kubeconfig create secret tls anthos-citrix --cert=$PWD/anthos-citrix-certificate.crt --key=$PWD/anthos-citrix-certificate.key

6. Create an Ingress resource for Tier-2 using the [tier-2-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/tier-2-ingress.yaml) file.

        kubectl --kubeconfig user-cluster-1-kubeconfig create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/tier-2-ingress.yaml

7.  Create a Kubernetes secret for the Tier-1 Citrix ADC.

        kubectl --kubeconfig user-cluster-1-kubeconfig create secret  generic nslogin --from-literal=username='citrix-adc-username' --from-literal=password='citrix-adc-password'

8.  Deploy the Citrix ingress controller as a Tier-1 ingress controller.

    1. Download the [cic.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/cic.yaml) file.
   
    2. Enter the management IP address of Citrix ADC. Update the Tier-1 Citrix ADC's management IP address in the placeholder `Tier-1-Citrix-ADC-IP` specified in the `cic.yaml` file.
   
    3. Save and deploy the `cic.yaml` using the following command.

                kubectl --kubeconfig user-cluster-1-kubeconfig create -f cic.yaml
9.  Create an Ingress resource for Tier-1 using the [tier-1-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/tier-1-ingress.yaml) file.

    1. Download the [tier-1-ingress.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/docs/deployment/gcp/manifest/anthos/dual-tiered-ingress/tier-1-ingress.yaml) file.
    
    2. Edit the YAML file and replace `VIP-Citrix-ADC` with the VIP address which was set aside.
    
    3. Save and deploy the `tier-1-ingress.yaml` file using the following command.

                kubectl --kubeconfig user-cluster-1-kubeconfig create -f tier-1-ingress.yaml

10. Update the DNS records with the IP address of `VIP-Citrix-ADC` for accessing the microservice. In this example, to access the Apache microservice, you must have the following DNS entry.
   
                <VIP-Citrix-ADC> anthos-citrix-ingress.com
    
11. Use the following command to access the application.
   

            curl -k --resolve anthos-citrix-ingress.com:443:<VIP-Citrix-ADC>   https://anthos-citrix-ingress.com/
            <html><body><h1>It works!</h1></body></html>

    **Note:** In this command, `--resolve anthos-citrix-ingress.com:443:<VIP-for-accessing-microservices>` is used to override the DNS configuration part.

### Clean up the installation: Dual tier Ingress

To clean up the installation, use the `kubectl --kubeconfig delete` command to delete each deployment.

To delete the Tier-1 Ingress object, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f tier-1-ingress.yaml

To delete the Tier-2 Ingress object, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f tier-2-ingress.yaml`

To delete the Citrix ADC CPX deployment along with the sidecar Citrix ingress controller, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cpx-cic.yaml

To delete the Citrix ADC CPX service deployment, use the following command:

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cpx-service.yaml

To delete the stand-alone Citrix ingress controller use the following command:

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f cic.yaml

To delete the Apache microservice, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete -f apache.yaml

To delete the Kubernetes secret, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete secret anthos-citrix

To delete the `nslogin` secret, use the following command.

        kubectl --kubeconfig /home/ubuntu/user-cluster-1-kubeconfig delete secret nslogin`
