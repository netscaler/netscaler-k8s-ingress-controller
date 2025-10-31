# VIP CustomResourceDefinitions

Citrix provides a [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRD) called **VIP** for asynchronous communication between the IPAM controller and [Netscaler ingress controller](https://github.com/netscaler/netscaler-k8s-ingress-controller).

The **IPAM controller** is provided by Citrix for IP address management. It allocates IP address to the service from a defined IP address range. The Netscaler ingress controller configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADX VPX. And, the service is exposed using the IP address.

When a new service is created, the Netscaler ingress controller creates a CRD object for the service with an empty IP address field. The IPAM Controller listens to addition, deletion, or modification of the CRD and updates it with an IP address to the CRD. Once the CRD object is updated, the Netscaler ingress controller automatically configures Netscaler-specfic configuration in the tier-1 Netscaler VPX.

## Deploy the VIP CRD

Deploy the VIP CRD using the following command:

    kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/vip/vip.yaml
