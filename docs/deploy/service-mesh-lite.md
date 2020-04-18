# Service Mesh lite

An Ingress solution (either hardware or virtualized or containerized) typically performs L7 proxy functions for north-south (N-S) traffic. The Service Mesh lite architecture uses the same Ingress solution to manage east-west traffic as well.

In a standard Kubernetes deployment, east-west (E-W) traffic traverses the built-in KubeProxy deployed in each node. KubeProxy being a L4 proxy can only do TCP/UDP based load balancing without the benefits of L7 proxy.

Citrix ADC (MPX, VPX, SDX, or CPX) can provide such benefits for E-W traffic such as:

-  Mutual TLS, SSL offload
-  Content based routing, Allow/Block traffic based on HTTP, HTTPS header parameters
-  Advanced load balancing algorithms (least connections, least response time)
-  Observability of east-west traffic through measuring golden signals (errors, latencies, saturation, traffic volume). Citrix ADM’s Service Graph is an observability solution to monitor and debug microservices.

A Service Mesh architecture (like Istio or LinkerD) can be complex to manage. Service Mesh lite architecture is much simpler to get started to achieve the same requirements.

Let’s start by looking at how KubeProxy is configured to manage east-west traffic.

## East-west communication with KubeProxy

When you create a Kubernetes deployment for a microservice, Kubernetes deploys a set of pods based on the replica count. To access those pods, you create a Kubernetes service which provides an abstraction to access those pods. The abstraction is provided by assigning a Cluster IP address to the service.

Kubernetes DNS gets populated with an address record that maps the service name with the Cluster IP. So, when an application lets say `tea` wants to access a microservice (let’s say) `coffee` then DNS returns the Cluster IP of `coffee` service to `tea` application. The `Tea` application initiates a connection which is then intercepted by KubeProxy to load balance it to a set of `coffee` pods.

![KubeProxy](../media/coffee-service.png)

## East-west communication with Citrix ADC CPX in Service Mesh Lite architecture

The goal is to insert the Citrix ADC CPX in the east-west path and use Ingress rules to control this traffic. The steps are:

### Step 1: Modify the coffee service definition to point to Citrix ADC CPX

For Citrix ADC CPX to manage east-west traffic, the FQDN of the microservice (for example, `coffee` as mentioned above) should point to Citrix ADC CPX IP address instead of the Cluster IP of the target microservice (`coffee`). (This Citrix ADC CPX deployment can be the same as the Ingress Citrix ADC CPX device.) After this modification, when a pod in the Kubernetes cluster resolves the FQDN for the coffee service, the IP address of the Citrix ADC CPX is returned.

![Modify coffee service](../media/coffee-svs-cpx.png)

## Step 2: Create a headless service “`coffee-headless`” for coffee microservice pods

Since we have modified `coffee` service to point to Citrix ADC CPX, we need to create one more service that represents coffee microservice deployment.

A sample headless service resource is given below.

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

### Step 3: Create an ingress resource with rules for "`coffee-headless`" service

With the above changes, we are now ready to create an ingress object that configures the Citrix ADC CPX to control the east-west traffic to the coffee microservice pods.

A sample ingress resource is given below.

![Sample](../media/coffee-headless.png)

Using the usual Ingress load balancing methodology with above changes, Citrix ADC CPX can now load balance east-west traffic. The following diagrams show how Citrix ADC CPX Service Mesh Lite architecture provides L7 proxying for east-west communication between `tea` and `coffee` microservices using Ingress rules:

![Sample](../media/coffee-micro-summary.png)

## East-west communication with Citrix ADC MPX or VPX in Service Mesh Lite architecture

Citrix ADC MPX or VPX acting as an ingress can also load balance east-west microservice communication in a similar way as mentioned above with slight modifications. The below procedure shows how to achieve the same.

### Step 1: Create external service resolving the coffee host name to Citrix ADC MPX/VPX IP address

There are two ways to do it. You can add an external service mapping a host name or by using an IP address.

#### Mapping by a host name (CNAME)

-  Create a domain name for ingress endpoint IP(Content Switching virtual server IP address) in Citrix ADC MPXor VPX lets say `myadc–instance1.us-east-1.mydomain.com` and update it in your DNS server.
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

When you want your application to use the host name `coffee` that will redirect to virtual IP address hosted in Citrix ADC MPX or VPX, you can create the following.

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

Since we have modified coffee service to point to Citrix ADC MPX, we need to create one more service that represents coffee microservice deployment.

### Step 3: Create an ingress resource with rules for “`coffee-headless`” service having the "`ingress.citrix.com/frontend-ip`" annotation
  
Create an ingress resource using `ingress.citrix.com/frontend-ip` annotation where the value matches the ingress endpoint IP address in Citrix ADC MPX or VPX.

With the above changes we are now ready to create an ingress object that configures the Citrix ADC MPX or VPX to control the east-west traffic to the coffee microservice pods.

A sample ingress resource is given below.

![Sample](../media/coffee-headless-ingress.png)

Using the usual ingress load balancing methodology with above changes Citrix ADC MPX can now load balance east-west traffic. The following diagram shows the Citrix ADC MPX or VPX configured as N-S and E-W proxy using ingress rules.

![Sample](../media/image006.png)
