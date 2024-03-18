# Disable API server certificate verification

While communicating with the API server from Netscaler ingress controller or gslb ingress, you have the option to disable the API server certificate verification on Netscaler ingress controller.

## Disable API server certificate verification on Netscaler ingress controller or gslb ingress

When you deploy Netscaler ingress controller using YAML, you can disable the API server certificate verification by providing the following argument in the [Netscaler ingress controller deployment YAML](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file.

     args:
        - --disable-apiserver-cert-verify
          true

When you deploy Netscaler ingress controller using Helm charts, the parameter `disableAPIServerCertVerify` can be mentioned as `True` in the Helm values file as follows:

        disableAPIServerCertVerify: True
