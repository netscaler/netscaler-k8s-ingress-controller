# Citrix ADC CPX integration with MetalLB in layer 2 mode for on-premises Kubernetes clusters  

Kubernetes service of type `LoadBalancer` support is provided by cloud load balancers in a cloud environment. Cloud service providers enable this support by automatically creates a load balancer and assign an IP address which is displayed as part of the service status. Any traffic destined to the external IP address is load balanced on NodeIP and NodePort by the cloud load balancer.

Citrix provides different options to support the type `LoadBalancer` services in an on-premises environment including:

- Using an external Citrix ADC VPX or Citrix ADC MPX as a tier-1 load balancer to load balance the incoming traffic to Kubernetes services.
For more information on such a deployment, see [Expose services of type LoadBalancer](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).

- Expose applications running in a Kubernetes cluster using the Citrix ADC CPX daemonset running inside the Kubernetes cluster along with a router supporting ECMP over BGP. ECMP router load balances the traffic to multiple Citrix ADC CPX instances. Citrix ADC CPX instances load balances the actual application pods. For more information on such a deployment, see [BGP advertisement of external IP addresses for type LoadBalancer services and Ingresses using Citrix ADC CPX](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/cpx-service-type-lb/).

- Expose the Citrix ADC CPX services as an external IP service with a node external IP address. You can use this option if an external ADC as tier-1 is not feasible, and a BGP router does not exist. In this deployment, Kubernetes routes the traffic coming to the `spec.externalIP` of the Citrix ADC CPX service on service ports to Citrix ADC CPX pods. Ingress resources can be configured using the Citrix ingress controller to perform SSL (Secure Sockets Layer) offloading and load balancing applications. However, this deployment has the major drawback of not being reliable if there is a node failure.  

- Use [MetalLB](https://metallb.universe.tf/) which is a load-balancer implementation for bare metal Kubernetes clusters in the layer 2 mode with Citrix ADC CPX to achieve ingress capability.

This documentation shows how you can leverage MetalLB along with Citrix ADC CPX to achieve ingress capability in bare-metal clusters when the other solutions are not feasible. MetalLB in layer 2 mode configures one node to send all the traffic to the Citrix ADC CPX service. MetalB automatically moves the IP address to a different node if there is a node failure. Thus providing better reliability than the ExternalIP service.

**Note:** MetalLB is still in the beta version. See the official documentation to know about the project maturity and any limitations.

Perform the following steps to deploy Citrix ADC CPX integration with MetalLB in layer 2 mode for on-premises Kubernetes clusters.

1. Install and configure MetalLB
2. Configure MetalLB configuration for layer 2
3. Install Citrix ADC CPX service

## Install and configure MetalLB

First, you should install MetalLB in layer 2 mode. For more information on different types of installations for MetalLB, see the [MetalLB documentation](https://metallb.universe.tf/installation/).

Perform the following steps to install MetalLB:

1. Create a namespace for deploying MetalLB.
   
        kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/namespace.yaml 

2. Deploy MetalLB using the following command.

        kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/metallb.yaml 

3. Perform the following step if you are performing the installation for the first time.

        kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)" 

4. Verify the MetalLB installation and ensure that the speaker and controller is in the running state using the following command:

        kubectl get pods -n metallb-system 

These steps deploy MetalLB to your cluster, under the `metallb-system` namespace.

The MetalLB deployment YAML file contains the following components:

- The metallb-system/controller deployment: This component is the cluster-wide controller that handles IP address assignments.
  
- The metallb-system/speaker daemonset. This component communicates using protocols of your choice to make the services reachable.
  
- Service accounts for the controller and speaker, along with the RBAC permissions that the components need to function.

## MetalLB configuration for Layer 2

Once MetalLB is installed, you should configure the MetalLB for layer 2 mode. MetalLB takes a range of IP addresses to be allocated to the type LoadBalancer services as external IP. In this deployment, a Citrix ADC CPX service acts as a front-end for all other applications. Hence, a single IP address is sufficient.

Create a ConfigMap for MetalLB using the following command where [metallb-config.yaml](./metal-lb-manifests/metallb-config.yaml) is the YAML file with the MetalLB configuration.  

    kubectl create –f metallb-config.yaml 

Following is a sample MetalLB configuration for layer2 mode. In this example, 192.168.1.240-192.168.1.240 is specified as the IP address range.

```
apiVersion: v1 
kind: ConfigMap 
metadata: 
  namespace: metallb-system 
  name: config 
data: 
  config: | 
    address-pools: 
    - name: default 
      protocol: layer2 
      addresses: 
      - 192.168.1.240-192.168.1.240 
```

## Citrix ADC CPX service installation

Once the metal LB is successfully installed, you can install the Citrix ADC CPX deployment and a service of type `LoadBalancer`.

To install Citrix ADC CPX, you can either use the YAML file or Helm charts.

To install Citrix ADC CPX using the YAML file, perform the following steps:

1. Download the Citrix ADC CPX deployment manifests.

        wget https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml 

2. Edit the Citrix ADC CPX deployment YAML:

    - Set the replica count as needed. It is better to have more than one replica for high availability.
    -  Change the service type to `LoadBalancer`.  

3. Apply the edited YAML file using the Kubectl command.
        
        kubectl apply –f citrix-k8s-cpx-ingress.yaml 


4. View the service using the following command:


        kubectl get svc cpx-service -output yaml

    You can see that MetalLB allocates an external IP address to the Citrix ADC CPX service as follows:

```yml
apiVersion: v1 
kind: Service 
metadata: 
  name: cpx-service 
  namespace: default 
spec: 
  clusterIP: 10.107.136.241 
  externalTrafficPolicy: Cluster 
  healthCheckNodePort: 31916 
  ports: 
  - name: http 
    nodePort: 31528 
    port: 80 
    protocol: TCP 
    targetPort: 80 
  - name: https 
    nodePort: 31137 
    port: 443 
    protocol: TCP 
    targetPort: 443 
  selector: 
    app: cpx-ingress 
  sessionAffinity: None 
  type: LoadBalancer 
status: 
  loadBalancer: 
    ingress: 
    - ip: 192.168.1.240 
 ```

## Deploy a sample application

Perform the following steps to deploy a sample application and verify the deployment.

1. Create a sample deployment using the [sample-deployment.yaml](./metal-lb-manifests/sample-deployment.yaml) file.

        kubectl create –f sample-deployment.yaml
 
2. Expose the application with a service using the [sample-service.yaml](./metal-lb-manifests/sample-service.yaml) file.

        kubectl create –f sample-service.yaml  

3. Once the service is created, you can add an ingress resource using the [sample-ingress.yaml](./metal-lb-manifests/sample-ingress.yaml).

        kubectl create –f sample-ingress.yaml  

You can test the Ingress by accessing the application using a `cpx-service` external IP address as follows:

       curl -v http://192.168.1.240 -H ‘host: testdomain.com’ 

## Additional references

For more information on configuration and troubleshooting for MetalLB see the following links:

- [Metal LB troubleshooting](https://metallb.universe.tf/configuration/troubleshooting/)
- [Configuring routing for metal LB in layer 2 mode](https://itnext.io/configuring-routing-for-metallb-in-l2-mode-7ea26e19219e)
