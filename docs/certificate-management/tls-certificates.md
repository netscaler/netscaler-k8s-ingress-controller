# TLS certificates handling in Citrix ingress controller

Citrix ingress controller provides option to configure TLS certificates for Citrix ADC SSL-based virtual servers. The SSL virtual server intercepts SSL traffic, decrypts it and processes it before sending it to services that are bound to the virtual server.

By default, SSL virtual server can bind to one default certificate and the application receives the traffic based on the policy bound to the certificate. However, you have the Server Name Indication (SNI) option to bind multiple certificates to a single virtual server. Citrix ADC determines which certificate to present to the client based on the domain name in the TLS handshake.

Citrix ingress controller handles the certificates in the following three ways:

-  [Citrix ingress controller default Certificate](#citrix-ingress-controller-default-certificate)
-  [Preconfigured certificates](#preconfigured-certificates)
-  [TLS Section in the Ingress YAML](#tls-section-in-the-ingress-yaml)

## Prerequisite

For handling TLS certificates using Citrix ingress controller, you need to [enable TLS support in Citrix ADC](#enable-tls-support-in-citrix-adc-for-the-application) for the application and also if you are using certificates in your Kubernetes deployment then you need to [generate Kubernetes secret using the certificate](#generate-kubernetes-secret).

### Enable TLS support in Citrix ADC for the application

Citrix Ingress Controller uses the **TLS** section in the ingress definition as an enabler for TLS support with Citrix ADC.

!!! note "Note"
    In case of Default certificate or Preconfigured certificates, you need to add an empty secrete in the ***spec.tls.secretname*** field in your ingress definition to enable TLS.

The following sample snippet of the ingress definition:

```yml
spec:
  tls:
  - secretName:
```

### Generate Kubernetes secret

To generate Kubernetes secret for an existing certificate, use the following `kubectl` command:

        $ kubectl create secret tls k8s-secret --cert=path/to/tls.cert --key=path/to/tls.key  --namespace=default

        secret “k8s-secret” created

The command creates a Kubernetes secret with a PEM formatted certificate under `tls.crt` key and a PEM formatted private key under `tls.key` key.

Alternatively, you can also generate the Kubernetes secret using the following YAML definition:

```yml
apiVersion: v1
kind: Secret
metadata:
  name: k8s-secret
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
```

Deploy the YAML using the `kubectl -create <file-name>` command. It creates a Kubernetes secret with a PEM formatted certificate under `tls.crt` key and a PEM formatted private key under `tls.key` key. 

## Citrix ingress controller default certificate

The Citrix ingress controller default certificate is used to provide a secret on Kubernetes that needs to be used as a non-SNI certificate. You must provide the secret name to be used and namespace from which it should be taken as arguments in the `.yaml` file of the Citrix ingress controller:

        --default-ssl-certificate <NAMESPACE>/<SECRET_NAME>

The following is a sample Citrix ingress controller YAML definition file that contains a TLS secret (`hotdrink.secret`) picked from the `ssl` namespace and provided as the Citrix ingress controller default certificate.

!!! note "Note"
     NAMESPACE is mandatory along with a valid SECRET_NAME.

```yml
apiVersion: v1
kind: Pod
metadata:
  name: cic
  labels:
    app: cic
spec:
      serviceAccountName: cpx
      containers:
      - name: cic
        image: "xxxx"
        imagePullPolicy: Always
        args:
        - --default-ssl-certificate
          ssl/hotdrink.secret
        env:
        # Set Citrix ADM Management IP
        - name: "NS_IP"
          value: "xx.xx.xx.xx"
        # Set port for Nitro
        - name: "NS_PORT"
          value: "xx"
        # Set Protocol for Nitro
        - name: "NS_PROTOCOL"
          value: "HTTP"
        # Set username for Nitro
        - name: "NS_USER"
          value: "nsroot"
        # Set user password for Nitro
        - name: "NS_PASSWORD"
          value: "nsroot"
```

## Preconfigured certificates

Citrix ingress controller allows you to use the certkeys that are already configured on the Citrix ADC. You must provide the details about the certificate using the following annotation in your ingress definition:

        ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "<name>", "type": "default|sni|ca"} ] }'

You can provide details about multiple certificates as a list within the annotation. Also, you can define the way the certificate is treated. In the following sample annotation, certkey1 is used as a non-SNI certificate and certkey2 is used as an SNI certificate:

        ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "certkey1", "type": "default"}, {"name": "certkey2", "type": "sni"} ] }’

If the type parameter is not provided with the name of a certificate, then it is considered as the default (non-SNI) type.

!!! tip "Important"
    1.  Ensure that you use this feature in cases where you want to reuse the certificates that are present on the Citrix ADC and bind them to the applications that are managed by Citrix ingress controller.
    1.  Citrix ingress controller does not manage the life cycle of the certificates. That is, it does not create or delete the certificates, but only binds them to the necessary applications.

## TLS Section in the Ingress YAML

Kubernetes allows you to provide the TLS secrets in the `spec:` section of an ingress definition. This section describes how the Citrix ingress controller uses these secrets.

### With the host section

If the secret name is provided with the host section, Citrix ingress controller binds the secret as an SNI certificate.

```yml
spec:
  tls:
  - secretName: fruitjuice.secret
    hosts: items.fruit.juice
```

### Without the host section

If the secret name is provided without the host section, Citrix ingress controller binds the secret as a default certificate.

```yml
spec:
  tls:
  - secretName: colddrink.secret
```

!!! note "Note"
    If there are more than one secret given then Citrix ingress controller binds all the certificates as SNI enabled certificates.

## Points to note

1.  In cases wherein if multiple secrets are provided to the Citrix ingress controller the following precedence is followed:

        default-ssl-certificate < preconfigured-default-certkey or non-host tls secret.

1.  If there is a conflict in precedence among the same grade certificates (for example, two ingress files configure a non-host TLS secret each, as default/non-SNI type), then the Citrix ingress controller binds the Citrix ingress controller default certificate as the non-SNI certificate and uses all other certificates with SNI.

1.  Certificate used for secret given under TLS section must have CN name otherwise it does not bind to Citrix ADC.

1.  If SNI enabled for SSL virtual server then:

    -  Non-SNI (Default) certificate is used for the following HTTPs requests:

            curl -1 -v -k https://1.1.1.1/

            curl -1 -v -k -H 'HOST:*.colddrink.beverages' https://1.1.1.1/

    -  SNI enabled certificate is used for request with full domain name

            curl -1 -v -k https://items.colddrink.beverages/

       If any request received that does not match with certificates CN name fails.