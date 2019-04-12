# TLS Certificates in Citrix Ingress Controller

Citrix Ingress Controller (CIC) can configure tls secrets provided to it from Kubernetes as SSL certkeys on the Citrix ADC. To enable this feature, you need to add the following section in the ingress definition:

```yaml
spec:
  tls:
  - secretName:
```

CIC handles the secrets in the following three ways:

-  CIC Default Certificate

-  Preconfigured Certificates

-  TLS Section in the Ingress YAML

## CIC Default Certificate

The CIC default certificate is used to provide a secret on Kubernetes that needs to be used as a non-SNI certificate. You must provide the secret name to be used and namespace from which it should be taken as arguments in the `.yaml` file of the CIC:

```YAML
--default-ssl-certificate <NAMESPACE>/<SECRET_NAME>
```

The following is a sample `cic.yaml` file with `hotdrink.secret` tls secret picked from the `ssl` namespace and provided as the CIC default certificate.

```YAML
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
        # Set NetScaler Management IP
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

CIC allows you to use the certkeys that are already configured on the Citrix ADC. You must provide the details about the certificate using an annotation in the ingress definition. The general format for the annotation is:

    ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "<name>", "type": "default|sni|ca"} ] }'

You can provide details about multiple certificates as a list within the annotation. Also, you can define the way the certificate should be treated. In the following sample annotation, certkey1 is used as a non-SNI certificate and certkey2 is used as an SNI certificate:

    ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "certkey1", "type": "default"}, {"name": "certkey2", "type": "sni"} ] }’

If the `type` parameter is not provided with the name of a certificate, then it is considered as the default (non-SNI) type.

>**Important**
>
>1.  Ensure that you use this feature in cases where you want to reuse the certificates that are present on the Citrix ADC and bind them to the applications that is managed by CIC.
>
>2.  CIC does not manage the life cycle of the certificates. That is, it does not create or delete the certificates, but only bind them to the necessary applications.

## TLS Section in the Ingress YAML

Kubernetes allows you to provide the tls secrets in the `spec:` section of an ingress definition. This section describes how CIC uses these secrets.

### With the host section

If the secret name is provided with the host section, CIC binds the secret as an SNI certificate.

```YAML
spec:
  tls:
  - secretName: fruitjuice.secret
  rules:
  - host: items.fruit.juice
```

### Without the host section

If the secret name is provided without the host section, CIC binds the secret as a non-SNI certificate.

```yml
spec:
  tls:
  - secretName: colddrink.secret
```

## Points to note

1.  In cases wherein if multiple secrets are provided to the CIC the following precedence is followed:

    ```ssl-default-certificate < preconfigured-default-certkey < non-host tls secret```.

2.  If there is a conflict in precedence among the same grade certificates (for example, two ingress files configure a non-host tls secret each, as default/non-SNI type), then the CIC binds the CIC default certificate as the non-SNI certificate and uses all other certificates with SNI.
