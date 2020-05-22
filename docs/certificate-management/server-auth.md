# TLS server authentication support in Citrix ADC using the Citrix ingress controller

[Server authentication](https://docs.citrix.com/en-us/citrix-adc/13/ssl/server-authentication.html) allows a client to verify the authenticity of the web server that it is accessing.
Usually, the Citrix ADC device performs SSL offload and acceleration on behalf of a web server and does not authenticate the certificate of the Web server. However, you can authenticate the server in deployments that require end-to-end SSL encryption.

In such a situation, the Citrix ADC device becomes the SSL client and performs the following:

- carries out a secure transaction with the SSL server
- verifies that a CA whose certificate is bound to the SSL service has signed the server certificate
- checks the validity of the server certificate.

To authenticate the server, you must first enable server authentication and then bind the certificate of the CA that signed the certificate of the server to the SSL service on the Citrix ADC appliance. When you bind the certificate, you must specify the bind as a CA option.

## Configuring TLS server authentication

Perform the following steps to configure TLS server authentication.

1. Enable the TLS support in Citrix ADC.

     The Citrix ingress controller uses the **TLS** section in the Ingress definition as an enabler for TLS support with Citrix ADC.
     The following is a sample snippet of the Ingress definition:



        spec:
          tls:
           - secretName:

2. To generate a Kubernetes secret for an existing certificate, perform the following.


    1. Generate a client certificate to be used with the service.

            $ kubectl create secret tls tea-beverage --cert=path/to/tls.cert --key=path/to/tls.key --namespace=default

    2. Generate a secret for an existing CA certificate. This certificate is required to sign the back end server certificate.


            $ kubectl create secret generic tea-ca --from-file=tls.crt=cacerts.pem

     **Note:** You must specify `tls.crt=` while creating a secret. This file is used by the Citrix ingress controller while parsing a CA secret.

3.  Enable secure back end communication to the service using the following annotation in the Ingress configuration.
   

         ingress.citrix.com/secure-backend: "True" 

4.  Use the following annotation to bind the certificate to SSL service. This certificate is used when the Citrix ADC acts as a client to send the request to the back end server.


        ingress.citrix.com/backend-secret: '{"tea-beverage": "tea-beverage", "coffee-beverage": "coffee-beverage"}'

5. To enable server authentication which authenticates the back end server certificate, you can use the following annotation. This configuration binds the CA certificate of the server to the SSL service on the Citrix ADC.  
 

         ingress.citrix.com/backend-ca-secret: '{"coffee-beverage":"coffee-ca", "tea-beverage":"tea-ca"}


