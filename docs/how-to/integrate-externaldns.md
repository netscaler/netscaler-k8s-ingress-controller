# Interoperability with ExternalDNS

In a Kubernetes environment, you can expose your deployment using a service of type `LoadBalancer`. Also, an IP address can be assigned to the service using Citrix IPAM controller. The Citrix IPAM controller assigns IP address to the service from a defined pool of IP addresses. For more information, see [Expose services of type LoadBalancer with IP addresses assigned by the IPAM controller](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/network/type_loadbalancer.md).

The service can be accessed using the IP address assigned by the IPAM controller and for service discovery you need to manually register the IP address to a DNS provider. If the IP address assigned to the service changes, the associated DNS record must be manually updated and the entire process becomes cumbersome. In such cases, you can use a [ExternalDNS](https://github.com/kubernetes-sigs/external-dns) to keep the DNS records synchronized with your external entry points. Also, ExternalDNS allows you to control DNS records dynamically through Kubernetes resources in a DNS provider-agnostic way.

For the ExternalDNS integration to work, the `external-dns.alpha.kubernetes.io/hostname` annotation must contain the host name.

>**Important:** For ExtenalDNS to work, ensure that you add the annotation `external-dns.alpha.kubernetes.io/hostname` in the service specification and specify a host name for the service using the annotation.

**To integrate with ExternalDNS:**

1.  Install the [ExternalDNS](https://github.com/kubernetes-sigs/external-dns) with Infoblox provider.

    >**Note:**
    > The interoperability solution has been tested with Infoblox provider and the solution might work for other providers as well.

1.  Specify the domain name in the ExternalDNS configuration.
1.  In the service of type `LoadBalancer` specification, add the following annotation and specify a host name for the service using the annotation:

        external-dns.alpha.kubernetes.io/hostname

1.  Deploy the service using the following command:

        kubectl create -f <service-name>.yaml