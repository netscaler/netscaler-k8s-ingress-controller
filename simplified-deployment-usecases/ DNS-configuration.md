# NetScaler DNS configuration using Netscaler ingress controller

NetScaler can be configured as an Authoritative Domain Name Server (ADNS), DNS proxy server, DNS resolver, or Forwarder. You can configure DNS resource records such as SRV records, A records, AAAA records, NS records, SOA records, and so on which can load balance on external DNS servers.

You can add, remove, enable, and disable external name servers using their IP addresses or you can configure an existing virtual server as the name server.

When adding name servers you can specify IP addresses or Virtual IP addresses (VIPs).

You can use Netscaler ingress controller to configure NetScaler with the following DNS configurations.

- [NetScaler DNS configuration using Netscaler ingress controller](#netscaler-dns-configuration-using-citrix-ingress-controller)
  - [Configuring NetScaler VPX or MPX as an ADNS server](#configuring-netscaler-vpx-or-mpx-as-an-adns-server)
  - [Configuring NetScaler as DNS resolver](#configuring-netscaler-as-dns-resolver)
    - [Adding DNS records for Ingress resources](#adding-dns-records-for-ingress-resources)
    - [Adding DNS records for services of type LoadBalancer](#adding-dns-records-for-services-of-type-loadbalancer)
  - [Configuring DNS Nameservers on NetScaler VPX or MPX](#configuring-dns-nameservers-on-netscaler-vpx-or-mpx)
  - [Traffic Management of External services](#traffic-management-of-external-services)
    - [Configure NetScaler as a domain name resolver using Netscaler ingress controller](#configure-netscaler-as-a-domain-name-resolver-using-citrix-ingress-controller)
    - [Configure a service to enable reachability of NetScaler from the Kubernetes cluster](#configure-a-service-to-enable-reachability-of-netscaler-from-the-kubernetes-cluster)
    - [Configure IP address of DNS server to reach external service endpoints](#configure-ip-address-of-dns-server-to-reach-external-service-endpoints)
    - [Traffic management using NetScaler CPX](#traffic-management-using-netscaler-cpx)
  - [Configuring Wildcard domains in NetScaler using Netscaler ingress controller](#configuring-wildcard-domains-in-netscaler-using-citrix-ingress-controller)
    - [Deploying Wildcard DNS CRD](#deploying-wildcard-dns-crd)

## Configuring NetScaler VPX or MPX as an ADNS server

Netscaler ingress controller can configure NetScaler VPX/MPX as an ADNS server using the ConfigMap variable `NS_ADNS_IPS`.

An example of a ConfigMap for configuring NetScaler VPX/MPX as ADNS servers.

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: adns-cmap
  namespace:  netscaler
data:
  NS_ADNS_IPS: '["192.1.2.3", "175.2.4.5"]' # List of IPs to configure ADNS server
```

**NOTE:**
 You can also configure NetScaler VPX or MPX as an ADNS server using the environment variable `NS_ADNS_IPS` of [Netscaler ingress controller deployment](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml#L95).

NetScaler Configuration:

```
show server

1)	Name:           192.1.2.3      State:ENABLED 
	IPAddress:         192.1.2.3 
2)	Name:    175.2.4.5      State:ENABLED 
	IPAddress:  175.2.4.5 
```

## Configuring NetScaler as DNS resolver

To configure NetScaler as a DNS resolver, you can add the DNS address records using Netscaler ingress controller.

### Adding DNS records for Ingress resources

To add DNS records for ingress resources, you need to set the value of the variable `NS_CONFIG_DNS_REC` to `true` in [Netscaler ingress controller](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml#L95) deployment at the boot time.
Netscaler ingress controller adds the address records in NetScaler for all the host names specified under the ingresses that are intended to configure NetScaler.

### Adding DNS records for services of type LoadBalancer

To add DNS records for the service of type LoadBalancer, you need to:

1.  Enable the `NS_SVC_LB_DNS_REC` environment variable of Netscaler ingress controller deployment by setting the value as `true`.
2.  Specify the DNS host name for which the address records needs to be updated in NetScaler using the `service.citrix.com/dns-hostname` annotation in the service of type LoadBalancer.

Following is an example of a service of Type LoadBalancer with the special annotation to add DNS address records in NetScaler.

```yml
apiVersion: v1
kind: Service
metadata:
  name: guestbook
  annotations:
    # Special annotation to add DNS Address records in Netscaler.
    service.citrix.com/dns-hostname: "www.guestbook.com"
spec:
    type: LoadBalancer
    ports:
    - port: 9006
      targetPort: 80
      protocol: TCP
    selector:
      app: guestbook
```

NetScaler Configuration:

```
show  dns addrec 

1)	Host Name : www.guestbook.com 	ECS Subnet : None                
	Record Type : ADNS  		TTL : 3600 secs
	IP Address : 175.4.3.5        

```

## Configuring DNS Nameservers on NetScaler VPX or MPX

Netscaler ingress controller can configure DNS nameservers on NetScaler VPX or MPX using the ConfigMap variable `NS_DNS_NAMESERVER`.

An example of a ConfigMap to configure DNS nameservers on NetScaler VPX or MPX.

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nameserver-cmap
  namespace: netscaler
data:
  NS_DNS_NAMESERVER: '["192.1.2.3", "175.2.4.5"]' # List of Name server IPs to configured on NetScaler VPX/MPX
```

**NOTE:**
You can also configure DNS nameservers on NetScaler VPX/MPX using the environment variable `NS_DNS_NAMESERVER` of [Netscaler ingress controller deployment](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml).

NetScaler configuration:

```
   # show nameserver
    1)	 192.1.2.3  -  State: DOWN 	Protocol: UDP
    2)	 192.1.2.3  -  State: DOWN 	Protocol: TCP
    3)	 175.2.4.5  -  State: DOWN 	Protocol: UDP
    4)	 175.2.4.5  -  State: DOWN 	Protocol: TCP

```

## Traffic Management of External services

To enable NetScaler features such as traffic management, policy enforcement, fail over management an external service which is deployed outside of the Kubernetes cluster, you need to configure NetScaler as domain name resolver and make sure that the reachability of the external service is established from the Kubernetes cluster.

### Configure NetScaler as a domain name resolver using Netscaler ingress controller

Netscaler ingress controller can configure NetScaler as domain name resolver by creating a domain-based service group using the ingress annotation `ingress.citrix.com/external-service`.

The value for `ingress.citrix.com/external-service` is a list of external name services with their corresponding domain names.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/external-service: '{"my-service": {"domain": "www.external.service.com"}}'
  name: ingress-demo
  namespace: netscaler
spec:
  ingressClassName: netscaler
  rules:
  - host: externalservice.com
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

```

### Configure a service to enable reachability of NetScaler from the Kubernetes cluster

To reach NetScaler from microservices in a Kubernetes cluster, you need to define a headless service which would be resolved to a NetScaler service and thus the connectivity between microservices and NetScaler establishes.

The following is the sample NetScaler service which enables connectivity from microservices to NetScaler.

```yml
apiversion: v1
kind: Service
metadata: 
  name: my-service
spec:
  selector:
    app: cpx
  ports:
    - protocol: TCP
      port: 80
```

### Configure IP address of DNS server to reach external service endpoints

Using the ConfigMap variable `NS_DNS_NAMESERVER` you can configure the name server to reach the external service.

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nameserver-cmap
  namespace: default
data:
    NS_DNS_NAMESERVER: '["192.1.2.3"]'
```

### Traffic management using NetScaler CPX

The following diagram depicts NetScaler CPX deployment to reach external services. An Ingress is deployed where the external service annotation is specified to configure DNS on NetScaler CPX.

**Note:** A ConfigMap is used to configure name servers on NetScaler VPX or MPX.

![Traffic Management of External Services](../docs/media/cpx-traffic.png)

In this deployment:

1. A microservice sends the DNS query for www.externalsvc.com which would get resolved to the NetScaler CPX service.

2. NetScaler CPX resolves www.externalsvc.com and reaches external service.

Following are the steps to configure NetScaler CPX to load balance external services:

1. Define a headless service to reach NetScaler.

    ```yml
    apiVersion: v1
    kind: Service
    metadata:
      name: external-svc # Service to reach CPX
    spec:
      selector:
        app: cpx # Referring to CPX deployment
      ports:
      - protocol: TCP
        port: 80
    ```

2.  Define an ingress and specify the external-service annotation with which, Netscaler ingress controller creates DNS servers on NetScaler and binds the servers to the corresponding service group.

    ```yml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      annotations:
        ingress.citrix.com/external-service: '{"external-svc": {"domain": "www.externalsvc.com"}}'
      name: dbs-ingress
    spec:
      ingressClassName: cpx-ingress
      rules:
      - host: www.portal.externalsvc.com
        http:
          paths:
          - backend:
              service:
                name: my-external-service
                port:
                  number: 30036
            path: /
            pathType: Prefix
    ---
    apiVersion: networking.k8s.io/v1
    kind: IngressClass
    metadata:
      name: cpx-ingress
    spec:
      controller: citrix.com/ingress-controller
    ---

    ```

## Configuring Wildcard domains in NetScaler using Netscaler ingress controller

Using the Wildcard DNS CRD, you can configure wildcard DNS domains on a Netscaler using Netscaler ingress controller.
The Wildcard DNS CRD is available in the Netscaler ingress controller GitHub repo at  [wildcarddnsentry.yaml](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/crd/wildcard-dns/wildcarddnsentry.yaml) . The Wildcard DNS CRD provides attributes for the various options that are required to configure wildcard DNS entries on NetScaler.

The following are the attributes provided in the Wildcard DNS CRD:

|Attribute |Description |
|----------|-------------|
|`domain` |Specifies the wild card domain name configured for the zone.|
|`dnsaddrec`|Specifies the DNS Address record with the IPv4 address of the wildcard domain.|
|`dnsaaaarec`|Specifies the DNS AAAA record with the IPV6 address of the wildcard domain.|
|`soarec`|Specifies the SOA record configuration details.|
|`nsrec`|Specifies the name server configuration details.|

### Deploying Wildcard DNS CRD

1.  Deploy the Wildcard DNS CRD definition YAML from [Wildcard DNS YAML](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/wildcard-dns/wildcarddnsentry.yaml)

      kubectl create -f wildcarddns_spec.yaml

2.  Update domain name, zone, DNS address record, AAAA record, SOA record and the NS record in the CRD instance and apply the configuration.

       kubectl create -f wilcardddns_config.yaml

   A sample YAML file definition that configures a SOA record, NS record, DNS zone, and address and AAAA Records on NetScaler.

```yml
apiVersion: citrix.com/v1
kind: wildcarddnsentry
metadata:
  name: sample-config
spec:
  zone:
    # Domain the wildcard domain name to configured on NetScaler
    domain: configexample.com
    # DNS address record to be configured on NetScaler with IP and ttl
    dnsaddrec:
      domain-ip: 1.1.1.1
      ttl: 3600
    # DNS AAAA record to be configured in Netscaler with IP and ttl 
    dnsaaaarec:
      domain-ip: '2001::.1'
      ttl: 3600
    # DNS SOA record to be configured in NetScaler with origin-server name, admin contact information, retry count, expiry time, refresh time, etc
    soarec:
      origin-server: n2.configexample.com
      contact: admin.configexample.com
      serial: 100
      refresh: 3600
      retry: 3
      expire: 3600
    # DNS NS records to be configured in NetScaler with nameserver domain name and ttl 
    nsrec:
      nameserver: n1.configexample.com
      ttl: 3600
```

NetScaler Configuration:

```
show soarec
1)	Domain Name : configexample.com 	ECS Subnet : None               		Origin Server : n2.configexample.com
	Contact : admin.configexample.com
	Serial No. : 100	Refresh : 3600 secs	Retry : 3 secs
	Expire : 3600 secs	Minimum : 5 secs	TTL : 3600 secs
	Record Type : ADNS

show nsrec
1)	Domain : configexample.com 	ECS Subnet : None               	NameServer : n1.configexample.com
	TTL : 3600 sec	Record Type : ADNS

show dns zone
	 Zone Name : configexample.com
	 Proxy Mode : NO
	 DNSSEC Offload: DISABLED

show dns addrec
1)	Host Name : *.configexample.com 	ECS Subnet : None                
	Record Type : ADNS  		TTL : 3600 secs
	IP Address : 1.1.1.1

show dns aaaarec
1)	Host Name : *.configexample.com 	ECS Subnet : None                
	Record Type : ADNS  		TTL : 3600 secs
	IPV6 Address : 2001::1        
```

**Note:** For more information on configuring wildcard domain names in NetScaler, see [Supporting Wildcard Domains](https://docs.citrix.com/en-us/citrix-adc/current-release/dns/supporting-wildcard-dns-domains.html).
