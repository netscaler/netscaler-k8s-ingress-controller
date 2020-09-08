# SSL certificate for services of type LoadBalancer through Kubernetes secret resource

This section provides information on how to use the SSL certificate stored as
a Kubernetes secret with services of type LoadBalancer. The certificate is applied if the annotation `service.citrix.com/service-type` is `SSL` or `SSL_TCP`.

## Using the Citrix ingress controller default certificate

If the SSL certificate is not provided, you can use the default Citrix ingress controller certificate.

You must provide the secret name you want to use and the namespace from which it should be taken as arguments in the Citrix ingress controller YAML file.

Default Citrix ingress controller

            --default-ssl-certificate <NAMESPACE>/<SECRET_NAME> 

## Service annotations for SSL certificate as Kubernetes secrets

The Citrix ingress controller provides the following service annotations to use SSL certificates stored as Kubernetes secrets for services of type `LoadBalancer`.

| Service annotation | Description|
| ---------------- | ------------ |
| `service.citrix.com/secret` | Use this annotation to specify the name of the secret resource for the front-end server certificate. It must contain a certificate and key. You can also provide a list of intermediate CA certificates in the certificate section followed by the server certificate. These intermediate CAs are automatically linked and sent to the client during the SSL handshake.  |
| `service.citrix.com/ca-secret`| Use this annotation to provide a CA certificate for client certificate authentication.  This certificate is bound to the front-end SSL virtual server in Citrix ADC.|
| `service.citrix.com/backend-secret`| Use this annotation if the back-end communication between Citrix ADC and your workload is on an encrypted channel, and you need the client authentication in your workload. This certificate is sent to the server during the SSL handshake and it is bound to the back end SSL service group.|
| `service.citrix.com/backend-ca-secret`| Use this annotation to enable server authentication which authenticates the back-end server certificate. This configuration binds the CA certificate of the server to the SSL service on the Citrix ADC. |
| `service.citrix.com/preconfigured-certkey`| Use this annotation to specify the name of the preconfigured cert key in the Citrix ADC to be used as a front-end server certificate. |
|`service.citrix.com/preconfigured-ca-certkey`| Use this annotation to specify the name of the preconfigured cert key in the Citrix ADC to be used as a CA certificate for client certificate authentication. This certificate is bound to the front-end SSL virtual server in Citrix ADC. |
|`service.citrix.com/preconfigured-backend-certkey`| Use this annotation to specify the name of the preconfigured cert key in the Citrix ADC to be bound to the back-end SSL service group. This certificate is sent to the server during the SSL handshake for server authentication.|
|`service.citrix.com/preconfigured-backend-ca-certkey`| Use this annotation to specify the name of the preconfigured CA cert key in the Citrix ADC to bound to back-end SSL service group for server authentication.|


### Examples: Front-end secret and Front-end CA secret

Following are some examples for the `service.citrix.com/secret` annotation:

The following annotation is applicable to all ports in the service.

            service.citrix.com/secret: hotdrink-secret

You can use the following notation to specify the certificate applicable to specific ports by giving either `portname` or `port`-`protocol` as key.

            # port-protocol : secret

            service.citrix.com/secret: '{"443-tcp": "hotdrink-secret", "8443-tcp": "hotdrink-secret"}' 

             # portname: secret

            service.citrix.com/secret: '{"https": "hotdrink-secret"}' 


Following are some examples for the `service.citrix.com/ca-secret` annotation.

You need to specify the following annotation to attach the generated CA secret which is used for client certificate authentication for a service deployed in Kubernetes.

The following annotation is applicable to all ports in the service.


      service.citrix.com/ca-secret: hotdrink-ca-secret

You can use the following notation to specify the certificate applicable to specific ports by giving either `portname` or `port`-`protocol` as key.

      # port-protocol: secret
      service.citrix.com/ca-secret: '{"443-tcp": "hotdrink-ca-secret", "8443-tcp": "hotdrink-ca-secret"}'      

      # portname: secret

      service.citrix.com/ca-secret: '{"https": "hotdrink-ca-secret"}' 

### Examples: back-end secret and back-end CA secret

Following are some examples for the `service.citrix.com/backend-secret` annotation.


      # port-protocol: secret
      service.citrix.com/backend-secret: '{"443-tcp": "hotdrink-secret", "8443-tcp": "hotdrink-secret"}'      

      # portname: secret

      service.citrix.com/backend-secret: '{"tea-443": "hotdrink-secret", "tea-8443": "hotdrink-secret"}' 

      # applicable to all ports

      service.citrix.com/backend-secret: "hotdrink-secret"

Following are some examples for the `service.citrix.com/backend-ca-secret` annotation.

      # port-proto: secret
      service.citrix.com/backend-ca-secret: '{"443-tcp": "coffee-ca", "8443-tcp": "tea-ca"}'      

      # portname: secret

      service.citrix.com/backend-ca-secret: '{"coffee-443": "coffee-ca", "tea-8443": "tea-ca"}' 

      # applicable to all ports

      service.citrix.com/backend-ca-secret: "hotdrink-ca-secret"
