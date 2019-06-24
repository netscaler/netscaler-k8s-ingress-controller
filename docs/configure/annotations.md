# Annotations

The following are the annotations supported by Citrix:

|**Annotations**|**Possible value**|**Description**|**Default**|
|---------------|------------------|---------------|-----------|
|ingress.citrix.com/frontend-ip| IP address | Use this annotation to customize the virtual IP address (VIP). This IP address is configured in Citrix ADC as VIP. The annotation is mandatory if you are using Citrix ADC VPX or MPX. </br>**Note:** Do not use the annotation if you want to use the Citrix ADC IP address as VIP. | Citrix ADC IP address is used as VIP. |
|ingress.citrix.com/secure-port|Port number |Use this annotation to configure the port for HTTPS traffic. This port is configured in Citrix ADC as a port value for corresponding Content Switching (CS) virtual server.| `443`|
|ingress.citrix.com/insecure-port| Port number | Use this annotation to configure the port for HTTP, TCP, or UDP traffic. This port is configured in Citrix ADC as a port value for corresponding CS virtual server.| `80` |
|ingress.citrix.com/insecure-termination| `allow`, `redirect`, or `disallow` |Use `allow` to allow HTTP traffic, Use `redirect` to redirect the HTTP request to HTTPS, or Use `disallow` if you want to drop the HTTP traffic. </br> For example: `ingress.citrix.com/insecure-termination: "redirect"`| `disallow` |
|ingress.citrix.com/secure-backend|In JSON form, list of services for secure-backend |Use `True`, if you want to establish secure HTTPS between Citrix ADC and the application, Use `False`, if you want to establish insecure HTTP connection Citrix ADC to the application. </br> For example: `ingress.citrix.com/secure-backend: {"app1":"True", "app2":"False", "app3":"True"}`| `False`|
|kubernetes.io/ingress.class|ingress class name| It is a way to associate a particular ingress resource with an ingress controller. </br> For example: `kubernetes.io/ingress.class:"Citrix"` | Configures all ingresses |
| ingress.citrix.com/secure-service-type | `ssl` or `ssl_tcp` | The annotation allows L4 load balancing with SSL over TCP as protocol. Use `ssl_tcp`, if you want to use SSL over TCP. | `ssl` |
|ingress.citrix.com/insecure-service-type| `http`, `tcp`, `udp`, or `any` | The annotation allows L4 load balancing with tcp/udp/any as protocol. Use `tcp`, if you want TCP as the protocol. Use `udp`, if you want UDP as the protocol.| `http` |
|ingress.citrix.com/service_weights|In JSON form, weights distribution (in %) among the back-end services. Sum of weight must be 100% | It allows CIC to play a role in canary deployment. The values must be in JSON format. For each back-end app in the ingress, there must be corresponding traffic %. All weights must be in % and sum must be 100. </br> For example: `ingress.citrix.com/service_weights: {"canary-app1":5, "baseline-app1":5 "production-app1":90}`. Here there are 3 apps and % traffic distribution is 5%, 5%, and 90%. | No weight distribution|

## Smart annotations

Smart annotation is an option provided by Citrix ingress controller to efficiently enable Citrix ADC features using Citrix ADC entity name. Citrix ingress controller converts the Ingress in Kubernetes to a set of Citrix ADC objects. You can efficiently control these objects using smart annotations.

!!! info "Important"
    To use smart annotations, you must have good understanding of Citrix ADC features and their respective entity names. For more information on Citrix ADC features and entity names, see [Citrix ADC Documentation](https://docs.citrix.com/en-us/citrix-adc/12-1.html).

Smart annotation takes JSON format as input. The key and value that you pass in the JSON format must match the Citrix ADC NITRO format. For more information on Citrix ADC NITRO API, see [Citrix ADC 12.1 REST APIs - NITRO Documentation](https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/latest/).

For example, if you want to enable SRCIPDESTIPHASH based lb method, you must use the corresponding NITRO key and value format `lbmethod`, `SRCIPDESTIPHASH` respectively.

The following table details the smart annotations provided by Citrix ingress controller:

| Citrix ADC Entity Name | Smart Annotation | Example |
| ----------------------- | ---------------- | ------- |
| lbvserver | ingress.citrix.com/lbvserver | `ingress.citrix.com/lbvserver: '{"citrix-svc":{"lbmethod":"SRCIPDESTIPHASH"}}'` |
| servicegroup | ingress.citrix.com/servicegroup | `ingress.citrix.com/servicegroup: '{"frontend":{"cip": "Enabled","cipHeader":"X-Forwarded-For"}}'` |
| monitor | ingress.citrix.com/monitor | `ingress.citrix.com/monitor: '{"frontend":{"type":"http"}}'` |

### Sample ingress YAML with smart annotations

The following is a sample Ingress YAML.  It includes smart annotations to enable Citrix ADC features using the entities such as, lbvserver, servicegroup, and monitor:

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: citrix
  annotations:
    ingress.citrix.com/insecure-port: "80"
    ingress.citrix.com/frontend-ip: "192.168.1.1"
    ingress.citrix.com/lbvserver: '{"citrix-svc":{"lbmethod":"LEASTCONNECTION", “persistenceType":"SOURCEIP"}}'
    ingress.citrix.com/servicegroup: '{"citrix-svc":{"usip":"yes"}}'
    ingress.citrix.com/monitor: '{"citrix-svc":{"type":"http"}}'
spec:
  rules:
  - host:  citrix.org
    http:
      paths:
      - path: /
        backend:
          serviceName: citrix-svc
          servicePort: 80
```

The sample Ingress YAML includes use cases related to the service, `citrix-svc`, and the following table explains the smart annotations used in the sample:

| Smart Annotation | Description |
| ---------------- | ----------- |
| `ingress.citrix.com/lbvserver: '{"citrix-svc":{"lbmethod":"LEASTCONNECTION", “persistenceType":"SOURCEIP"}}'` | Sets the load balancing method as [Least Connection](https://docs.citrix.com/en-us/citrix-adc/12-1/load-balancing/load-balancing-customizing-algorithms/leastconnection-method.html) and also configures [Source IP address persistence](https://docs.citrix.com/en-us/citrix-adc/12-1/load-balancing/load-balancing-persistence/source-ip-persistence.html). |
| `ingress.citrix.com/servicegroup: '{"citrix-svc":{"usip":"yes"}}'` | Enables [Use Source IP Mode (USIP)](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing/enabling-use-source-ip-mode.html) on the Ingress Citrix ADC device. When you enable USIP on the Citrix ADC, it uses the client's IP address for communication with the back-end pods. |
| `ingress.citrix.com/monitor: '{"citrix-svc":{"type":"http"}}'` | Creates a [custom HTTP monitor](https://docs.citrix.com/en-us/citrix-adc/12-1/load-balancing/load-balancing-custom-monitors.html) for the servicegroup. |
