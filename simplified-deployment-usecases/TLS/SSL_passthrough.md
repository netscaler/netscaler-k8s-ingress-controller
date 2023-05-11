# SSL Passthrough

SSL passthrough feature allows you to pass incoming security sockets layer (SSL) requests directly to a server for decryption rather than decrypting the request using a load balancer. SSL passthrough is widely used for web application security and it uses the TCP mode to pass encrypted data to servers.

The proxy SSL passthrough configuration does not require the installation of an SSL certificate on the load balancer. SSL certificates are installed on the back end server as they handle the SSL connection instead of the load balancer.

The following diagram explains the SSL passthrough feature.

![SSL Passthrough](../../docs/media/ssl-passthrough.png)

As shown in this diagram, SSL traffic is not terminated at the NetScaler and SSL traffic is passed through the NetScaler to the back end server. SSL certificate at the back end server is used for the SSL handshake.

The Citrix ingress controller provides the following Ingress annotation that you can use to enable SSL passthrough on the Ingress NetScaler:

    ingress.citrix.com/ssl-passthrough: 'True|False'

The default value of the annotation is `False`.

SSL passthrough is enabled for all services or host names provided in the Ingress definition. SSL passthrough uses host name (wildcard host name is also supported) and ignores paths given in Ingress.

**Note:** The Citrix ingress controller does not support SSL passthrough for non-hostname based Ingress. Also, SSL passthrough is not valid for default back end Ingress.

To configure SSL passthrough on the Ingress NetScaler, you must define the `ingress.citrix.com/ssl-passthrough:` as shown in the following sample Ingress definition. You must also enable TLS for the host as shown in the example.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
        annotations:
            kubernetes.io/ingress.class: "netscaler"
             # annotation ingress.citrix.com/insecure-termination will redirect HTTP traffic to secure TLS.
            ingress.citrix.com/insecure-termination: redirect
            # annotation ingress.citrix.com/secure-backend will enable secure back end communication to the backend service.
            ingress.citrix.com/secure-backend: "True"
            # annotaion ingress.citrix.com/ssl-passthrough will enable SSL passthrough
            ingress.citrix.com/ssl-passthrough: "True"
        name: ssl-passthrough-example
        spec:
        rules:
        - host: www.exampletest.com
            http:
            paths:
            - backend:
                service:
                    name: example-test
                    port:
                    number: 443
                path: /
                pathType: Prefix
        tls:
        - secretName: tls-example-test