# How to use Kubernetes secrets for storing Citrix ADC credentials

In most organizations, Tier 1 Citrix ADC Ingress devices and Kubernetes clusters are managed by separate teams. The Citrix ingress controller requires Citrix ADC credentials such as Citrix ADC user name and password to configure the Citrix ADC. Usually, Citrix ADC credentials are specified as environment variables in the Citrix ingress Controller pod specification. But, another secure option is to use Kubernetes secrets to store the Citrix ADC credentials.

This topic describes how to use Kubernetes secrets to store the ADC credentials and
various ways to provide the credentials stored as secret data for the Citrix ingress controller.

## Create a Kubernetes secret

Perform the following steps to create a Kubernetes secret.

1. Create a file `adc-credential-secret.yaml` which defines a Kubernetes secret YAML with Citrix ADC user name and password in the `data` section as follows.

        apiVersion: v1
        kind: Secret
        metadata:
          name: adc-credential
        data:
          username: <ADC user name>
          password: <ADC password>

2. Apply the `adc-credential-secret.yaml` file to create a secret.
   
        kubectl apply -f adc-credential-secret.yaml

Alternatively, you can also create the Kubernetes secret using `--from-literal` option of the `kubectl` command as shown as follows:

        kubectl create secret generic adc-credentials --from-literal=username=<username> --from-literal=password=<password>

Once you have created a Kubernetes secret, you can use one of the following options to use the secret data in the Citrix ingress controller pod specification.

  - [Use secret data as environment variables in the Citrix ingress controller pod specification](#Use-secret-data-as-environment-variables-in-the-Citrix-ingress-controller-pod-specification)
  - [Use a secret volume mount to pass credentials to the Citrix ingress controller](#Use-a-secret-volume-mount-to-pass-credentials-to-the-Citrix-ingress-controller)

## Use secret data as environment variables in the Citrix ingress controller pod specification

You can use secret data from the Kubernetes secret as the values for the environment variables in the Citrix ingress controller deployment specification.  

A snippet of the YAML file is shown as follows.

      - name: "NS_USER"
        valueFrom:
          secretKeyRef:
            name: adc-credentials
            key: username
      # Set user password for Nitro
      - name: "NS_PASSWORD"
        valueFrom:
          secretKeyRef:
            name: adc-credentials
            key: password

Here is an example of the Citrix ingress controller deployment with value of environment variables sourced from the secret object.

``` yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cic-k8s-ingress-controller
spec:
  selector:
    matchLabels:
      app: cic-k8s-ingress-controller
  replicas: 1
  template:
    metadata:
      name: cic-k8s-ingress-controller
      labels:
        app: cic-k8s-ingress-controller
      annotations:
    spec:
      serviceAccountName: cic-k8s-role
      containers:
      - name: cic-k8s-ingress-controller
        image: <image location>
        env:
         # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)
         - name: "NS_IP"
           value: "x.x.x.x"
         # Set username for Nitro
         - name: "NS_USER"
           valueFrom:
            secretKeyRef:
             name: adc-credentials
             key: username
         # Set user password for Nitro
         - name: "NS_PASSWORD"
           valueFrom:
            secretKeyRef:
             name: adc-credentials
             key: password
         # Set log level
         - name: "EULA"
           value: "yes"
        imagePullPolicy: Always
```

## Use a secret volume mount to pass credentials to the Citrix ingress controller

Alternatively, you can also use a volume mount using the secret object as a source for the Citrix ADC credentials. The Citrix ingress controller expects the secret to be mounted at path `/etc/citrix` and it looks for the credentials in files `username` and `password`.  

You can create a volume from the secret object and then mount the volume using volumeMounts at `/etc/citrix` as shown in the following deployment example.

```yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cic-k8s-ingress-controller
spec:
  selector:
    matchLabels:
      app: cic-k8s-ingress-controller
  replicas: 1
  template:
    metadata:
      name: cic-k8s-ingress-controller
      labels:
        app: cic-k8s-ingress-controller
      annotations:
    spec:
      serviceAccountName: cic-k8s-role
      containers:
      - name: cic-k8s-ingress-controller
        image: <image location>
        env:
         # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)
         - name: "NS_IP"
           value: "x.x.x.x"       
         # Set log level
         - name: "EULA"
           value: "yes"
        volumeMounts:
        # name must match the volume name below
          - name: secret-volume
            mountPath: /etc/citrix
        imagePullPolicy: Always
      # The secret data is exposed to Containers in the Pod through a Volume.
      volumes:
      - name: secret-volume
        secret:
          secretName: adc-credentials
```

## Use Citrix ADC credentials stored in a Hashicorp Vault server

You can also use the Citrix ADC credentials stored in a Hashicorp Vault server for the Citrix ingress controller and push the credentials through a sidecar container.
For more information, see [Using Citrix ADC credentials stored in a Vault server](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/how-to/use-vault-stored-credentials-for-cic.md).