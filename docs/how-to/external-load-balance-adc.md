# Traffic management for external services

Sometimes, all the available services of an application may not be deployed completely on a single Kubernetes cluster. You may have applications that rely on the services outside of one cluster as well. In this case, micro services need to define an [ExternalName](https://kubernetes.io/docs/concepts/services-networking/service/#externalname) service to resolve the domain name. However, in this approach, you would not be able to get features such as traffic management, policy enforcement, fail over management and so on. As an alternative, you can configure Netscaler to resolve the domain names and leverage the features of Netscaler.

## Configure Netscaler to reach external services

You can configure Netscaler as a domain name resolver using Netscaler ingress controller. When you configure Netscaler as domain name resolver, you need to resolve:

 - Reachability of Netscaler from microservices
 - Domain name resolution at Netscaler to reach external services

### Configure a service for reachability from Kubernetes cluster to Netscaler

To reach Netscaler from microservices, you have to define a headless service which would be resolved to a Netscaler service and thus the connectivity between microservices and Netscaler establishes.

    apiversion: v1
    kind: Service
    metadata: 
      name: external-svc
    spec:
      selector:
        app: cpx
      ports:
        - protocol: TCP
          port: 80

### Configure Netscaler as a domain name resolver using Netscaler ingress controller

You can configure Netscaler through Netscaler ingress controller to create a domain based service group using the ingress annotation `ingress.citrix.com/external-service`. The value for `ingress.citrix.com/external-service` is a list of external name services with their corresponding domain names. For Netscaler VPX, name servers are configured on Netscaler using the ConfigMap.

**Note:** ConfigMaps are used to configure name servers on Netscaler only for Netscaler VPX. For Netscaler CPX, CoreDNS forwards the name resolution request to the upstream DNS server.

### Traffic management using Netscaler CPX

The following diagram explains Netscaler CPX deployment to reach external services. An Ingress is deployed where the external service annotation is specified to configure DNS on Netscaler CPX.

**Note:**
A ConfigMap is used to configure name servers on Netscaler VPX.

![Traffic management with Netscaler CPX](../media/cpx-traffic.png)

In this deployment:

1. A microservice sends the DNS query for www.externalsvc.com which would get resolved to the Netscaler CPX service.
2. Netscaler CPX resolves www.externalsvc.com and reaches external service.

Following are the steps to configure Netscaler CPX to load balance external services:

1. Define a headless service to reach Netscaler.

        apiVersion: v1
        kind: Service
        metadata:
          name: external-svc
        spec:
          selector:
            app: cpx
          ports:
            - protocol: TCP
              port: 80

1. Define an ingress and specify the external-service annotation as specified in the [dbs-ingress.yaml](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/example/load-balance-external/db-ingress.yaml) file. When you specify this annotation, Netscaler ingress controller creates DNS servers on Netscaler and binds the servers to the corresponding service group.


            annotations:
              ingress.citrix.com/external-service: '{"external-svc": {"domain": "www.externalsvc.com"}}'

1. Add the IP address of the DNS server on Netscaler using ConfigMap.

   **Note:** This step is applicable only for Netscaler VPX.

    ```
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: nameserver-cmap
      namespace: default
    data:
      NS_DNS_NAMESERVER: '[]'
    ```
  