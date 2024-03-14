# TLS client and server authentication

This topic provides information about TLS client and server authentication.

## TLS client authentication

In TLS client authentication, a server requests a valid certificate from the client for authentication and ensures that it is only accessible by authorized machines and users.
You can enable the TLS client authentication using NetScaler SSL-based virtual servers. With client authentication enabled on a NetScaler SSL virtual server, the NetScaler asks for the client certificate during the SSL handshake. The appliance checks the certificate presented by the client for normal constraints, such as the issuer signature and expiration date.

TLS client authentication can be set to mandatory, or optional. If the SSL client authentication is set as mandatory and the SSL client does not provide a valid client certificate, then the connection is dropped. A valid client certificate means that it is signed or issued by a specific Certificate Authority, and not expired or revoked. If it is marked as optional, then the NetScaler requests the client certificate, but the connection is not dropped. The NetScaler proceeds with the SSL transaction even if the client does not present a certificate or the certificate is invalid. The optional configuration is useful for authentication scenarios like two-factor authentication.

### Configuring TLS client authentication

Create a Kubernetes certificate for the CA certificate with which client certificates are generated.

            kubectl create secret generic tls-ca --from-file=tls.crt=cacerts.pem -n netscaler

**Note:** You must specify `tls.crt=` while creating a secret. This file is used by the Citrix ingress controller while parsing a CA secret.

You need to specify the `ingress.citrix.com/frontend_sslprofile` annotation to attach the generated CA secret which is used for the client certificate authentication for a service deployed in Kubernetes. For client authentication `clientauth` should be enabled using the `ingress.citrix.com/frontend_sslprofile` annotation. To know more about the SSL profile, see the [SSL profile documentation](./SSL-profile.md).

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            ingress.citrix.com/ca-secret: '{"ingress-demo": "tls-ca"}'
            ingress.citrix.com/frontend_sslprofile: '{"clientauth":"ENABLED", "sni": "enabled"}'
          name: ingress-demo
          namespace: netscaler
        spec:
          ingressClassName: netscaler
          rules:
          - host: example.com
            http:
              paths:
              - backend:
                  service:
                    name: service-test
                    port:
                      number: 80
                path: /
                pathType: Prefix
          tls:
          - secretName: tls-secret
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---
        

## TLS server authentication

[Server authentication](https://docs.citrix.com/en-us/citrix-adc/13/ssl/server-authentication.html) allows a client to verify the authenticity of the web server that it is accessing.
Usually, the NetScaler appliance performs SSL offloading and acceleration on behalf of a web server and does not authenticate the certificate of the web server. However, you can authenticate the server in deployments that require end-to-end SSL encryption.

In such a situation, the NetScaler appliance becomes the SSL client and performs the following:

-  carries out a secure transaction with the SSL server
-  verifies that a CA whose certificate is bound to the SSL service has signed the server certificate
-  checks the validity of the server certificate.

To authenticate the server, you must first enable server authentication and then bind the certificate of the CA that signed the certificate of the server to the SSL service on the NetScaler appliance. When you bind the certificate, you must specify the bind as a CA option.

### Configuring TLS server authentication

Perform the following steps to generate a Kubernetes secret for an existing certificate:

1.  Generate a Kubernetes secret for the pre-existing client certificate which is used with the back-end service.

        kubectl create secret tls tls-example-test --cert=path/to/tls.cert --key=path/to/tls.key -n netscaler

1.  Generate a secret for an existing CA certificate. This certificate is required to sign the back end server certificate.

        kubectl create secret generic example-test-ca --from-file=tls.crt=cacerts.pem -n netscaler

    **Note:** You must specify 'tls.crt=' while creating a secret. This file is used by Citrix ingress controller while parsing a CA secret.

1.  Create and apply the Ingress configuration.

     To enable the TLS server authentication, set the `ingress.citrix.com/secure-backend` annotation in the ingress as `True`. The `ingress.citrix.com/backend-secret` annotation is used to provide the certificate for back-end server communication from NetScaler. Also, CA certificate can be provided using the `ingress.citrix.com/backend-ca-secret` annotation and the back end SSL profile can be used to enable server authentication.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            ingress.citrix.com/backend-ca-secret: '{"service-test":"example-test-ca"}'
            ingress.citrix.com/backend-secret: '{"service-test": "tls-example-test"}'
            ingress.citrix.com/backend-sslprofile: '{"service-test":{"serverauth": "enabled",
              "sni": "enabled"}}'
            ingress.citrix.com/ca-secret: '{"ingress-demo": "tls-ca"}'
            ingress.citrix.com/frontend_sslprofile: '{"clientauth":"ENABLED", "sni": "enabled"}'
            ingress.citrix.com/secure-backend: 'True'
          name: ingress-demo
          namespace: netscaler
        spec:
          ingressClassName: netscaler
          rules:
          - host: example.com
            http:
              paths:
              - backend:
                  service:
                    name: service-test
                    port:
                      number: 443
                path: /
                pathType: Prefix
          tls:
          - secretName: tls-secret
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---


**Note:** SNI can be enabled or disabled based on the certificate.