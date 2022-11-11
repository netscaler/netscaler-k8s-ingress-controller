
# Configuring wildcard DNS domains through Citrix ADC ingress controller

Wildcard DNS domains are used to handle requests for non-existent domains and subdomains. In a DNS zone, you can use wildcard domains to redirect queries for all non-existent domains or subdomains to a particular server, instead of creating a separate Resource Record (RR) for each domain. The most common use of a wildcard DNS domain is to create a zone that can be used to forward mail from the internet to some other mail system.

For more information on wildcard DNS domains, see the [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/dns/supporting-wildcard-dns-domains.html).

Now, you can configure wildcard DNS domains on a Citrix ADC with Citrix ingress controller. Custom Resource Definitions (CRDs) are the primary way of configuring policies in cloud native deployments. Using the Wildcard DNS CRD provided by Citrix, you can configure wildcard DNS domains on Citrix ADC with the Citrix ingress controller. The Wildcard DNS CRD enables communication between Citrix ingress controller and Citrix ADC for supporting wild card domains.

## Usage guidelines and restrictions

-  For fully qualified domain names (FQDNs), there are multiple ways to add DNS records. You can either enable the `NS_CONFIG_DNS_REC` variable for Citrix ingress controller for the Ingress resource or use the wildcard DNS CRD. However, you should make sure that they are configured through either CRD or ingress in order to avoid multiple IP mappings to the same domain.
-  It is recommended to use the Wildcard DNS CRD for the wildcard DNS configurations.
-  You cannot configure wildcard DNS entries in the DNS address record through ingress if the `NS_CONFIG_DNS_REC` is enabled for Citrix ingress controller.

## Wildcard DNS CRD definition

The Wildcard DNS CRD is available in the Citrix ingress controller GitHub repo at [wildcarddnsentry.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/wildcard-dns/wildcarddnsentry.yaml). The **Wildcard DNS CRD provides** attributes for the various options that are required to configure wildcard DNS entries on Citrix ADC.

The following are the attributes provided in the Wildcard DNS CRD:

| Attribute | Description |
| --------- | ----------- |
| `domain` | Specifies the wild card domain name configured for the zone.|
| `dnsaddrec` | Specifies the DNS Address record with the IPv4 address of the wildcard domain.|
|`dnsaaaarec`| Specifies the DNS AAAA record with the IPV6 address of the wildcard domain.|
| `soarec`| Specifies the SOA record configuration details.|
| `nsrec` |Specifies the name server configuration details.|

## Deploy the Wildcard DNS CRD

Perform the following to deploy the Wildcard DNS CRD:

1. Download the Wildcard DNS CRD.

1. Deploy the Wildcard DNS CD using the following command:

        kubectl create -f wildcarddnsentry.yaml

## How to write a Wildcard DNS configuration policy

After you have deployed the Wildcard DNS CRD provided by Citrix in the Kubernetes cluster, you can define the wildcard DNS related configuration in a `yaml` file. In the `.yaml` file, use `wildcarddnsentry` in the kind field and in the `spec` section add the Wildcard DNS CRD attributes based on your requirement for the policy configuration.

The following is a sample YAML file definition that configures a SOA record, NS record, DNS zone, and address and AAAA Records on Citrix ADC.

```
apiVersion:
citrix.com/v1
kind: wildcarddnsentry
metadata:
  name: sample-config
spec:
  zone:
    domain: configexample
    dnsaddrec:
      domain-ip: 1.1.1.1
      ttl: 3600
    dnsaaaarec:
      domain-ip: '2001::.1'
      ttl: 3600
    soarec:
      origin-server: n2.configexample.com
      contact: admin.configexample.com
      serial: 100
      refresh: 3600
      retry: 3
      expire: 3600
    nsrec:
      nameserver: n1.configexample.com
      ttl: 3600
```

After you have defined the DNS configuration, deploy the `wildcarddns-example.yaml` file using the following command.

        $ kubectl create -f wildcarddns-example.yaml
