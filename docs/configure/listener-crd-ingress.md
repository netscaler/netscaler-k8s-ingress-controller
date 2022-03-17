# Listener CRD support for Ingress through annotation

Ingress is a standard Kubernetes resource that specifies HTTP routing capability to back-end Kubernetes services. Citrix ingress controller provides various annotations to fine-tune the Ingress parameters for both front-end and back-end configurations. For example, using the `ingress.citrix.com/frontend-ip`  annotation you can specify the front-end listener IP address configured in Citrix ADC by Citrix ingress controller. Similarly, there are other front-end annotations to fine-tune HTTP and SSL parameters. When there are multiple Ingress resources and if they share front-end IP and port, specifying these annotations in each Ingress resource is difficult.

Sometimes, there is a separation of responsibility between network operations professionals (NetOps) and developers. NetOps are responsible for coming up with front-end configurations like front-end IP, certificates, and SSL parameters. Developers are responsible for HTTP routing and back-end configurations. Citrix ingress controller already provides [content routing CRDs](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/contentrouting) such as listener CRD for front-end configurations and `HTTProute` for back-end routing logic.
Now, Listener CRD can be applied for Ingress resources using an annotation provided by Citrix.

Through this feature, you can use the Listener CRD for your Ingress resource and separate the creation of the front-end configuration from the Ingress definition. Hence, NetOps can separately define the Listener resource to configure front-end IP, certificates, and other front-end parameters (TCP, HTTP, and SSL). Any configuration changes can be applied to the listener resources without changing each Ingress resource. In Citrix ADC, a listener resource corresponds to content switching virtual servers, SSL virtual servers, certkeys and front-end HTTP, SSL, and TCP profiles.

**Note:** While using this feature, you must ensure that all ingresses with the same front-end IP and port refer to the same Listener resource. For ingresses that use the same front-end IP and port combinations, one Ingress referring to a listener resource and another ingress referring to the `ingress.citrix.com/frontend-ip` annotation is not supported.

## Restrictions

When Listener is used for the front-end configurations, the following annotations are ignored and there may not be any effect:

- `ingress.citrix.com/frontend-ip`
- `Ingress.citrix.com/frontend-ipset-name`
- `ingress.citrix.com/secure-port`
- `ingress.citrix.com/insecure-port`
- `ingress.citrix.com/insecure-termination`
- `ingress.citrix.com/secure-service-type`
- `ingress.citrix.com/insecure-service-type`
- `ingress.citrix.com/csvserver`
- `ingress.citrix.com/frontend-tcpprofile`
- `ingress.citrix.com/frontend-sslprofile`
- `ingress.citrix.com/frontend-httpprofile`

## Deploying a Listener CRD resource for Ingress

Using the `ingress.citrix.com/listener` annotation, you can specify the name and namespace of the Listener resource for the ingress in the form of `namespace/name`. The namespace is not required if the Listener resource is in the same namespace as that of Ingress.

Following is an example for the annotation:

    ingress.citrix.com/listener: default/listener1

Here, `default` is the namespace of the Listener resource and `listener1` is the name of the Listener resource which specifies the front-end parameters.

Perform the following steps to deploy a Listener resource for the Ingress:

1. Create a Listener resource (`listener.yaml`) as follows:

    ```yml
    apiVersion: citrix.com/v1
    kind: Listener
    metadata:
      name: my-listener
      namespace: default
    spec:
      ingressClass: citrix
      vip: '192.168.0.1' # Virtual IP address to be used, not required when CPX is used as ingress device
      port: 443
      protocol: https
      redirectPort: 80
      secondaryVips:
      - "10.0.0.1"
      - "1.1.1.1"
      policies:
        httpprofile:
          config:
            websocket: "ENABLED"
        tcpprofile:
          config:
            sack: "ENABLED"
        sslprofile:
          config:
            ssl3: "ENABLED"
        sslciphers:
        - SECURE
        - MEDIUM
        analyticsprofile:
          config:
          - type: webinsight
            parameters:
              allhttpheaders: "ENABLED"
        csvserverConfig:
          rhistate: 'ACTIVE'
    ```

   Here, the Listener resource `my-listener` in the default namespace specifies the front-end configuration such as VIP, secondary VIPs, HTTP profile, TCP profile, SSL profile, and SSL ciphers. It creates a content switching virtual server in Citrix ADC on port 443 for HTTPS traffic, and all HTTP traffic on port 80 is redirected to HTTPS.

   **Note:** The `vip` field in the Listener resource is not required when Citrix ADC CPX is used as an ingress device. For Citrix ADC VPX, VIP is the same as the pod IP address which is automatically configured by Citrix ingress controller.

1. Apply the Listener resource.

       kubectl apply -f listener.yaml

1. Create an Ingress resource (`ingress.yaml`) by referring to the Listener resource.

    ```yml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: my-ingress
      namespace: default
      annotations:
        ingress.citrix.com/listener: my-listener
        kubernetes.io/ingress.class: "citrix"
    spec:
      tls:
      - secretName: my-secret
        hosts:
        - example.com
      rules:
      - host: example.com
        http:
          paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kuard
                port:
                  number: 80
    ```

   Here, the ingress resource `my-ingress` refers to the Listener resource `my-listener` in the default namespace for front-end configurations.

1. Apply the ingress resource.

       kubectl apply -f ingress.yaml

## Certificate management

There are two ways in which you can specify the certificates for Ingress resources. You can specify the certificates as part of the Ingress resource or provide the certificates as part of the Listener resource.

### Certificate management through Ingress resource

In this approach, all certificates are specified as part of the regular ingress resource as follows. Listener resource does not specify certificates. In this mode, you need to specify certificates as part of the Ingress resource.

   ```yml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: my-ingress
      namespace: default
      annotations:
        ingress.citrix.com/listener: my-listener
        kubernetes.io/ingress.class: "citrix"
    spec:
      tls:
      - secretName: my-secret
        hosts:
        - example.com
      rules:
      - host: example.com
        http:
          paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kuard
                port:
                  number: 80
   ```

### Certificate management through Listener resource

In this approach, certificates are provided as part of the Listener resource. You do not have to specify certificates as part of the Ingress resource.

The following Listener resource example shows certificates.

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: my-listener
  namespace: default
spec:
  ingressClass: citrix
  certificates:
  - secret:
      name: my-secret
    # Secret named 'my-secret' in current namespace bound as default certificate
    default: true
  - secret:
      # Secret 'other-secret' in demo namespace bound as SNI certificate
      name: other-secret
      namespace: demo
  vip: '192.168.0.1' # Virtual IP address to be used, not required when CPX is used as ingress device
  port: 443
  protocol: https
  redirectPort: 80
```

In the Ingress resource, secrets are not specified as shown in the following example.

```yml
 apiVersion: networking.k8s.io/v1
 kind: Ingress
 metadata:
   name: my-ingress
   namespace: default
   annotations:
     ingress.citrix.com/listener: my-listener
     kubernetes.io/ingress.class: "citrix"
 spec:
   tls:
   # TLS field is empty as the certs are specified in Listener
   rules:
   - host: example.com
     http:
       paths:
       - path: /
         pathType: Prefix
         backend:
           service:
             name: kuard
             port:
               number: 80
```
