# TLS certificate handling

Ingress can be secured with the TLS PEM certificates. You can use this certificate to encrypt the communication. Netscaler ingress controller provides option to configure TLS certificates for SSL-based virtual servers in NetScaler. The SSL virtual server intercepts SSL traffic, decrypts it and processes it before sending it to services that are bound to the virtual server.

This tutorial shows you how to secure an Ingress using TLS/SSL certificates while using NetScaler.

## Before you begin

You need a Kubernetes cluster and the `kubectl` command-line tool to communicate with the cluster. If you already do not have a cluster created, follow the instructions in [creating the Kubernetes cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).

This tutorial uses a separate namespace called `netscaler` throughout this tutorial for keeping things isolated. Run the following command to prepare your cluster for this tutorial:

        $ kubectl create namespace netscaler
          namespace "netscaler" created

## Sourcing the TLS certificate

You can use an existing TLS certificate or key pair or use the certificate issued from Let's Encrypt.

### Import existing certificate for pre-existing TLS certificate or key pair

To import an existing TLS certificate/key pair into a Kubernetes cluster, run the following command.

        $ kubectl create secret tls tls-secret --namespace=netscaler --cert=path/to/tls.cert --key=path/to/tls.key
          secret "tls-secret" created

This command creates a secret with the PEM formatted certificate under the `tls.cert` key and the PEM formatted private key under the `tls.key` key.

        apiVersion: v1
        kind: Secret
        metadata:
          name: tls-secret
          namespace: netscaler
        data:
          tls.crt: base64 encoded cert
          tls.key: base64 encoded key

### Issue the certificate from Let's Encrypt

The [cert-manager](https://github.com/cert-manager/cert-manager) add-on automatically requests missing or expired certificates from a range of [supported issuers](https://cert-manager.io/docs/configuration/) (including [Let's Encrypt](https://letsencrypt.org)) by monitoring ingress resources.

To enable such a certificate for an ingress resource you have to deploy cert-manager, configure a certificate issuer, and then update the manifest.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            cert-manager.io/issuer: letsencrypt-staging
            [..]
          name: ingress-demo
          namespace: netscaler
        spec:
          ingressClassName: netscaler
          tls:
          - hosts:
            - demo.example.com
            secretName: tls-secret
          [..]
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---


## Securing HTTP Service

### TLS Section in the Ingress YAML

Kubernetes allows you to provide the TLS secrets in the `spec:` section of an ingress definition. This section describes how the Netscaler ingress controller uses these secrets.

#### Without the host section

If the secret name is provided without the host section, Netscaler ingress controller binds the secret as a default certificate.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations: {}
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


This Ingress opens an HTTPS listener to secure the channel from the client to the load balancer, terminate TLS at the load balancer, and forward unencrypted traffic to the `service-test` service.

#### With the `host` section

If the secret name is provided with the host section, Netscaler ingress controller binds the secret as an SNI certificate.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations: {}
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
          - hosts:
            - example.com
            secretName: tls-secret
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---


This Ingress opens an https listener to secure the channel from the client to the load balancer, terminates TLS at NetScaler with the secret retrieved via SNI, and forward unencrypted traffic to the `service-test`.

### Using the argument `default-ssl-certificate` in Netscaler ingress controller

The argument `default-ssl-certificate` in Netscaler ingress controller is used to provide a secret on Kubernetes that needs to be used as a non-SNI certificate. You must provide the secret name to be used and the namespace from which it should be taken as arguments in the deployment YAML file of the Netscaler ingress controller:

            --default-ssl-certificate <NAMESPACE>/<SECRET_NAME>

**Note:**
The `default-ssl-certificate` option is supported for OpenShift routes as well.

### Pre-configured Certificates in NetScaler

Netscaler ingress controller allows you to use certkeys that are already configured on NetScaler. You must provide the details about the certificate using the following annotation in your ingress definition:

        ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "<name>", "type": "default|sni|ca"} ] }'

You can provide details about multiple certificates as a list within the annotation. Also, you can define the way the certificate is treated. In the following sample annotation, certkey1 is used as a non-SNI certificate and certkey2 is used as an SNI certificate:

        ingress.citrix.com/preconfigured-certkey : '{"certs": [ {"name": "certkey1", "type": "default"}, {"name": "certkey2", "type": "sni"} ] }’

If the type parameter is not provided with the name of a certificate, then it is considered as the default (non-SNI) type.

The following ingress YAML shows for how back-end service `service-test` is secured using certkeys preconfigured in NetScaler (`leaf-certificate`, `intermediate-ca`, and `root-ca` are pre-configured certkeys in NetScaler).

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            ingress.citrix.com/preconfigured-certkey: '{"certs": [ {"name": "leaf-certificate",
              "type": "default"} , {"name": "intermediate-ca", "type": "ca"}, {"name": "root-ca",
              "type": "ca"} ] }'
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
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---
        

**Note:**
Ensure that you use this feature in cases where you want to reuse the certificates that are present on the NetScaler and bind them to the applications that are managed by Netscaler ingress controller.

**Note:**
Netscaler ingress controller does not manage the life cycle of the certificates. That is, it does not create or delete the certificates, but only binds them to the necessary applications.
