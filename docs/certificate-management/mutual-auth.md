# Mutual authentication

In TLS client authentication, a server requests a valid certificate from the client for authentication and ensures that it is only accessible by authorized machines and users. Server authentication allows a client to verify the authenticity of the web server that it is accessing.

In mutual authentication, two sides of a communication channel verify the identity of each other instead of only one side verifying the other. Hence, when you use mutual authentication a client and a server independently verifies the identity of each other, instead of only the client authenticating the server or vice versa.

Perform the following steps to apply mutual authentication for Ingress:

1.  Enable the default SSL profile on Netscaler.

        set ssl parameter -defaultProfile ENABLED

    **Note:** Make sure that Netscaler ingress controller is restarted after enabling the default profile.

2.  Download the [mutual-auth.yaml](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/example/mutual-auth.yaml) file. This YAML file contains the Ingress resource definition and the SSL annotations.

    The contents of the YAML is as follows:

          ```yml
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              annotations:
                ingress.citrix.com/backend-ca-secret: '{"apache": "tls-ca"}'
                ingress.citrix.com/backend-secret: '{"apache": "wildcard-secret"}'
                ingress.citrix.com/backend-sslprofile: '{"apache":{"serverauth": "enabled", "sni": "enabled"}}'
                ingress.citrix.com/ca-secret: '{"apache": "tls-ca"}'
                ingress.citrix.com/frontend-ip: A.B.C.D
                ingress.citrix.com/frontend-sslprofile: '{"clientauth": "enabled", "sni": "enabled"
                  }'
                ingress.citrix.com/secure_backend: '{"apache": "True"}'
              name: web-ingress
            spec:
              ingressClassName: citrix
              rules:
              - host: www.guestbook.com
                http:
                  paths:
                  - backend:
                      service:
                        name: apache
                        port:
                          number: 443
                    path: /
                    pathType: ImplementationSpecific
              tls:
              - hosts:
                - www.guestbook.com
                secretName: wildcard-secret
            ---
            apiVersion: networking.k8s.io/v1
            kind: IngressClass
            metadata:
              name: citrix
            spec:
              controller: citrix.com/ingress-controller
            ---

          ```

    In this example:

      -  An application named `apache` is used as the back-end service. You can replace it with the application that you are using.

      -  `wildcard-secret` is the associated Kubernetes secret holding the client certificate. This certificate is used when Netscaler acts as a client to send the request to the back end Apache service.

      -  The `tls-ca` secret holds the CA certificate that is used for verification of the client
certificate

      -  Specify the virtual IP address in the `ingress.citrix.com/frontend-ip` annotation.

      -  authSNI needs to be enabled in the back-end and front-end SSL profile annotations for host name matching during the SSL handshake.

      -  The `hosts` field should be populated with the appropriate DNS or FQDN that is used for matching the SNI.

1. Edit the YAML to specify the appropriate IP address, service, and secrets.

        kubectl apply -f mutual-auth.yaml

## Additional information

 The following SSL related annotations are used in this example. For detailed information on these annotations, see [annotations](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/configure/annotations.html).

-  `ingress.citrix.com/frontend-sslprofile` : Creates the front end profile applicable to the entity that receives requests from a client.

-  `ingress.citrix.com/backend-sslprofile`: Creates the back-end SSL profile (server plane).

-  `ingress.citrix.com/secure-backend: "True"`: Enables secure back end communication to the service.

-  `ingress.citrix.com/ca-secret`: Provides a CA certificate for the client certificate verification. This certificate is bound to the front-end SSL virtual server in Netscaler.

-  `ingress.citrix.com/backend-secret`: Use this annotation if the back-end communication between the Netscaler and your workload is on an encrypted channel, and you need the client authentication in your workload. This annotation is bound to the back end SSL service group.

-  `ingress.citrix.com/backend-ca-secret`: Enables server authentication which authenticates the back-end server certificate. This configuration binds the CA certificate of the server to the SSL service on the Netscaler.