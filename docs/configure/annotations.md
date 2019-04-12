# Annotations

The following are the annotations supported by Citrix:

|**Annotations**|**Possible value**|**Description**|**Default**|
|---------------|------------------|---------------|-----------|
|ingress.citrix.com/frontend-ip| IP address | Use this annotation to customize the virtual IP address (VIP). This IP address is configured in Citrix ADC as VIP. The annotation is mandatory if you are using Citrix ADC VPX or MPX. **Note:** Do not use the annotation if you want to use the Citrix ADC IP address as VIP. | Citrix ADC IP address is used as VIP.
|ingress.citrix.com/secure-port|Port number |Use this annotation to configure the port for HTTPS traffic. This port is configured in Citrix ADC as a port value for corresponding Content Switching (CS) virtual server.| 443|
|ingress.citrix.com/insecure-port| Port number | Use this annotation to configure the port for HTTP traffic. This port is configured in Citrix ADC as a port value for corresponding CS virtual server| 80 |
|ingress.citrix.com/insecure-termination|one of {"allow", "redirect","disallow"}|Use `allow` to allow HTTP traffic, Use `redirect` to redirect the HTTP request to HTTPS, or Use `disallow` if you want to drop the HTTP traffic. | disallow |
| | |For example: `ingress.citrix.com/insecure-termination: "redirect"` | |
|ingress.citrix.com/secure-backend|In JSON form, list of services for secure-backend |Use `True`, if you want to establish secure HTTPS between Citrix ADC and the application, Use `False`, if you want to establish insecure HTTP connection Citrix ADC to the application | False|
| | | For example: `ingress.citrix.com/secure-backend: {‘app1’:"True", ‘app2’:"False", ‘app3’:"True"}` | |
|kubernetes.io/ingress.class|ingress class name| It is a way to associate a particular ingress resource with an ingress controller. | Configures all ingresses |
| | |For example: `kubernetes.io/ingress.class:"Citrix"` | |
|ingress.citrix.com/insecure-service-type| Any one of `tcp` or `udp` | The annotation allows L4 load balancing with tcp/udp/any as protocol. Use `tcp`, if you want TCP as the protocol. Use `udp`, if you want udp as the protocol| http|
|ingress.citrix.com/service_weights|In JSON form, weights distribution (in %) among the backend services. Sum of weight should be 100% | It allows CIC to play a role in canary deployment. The values must be in JSON format. For each backend app in the ingress, there should be corresponding traffic %. All weights should be in % and sum should be 100 | No weight distribution|
| | | For example: `ingress.citrix.com/service_weights: {‘canary-app1’:5, ‘baseline-app1’:5 ‘production-app1’:90}` | |
| | | Here there are 3 apps and % traffic distribution is 5%, 5%, and 90% | |
|ingress.citrix.com/lbvserver | In JSON form, settings for lb virtual server or service group | This provides smart annotation capability. Using this, an advanced user (who has knowledge of NetScaler LB virtual server and Service group options) can directly apply them. Values must be in JSON format. For each backend app in the ingress, provide key value pair. Key name should match with the corresponding CLI name |Default options provided by Citrix ADC|
| | |For example:  `ingress.citrix.com/lbvserver: '{"app-1":{"lbmethod":"ROUNDROBIN"}}'` | |
| | | `ingress.citrix.com/servicegroup: '{"app-1":{"maxReq":"100"}}'` | |
| | | Here for app-1, you want to configure ROUND-ROBIN load balance method at LB level and maxReq at service group| |
