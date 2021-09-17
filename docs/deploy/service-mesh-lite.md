# Service Mesh lite

An Ingress solution (either hardware or virtualized or containerized) typically performs L7 proxy functions for north-south (N-S) traffic. The Service Mesh lite architecture uses the same Ingress solution to manage east-west traffic as well.

In a standard Kubernetes deployment, east-west (E-W) traffic traverses the built-in kube-proxy deployed in each node. Kube-proxy is an L4 proxy that can only perform TCP/UDP based load balancing and cannot offer the benefits provided by an L7 proxy.

Citrix ADC (MPX, VPX, or CPX) can provide the benefits of L7 proxy for E-W traffic such as:

-  Mutual TLS and SSL offload.
-  Content based routing, allow or block traffic based on HTTP and HTTPS header parameters.
-  Advanced load balancing algorithms (least connections or least response time).
-  Observability of east-west traffic through measuring golden signals (errors, latencies, saturation, traffic volume). Citrix ADM Service Graph is an observability solution to monitor and debug microservices.

A Service Mesh architecture (such as Istio or LinkerD) is complex to manage. Service Mesh lite architecture is a lightweight version and much simpler to get started to achieve the same requirements.

To configure east-west communication with Citrix ADC CPX in a Service mesh lite architecture, you must first understand how the kube-proxy is configured to manage east-west traffic.

## East-west communication with kube-proxy

When you create a Kubernetes deployment for a microservice, Kubernetes deploys a set of pods based on the replica count. To access those pods, you create a Kubernetes service which provides an abstraction to access those pods. The abstraction is provided by assigning a Cluster IP address to the service.

Kubernetes DNS gets populated with an address record that maps the service name with the Cluster IP address. So, when an application, say `tea` wants to access a microservice named `coffee` then DNS returns the Cluster IP address of the `coffee` service to the `tea` application. The `tea` application initiates a connection which is then intercepted by kube-proxy to load balance it to a set of `coffee` pods.

![Kube-proxy](../media/coffee-service.png)

## East-west communication with Citrix ADC CPX in Service Mesh Lite architecture

The goal is to insert the Citrix ADC CPX in the east-west path and use the Ingress rules to control this traffic. 

Perform the following steps to configure east-west communication with Citrix ADC CPX.

### Step 1: Modify the coffee service definition to point to Citrix ADC CPX

For Citrix ADC CPX to manage east-west traffic, the FQDN of the microservice (for example, `coffee`) should point to the Citrix ADC CPX IP address instead of the Cluster IP of the target microservice (`coffee`). (This Citrix ADC CPX deployment can be the same as the Ingress Citrix ADC CPX device.) After this modification, when a pod in the Kubernetes cluster resolves the FQDN for the coffee service, the IP address of the Citrix ADC CPX is returned.

![Modify coffee service](../media/coffee-svs-cpx.png)

> **Note:**
> If you are deploying service mesh lite to bring up the service graph in Citrix ADM for observability,
> then you should add the label `citrix-adc: cpx` in all the services of your application which are pointing to the Citrix ADC CPX IP address after modifying the service.

### Step 2: Create a headless service named  `coffee-headless` for coffee microservice pods

Since you have modified the `coffee` service to point to Citrix ADC CPX, you need to create one more service that represents coffee microservice deployment.

The following is a sample headless service resource:

```yml
apiVersion: v1
kind: Service
metadata:
  name: coffee-headless
spec:
#headless Service
  clusterIP: None
  ports:
  - name: coffee-443
    port: 443
    targetPort: 443
  selector:
    name: coffee-deployment
```

### Step 3: Create an Ingress resource with rules for "`coffee-headless`" service

With the changes in the previous steps, you are now ready to create an Ingress object that configures the Citrix ADC CPX to control the east-west traffic to the coffee microservice pods.

The following is a sample Ingress resource:

![Sample](../media/coffee-headless.png)

Using the usual Ingress load balancing methodology with these changes, Citrix ADC CPX can now load balance the east-west traffic. The following diagrams show how the Citrix ADC CPX Service Mesh Lite architecture provides L7 proxying for east-west communication between `tea` and `coffee` microservices using the Ingress rules:

![Sample](../media/coffee-micro-summary.png)

## East-west communication with Citrix ADC MPX or VPX in Service Mesh lite architecture

Citrix ADC MPX or VPX acting as an Ingress can also load balance east-west microservice communication in a similar way as mentioned in the previous section with slight modifications. The following procedure shows how to achieve the same.

### Step 1: Create an external service resolving the coffee host name to Citrix ADC MPX/VPX IP address

There are two ways to do it. You can add an external service mapping a host name or by using an IP address.

#### Mapping by a host name (CNAME)

-  Create a domain name for the Ingress endpoint IP address(Content Switching virtual server IP address) in Citrix ADC MPX or VPX (for example, `myadc–instance1.us-east-1.mydomain.com`) and update it in your DNS server.
-  Create a Kubernetes service for `coffee` with `externalName` as `myadc–instance1.us-east-1.mydomain.com`.
-  Now, when any pod looks up for the `coffee` microservice a `CNAME`(`myadc–instance1.us-east-1.mydomain.com`) is returned.

```yml
kind: Service
apiVersion: v1
metadata:
name: coffee
spec:
type: ExternalName
externalName: myadc–instance1.us-east-1.mydomain.com
```

#### Mapping a host name to an IP address

When you want your application to use the host name `coffee` that will redirect to the virtual IP address hosted in Citrix ADC MPX or VPX, you can create the following:

```yml
---
kind: "Service"
apiVersion: "v1"
metadata:
  name: "coffee"
spec:
  ports:
    -
      name: "coffee"
      protocol: "TCP"
      port: 80
---
kind: "Endpoints"
apiVersion: "v1"
metadata:
  name: "coffee"
subsets:
  -
    addresses:
      -
        ip: "1.1.1.1" # Ingress IP in MPX
    ports:
      -
        port: 80
        name: "coffee"
```

### Step 2: Create a headless service “`coffee-headless`” for the "`coffee`" microservice pods

Since you have modified the coffee service to point to Citrix ADC MPX, you need to create one more service that represents coffee microservice deployment.

### Step 3: Create an Ingress resource with rules for `coffee-headless` service having the "`ingress.citrix.com/frontend-ip`" annotation
  
Create an Ingress resource using the `ingress.citrix.com/frontend-ip` annotation where the value matches the Ingress endpoint IP address in Citrix ADC MPX or VPX.

Now, you can create an Ingress object that configures the Citrix ADC MPX or VPX to control the east-west traffic to the coffee microservice pods.

The following is a sample ingress resource:

![Sample](../media/coffee-headless-ingress.png)

Using the usual ingress load balancing methodology with these changes Citrix ADC MPX can now load balance east-west traffic. The following diagram shows a Citrix ADC MPX or VPX configured as the N-S and E-W proxy using the Ingress rules.

![Sample](../media/image006.png)

## Automated deployment of applications in Service Mesh lite

To deploy an application in a Service Mesh lite architecture, you need to perform multiple tasks manually. However, when you want to deploy multiple applications which consist of several microservices, you have an easier way to deploy the services in a Service Mesh lite architecture. Citrix provides you an automated way to generate ready to deploy YAMLs.

[This](https://github.com/citrix/citrix-k8s-ingress-controller/blob/smlUpdate/docs/deploy/service-mesh-lite-script.md) doc provides information on how to generate all the necessary YAMLs for Service Mesh lite deployment from your existing YAMLs using the Citrix provided script.
