# Add DNS records using Citrix ADC ingress controller

A DNS address record is a mapping of the domain name to the IP address.
When you want to use Citrix ADC as a DNS resolver, you can add the DNS records on Citrix ADC using Citrix ingress controller.

For more information on creating DNS records on Citrix ADC, see the [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/dns/configure-dns-resource-records/create-address-records.html).

## Adding DNS records for Ingress resources

You need to enable the following environment variable during the Citrix ingress controller deployment to add DNS records for an Ingress resource.

`NS_CONFIG_DNS_REC`: This variable is configured at the boot time and cannot be changed at runtime. Possible values are `true` or `false`. The default value is false and you need to set it as true to enable the DNS server configuration. When you set the value as `true`, an address record is created on Citrix ADC.

## Adding DNS records for services of type LoadBalancer

You need to perform the following tasks to add DNS records for services of type LoadBalancer:

-  Enable the `NS_SVC_LB_DNS_REC` environment variable by setting the value as `True` for adding DNS records for a service of type LoadBalancer.
-  Specify the DNS host name using the `service.citrix.com/dns-hostname` annotation.

When you create a service of type LoadBalancer with the  `service.citrix.com/dns-hostname` annotation, Citrix ingress controller adds the DNS record on Citrix ADC. The DNS record is configured using the domain name specified in the annotation and the external IP address assigned to the service.

When you delete a service of type LoadBalancer with the `service.citrix.com/dns-hostname` annotation, Citrix ADC ingress controller removes the DNS records from the Citrix ADC.
Citrix ingress controller also removes the stale entries of DNS records during boot up if the service is not available.

The following example shows a sample service of type LoadBalancer with the annotation configuration to add DNS records to Citrix ADC:

```yml
apiVersion: v1
kind: Service
metadata:
  name: guestbook
  annotations:
      service.citrix.com/dns-hostname: "guestbook.com"
spec:
  loadBalancerIP: "192.2.212.16"
  type: LoadBalancer
  ports:
  - port: 9006
    targetPort: 80
    protocol: TCP
  selector:
    app: guestbook
```