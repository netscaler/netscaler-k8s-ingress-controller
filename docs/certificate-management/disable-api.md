# Disable API server certificate verification

While communicating with the API server from Citrix ingress controller or multicluster ingress, you have the option to disable the API server certificate verification on Citrix ingress controller. This option is useful when you are using custom certificates.

## Disable API server certificate verification on Citrix ingress controller or Multi-cluster ingress

When you deploy Citrix ingress controller using YAML, you can disable the API server certificate verification by providing the following argument in the [Citrix ingress controller deployment YAML](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file.

     args:
        - --disable-apiserver-cert-verify
          true

When you deploy Citrix ingress controller using Helm charts, the parameter `disableAPIServerCertVerify` can be mentioned as `True` in the Helm values file as follows:

        disableAPIServerCertVerify: True
