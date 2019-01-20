# **Annotations**

List of annotations supported by Citrix Ingress Controller:

|**Annotations**|**Possible value**|**Description**|**Default**|
|---------------|------------------|---------------|-----------|
|ingress.citrix.com/frontend-ip| IP address | Use this annotation to customize VIP. This IP is configured in Citrix ADC as VIP| Citrix ADC IP is used as VIP.
|ingress.citrix.com/secure-port|Port number |Use this annotation to configure port on which https traffic should land. This port is configured in Citrix ADC as a port value for corresponding CS Vserver.| 443|
|ingress.citrix.com/insecure-port| Port number | Use this annotation to configure port on which http traffic should land. This port is configured in NetScaler as a port value for corresponding CS Vserver| 80 |
|ingress.citrix.com/insecure-termination|one of {"allow", "redirect","disallow"}|Use "allow" to permit http traffic, Use "redirect" to redirect the http request to https, or Use "disallow" if you want to drop the http traffic| disallow|
| | |Example: ingress.citrix.com/insecure-termination: "redirect" | |
|ingress.citrix.com/secure-backend|In JSON form, list of services for secure-backend |Use "True", if you want Citrix ADC to application connection via secure https, Use "False", if you want Citrix ADC to application connection via insecure http| False|
| | | Example: ingress.citrix.com/secure-backend: {‘app1’:"True", ‘app2’:"False", ‘app3’:"True"}| |
|kubernetes.io/ingress.class|ingress class name|It is a way to associate a particular ingress resource with an ingress controller.|Configures all ingresses|
| | |Example: kubernetes.io/ingress.class:"Citrix" | |
|ingress.citrix.com/insecure-service-type|one of {"tcp", "udp"}|This annotation allows L4 load balancing with tcp/udp/any as protocol. Use "tcp", if you want tcp as the protocol. Use "udp", if you want udp as the protocol| http|
|ingress.citrix.com/service_weights|In JSON form, Weights distribution (in %) among the backend services. Sum of weight should be 100%| It allows CIC to play role in canary deployment. Values must be in JSON format. For each backend app in the ingress, there should be corresponding traffic %. All weights should be in % and sum should be 100| No weight distribution|
| | |Example: ingress.citrix.com/service_weights: {‘canary-app1’:5, ‘baseline-app1’:5 ‘production-app1’:90} | |
| | |Here there are 3 apps and % traffic distribution is 5%, 5% and 90% | |
|ingress.citrix.com/lbvserver, ingress.citrix.com/lbvserver| In JSON form, settings for lbvserver/servicegroup| This provides smart annotation capability. Using this, an advanced user (who has knowledge of NetScaler LB Vserver and Service group options) can directly apply them. Values must be in JSON format. For each backend app in the ingress, provide key value pair. Key name should match with the corresponding CLI name |Default options provided by NetScaler|
| | |Example:  ingress.citrix.com/lbvserver: '{"app-1":{"lbmethod":"ROUNDROBIN"}}' | |
| | | ingress.citrix.com/servicegroup: '{"app-1":{"maxReq":"100"}}' | |
| | | Here for app-1, user wants to configure ROUND-ROBIN lbmethod at LB level and maxReq at service group| |
