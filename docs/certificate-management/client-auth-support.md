# TLS client authentication support in Citrix ADC

In TLS client authentication, a server requests a valid certificate from the client for authentication and ensures that it is only accessible by authorized machines and users.

You can enable TLS client authentication using Citrix ADC SSL-based virtual servers. With client authentication enabled on a Citrix ADC SSL virtual server, the Citrix ADC asks for the client certificate during the SSL handshake. The appliance checks the certificate presented by the client for normal constraints, such as the issuer signature and expiration date.

The following diagram explains the TLS client authentication feature on Citrix ADC.

![TLS client authentication](../media/ssl-client-authentication.png)

TLS client authentication can be set to mandatory, or optional.
If the SSL client authentication is set as mandatory and the SSL Client does not provide a valid client certificate, then the connection is dropped. A valid client certificate means that it is signed or issued by a specific Certificate Authority, and not expired or revoked.
If it is marked as optional, then the Citrix ADC requests the client certificate, but the connection is not dropped. The Citrix ADC proceeds with the SSL transaction even if the client does not present a certificate or the certificate is invalid. The optional configuration is useful for authentication scenarios like two-factor authentication.

## Configuring TLS client authentication

Perform the following steps to configure TLS client authentication.

1. Enable the TLS support in Citrix ADC.

     The Citrix ingress controller uses the **TLS** section in the Ingress definition as an enabler for TLS support with Citrix ADC.
     The following is a sample snippet of the Ingress definition:



        spec:
          tls:
           - secretName:

1. Apply a CA certificate to the Kubernetes environment.

    To generate a Kubernetes secret for an existing certificate, use the following kubectl command:

           $ kubectl create secret generic tls-ca --from-file=tls.crt=cacerts.pem

     **Note:** You must specify 'tls.crt=' while creating a secret. This file is used by the Citrix ingress controller while parsing a CA secret.

1. Configure Ingress to enable client authentication.

      You need to specify the following annotation to attach the generated CA secret which is used for client certificate authentication for a service deployed in Kubernetes.


          ingress.citrix.com/ca-secret: '{"frontend-hotdrinks": "hotdrink-ca-secret"}' 
   
      By default, client certificate authentication is set to `mandatory` but you can configure it to `optional` using the `frontend_sslprofile` annotation in the front end configuration.

  

          ingress.citrix.com/frontend_sslprofile: '{"clientauth":"ENABLED", “clientcert”: “optional”}'

      **Note:**
      The `frontend_sslprofile` only supports the front end Ingress configuration. For more information, see [front end configuration](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/profiles.md#front-end-configuration).

