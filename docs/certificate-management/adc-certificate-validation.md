# Enable Citrix ADC certificate validation in the Citrix ingress controller

The Citrix ingress controller provides an option to ensure secure communication between the Citrix ingress controller and Citrix ADC by using the HTTPS protocol. You can achieve this by using pre-loaded certificates in the Citrix ADC. As an extra measure to avoid any possible man-in-the-middle (MITM) attack, the Citrix ingress controller also allows you to validate the SSL server certificate provided by the Citrix ADC.

To enable certificate signature and common name validation of the ADC server certificate by the Citrix ingress controller, security administrators can optionally install signed (or self-signed) certificates in the Citrix ADC and configure the Citrix ingress controller with the corresponding CA certificate bundle. Once the validation is enabled and CA certificate bundles are configured, the Citrix ingress controller starts validating the certificate (including certificate name validation). If the validation fails, the Citrix ingress controller logs the same and none of the configurations are used on an unsecure channel.

This validation is turned off by default and an administrator can chose to enable the validation in the Citrix ingress controller as follows.

## Prerequisites

- For enabling certificate validation, you must configure a Citrix ADC with proper SSL server certificates (with proper server name or IP address in certificate subject). For more information, see [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ssl-certificates/add-group-certs.html).

- The CA certificate for the installed server certificate-key pair is used to configure the Citrix ingress controller to enable validation of these certificates.

## Configure the Citrix ingress controller for certificate validation

To make a CA certificate available for configuration, you need to configure the CA certificate as a Kubernetes secret so that the Citrix ingress controller can access it on a mounted storage volume.

To generate a Kubernetes secret for an existing certificate, use the following `kubectl` command:

      $ kubectl create secret generic ciccacert --from-file=path/myCA.pem –namespace default

      secret “ciccacert” created

Alternatively, you can also generate the Kubernetes secret using the following YAML definition:

        apiVersion: v1
        kind: Secret
        metadata:
	      name: ciccacert
        data:
  	       myCA.pem: <base64 encoded cert>

The following is a sample YAML file with the Citrix ingress controller configuration for enabling certificate validation.

```yml

kind: Pod
metadata:
  name: cic
  labels:
    app: cic
spec:
  serviceAccountName: cpx
  # Make secret available as a volume
  volumes:
  - name: certs
    secret:
      secretName: ciccacert
  containers:
  - name: cic
    image: "xxxx"
    imagePullPolicy: Always
    args: []
    # Mounting certs in a volume path
    volumeMounts:
    - name: certs
      mountPath: <Path to mount the certificate>
      readOnly: true
    env:
    # Set Citrix ADM Management IP
    - name: "NS_IP"
      value: "xx.xx.xx.xx"
    # Set port for Nitro
    - name: "NS_PORT"
      value: "xx"
    # Set Protocol for Nitro
    - name: "NS_PROTOCOL"
      # Enable HTTPS protocol for secure communication
      value: "HTTPS"
    # Set username for Nitro
    - name: "NS_USER"
      value: "nsroot"
    # Set user password for Nitro
    - name: "NS_PASSWORD"
      value: "nsroot"
    # Certificate validation configurations
    - name: "NS_VALIDATE_CERT"
      value: "yes"
    - name: "NS_CACERT_PATH"
      value: " <Mounted volume path>/myCA.pem"
```

As specified in the example YAML file, following are the specific changes required for enabling certificate validation in the Citrix ingress controller.

### Configure Kubernetes secret as a volume

-  Configure a volume section declared with `secret` as the source. Here, `secretName` should match the Kubernetes secret name created for the CA certificate.

### Configure a volume mount location for the CA certificate

- Configure a `volumeMounts` section with the same name as that of `secretName` in the volume section
- Declare a `mountPath` directory to mount the CA certificate
- Set the volume as `ReadOnly`

### Configure secure communication

- Set the environment variable `NS_PROTOCOL` as HTTPS
- Set the environment variable `NS_PORT` as ADC HTTPS port

### Enable and configure CA validation and certificate path

- Set the environment variable `NS_VALIDATE_CERT` to `yes` ( `no` for disabling)
- Set the environment variable `NS_CACERT_PATH` as the mount path (volumeMounts->mountPath)/ PEM file name (used while creating the secret).
