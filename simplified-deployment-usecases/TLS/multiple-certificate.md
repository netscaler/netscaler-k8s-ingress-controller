# Multiple certificates to an Ingress

You can secure an Ingress by specifying TLS secrets inside the `spec.tls` section of the Ingress. Citrix ingress controller uploads the TLS secrets in the `nsconfig/ssl` folder inside the NetScaler. So if you specify multiple TLS secrets, all of them are present in the `/nsconfig/ssl` folder. NetScaler presents the certificate to clients which matches with the TLS Server Name Indication (SNI) field of the request. If no SNI is provided by the client or if the SNI does not match with any certificate, then the first loaded certificate is presented. So you need to send a request with the correct SNI. The Host header indicates the SNI.

This tutorial shows you how to configure multiple TLS secrets or certificates for different hosts within a single ingress.

## Before you begin

You need a Kubernetes cluster and `kubectl` command-line tool to communicate with the cluster.
If you are using NetScaler VPX or MPX, follow [Deploy Citrix ingress controller](./quick-installation-cic.md) instructions to deploy Citrix ingress controller to configure the same. If you do not have NetScaler VPX or MPX, you can use NetScaler CPX and follow the instructions to deploy Citrix ingress controller and CPX.

This tutorial uses a separate namespace called `netscaler` throughout this tutorial for keeping things isolated. Run the following command to prepare your cluster for this tutorial:

        $ kubectl create namespace netscaler
          namespace "netscaler" created

## Create certificate

Create a TLS certificate or key pair into a Kubernetes cluster for two hosts in this example considering hosts (exampleone.com and exampletwo.com), run the following commands:

        $ kubectl create secret tls tls-example-one --namespace=netscaler --cert=path/to/tls-example-one.cert --key=path/to/tls-example-one.key 
          secret "tls-example-one" created

        $ kubectl create secret tls tls-example-two --namespace=netscaler --cert=path/to/tls-example-two.cert --key=path/to/tls-example-two.key 
          secret "tls-example-two" created

Here, `tls-example-one.cert` and `tls-example-one.key` is cert/key for `exampleone.com`. Similarly `tls-example-two.cert` and `tls-example-two.key` is cert/key for `exampletwo.com`

## Ingress with multiple certificates

Following is the ingress for the two hosts and the hosts are used for SNI matching in the request.

          apiVersion: networking.k8s.io/v1
          kind: Ingress
          metadata:
            annotations: {}
            name: multi-cert-ingress
            namespace: netscaler
          spec:
            ingressClassName: netscaler
            rules:
            - host: exampleone.com
              http: null
              paths:
              - backend: null
                path: /
                serviceName: example-one
                servicePort: 80
            - host: exampletwo.com
              http: null
              paths:
              - backend: null
                path: /
                serviceName: example-two
                servicePort: 80
            tls:
            - hosts:
              - host: exampleone.com
                secretName: tls-example-one
            - hosts:
              - host: exampletwo.com
                secretName: tls-example-two
          ---
          apiVersion: networking.k8s.io/v1
          kind: IngressClass
          metadata:
            name: netscaler
          spec:
            controller: citrix.com/ingress-controller
          ---
          