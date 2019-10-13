# How to load balance Ingress traffic to TCP or UDP based application

In a Kubernetes environment, an Ingress is an object that allows access to the Kubernetes services from outside the Kubernetes cluster. Standard Kubernetes Ingress resources assume that all the traffic is HTTP-based and does not cater to non-HTTP based protocols such as, TCP, TCP-SSL, and UDP. Hence, critical applications based on L7 protocols such as DNS, FTP, LDAP, and so on, cannot be exposed using standard Kubernetes Ingress.

Please note that in addition to Ingress option, there is an alternate way to expose end user traffic to TCP applications, which is to use Kubernetes Service Type `LoadBalancer`. Please read more about how to use [Service Type LoadBalancer in Citrix ADC](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/type_loadbalancer.md)

Citrix ingress controller enables you to load balance TCP or UDP based Ingress traffic. It provides the following [annotations](/docs/configure/annotations.md) that you can use in your Kubernetes Ingress resource definition and load balance the TCP or UDP based Ingress traffic:

-  `ingress.citrix.com/insecure-service-type`: The annotation enables L4 load balancing with TCP, UDP, or ANY as protocol for Citrix ADC.
-  `ingress.citrix.com/insecure-port`: The annotation configures the TCP port. The annotation is helpful when micro service access is required on a non-standard port. By default, port 80 is configured.

**Sample:** Ingress definition for TCP-based Ingress.

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: redis-master-ingress
    annotations:
        kubernetes.io/ingress.class: “guestbook”
        ingress.citrix.com/insecure-service-type: “tcp”
        ingress.citrix.com/insecure-port: “6379”
spec:
    backend:
        serviceName: redis-master-pods
        servicePort: 6379
```

**Sample:** Ingress definition for UDP-based Ingress. The following is a sample for Citrix ingress controller version 1.1.1:

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: udp-ingress
    annotations:
        ingress.citrix.com/insecure-service-type: “udp”
        ingress.citrix.com/insecure-port: “5084”
spec:
    backend:
        serviceName: frontend
        servicePort: udp-53  /* Service port name defined in the service defination */
```

The following is a sample service definition where the service port name is defined as `udp-53`:

```yml
apiVersion: v1
kind: Service
metadata:
  name: bind
  labels:
    app: bind
spec:
  ports:
  - name: udp-53
    port: 53
    targetPort: 53
    protocol: UDP
  selector:
    name: bind
```

**Sample:** Ingress definition for UDP-based Ingress. The following is a sample for Citrix ingress controller version 1.4.392:

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: udp-ingress
    annotations:
        ingress.citrix.com/insecure-service-type: “udp”
        ingress.citrix.com/insecure-port: “5084”
spec:
    backend:
        serviceName: frontend
        servicePort: 53
```

## Load balance Ingress traffic based on TCP over SSL

Citrix ingress controller provides an `‘ingress.citrix.com/secure-service-type: ssl_tcp` annotation that you can use to load balance Ingress traffic based on TCP over SSL.

**Sample:** Ingress definition for TCP over SSL based Ingress.

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: colddrinks-ingress
    annotations:
        kubernetes.io/ingress.class: “colddrink”
        ingress.citrix.com/secure-service-type: “ssl_tcp”
        ingress.citrix.com/secure_backend: ‘{“frontendcolddrinks”:”True”}’
spec:
    tls:
    - secretName: “colddrink-secret”
    backend:
        serviceName: frontend-colddrinks
        servicePort: 443
```

## Monitor and improve the performance of your TCP or UDP based applications

Application developers can closely monitor the health of TCP or UDP based applications through rich monitors (such as TCP-ECV, UDP-ECV) in Citrix ADC. The ECV (extended content validation) monitors help in checking whether the
application is returning expected content or not.

Also, the application performance can be improved by using persistence methods such as `Source IP`. You can use these Citrix ADC features through [Smart Annotations](/docs/configure/annotations.md#smart-annotations) in
Kubernetes. The following is one such example:

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: mongodb
    annotations:
        ingress.citrix.com/insecure-port: “80”
        ingress.citrix.com/frontend-ip: “192.168.1.1”
        ingress.citrix.com/csvserver: ‘{“l2conn”:”on”}’
        ingress.citrix.com/lbvserver: ‘{“mongodb-svc”:{“lbmethod”:”SRCIPDESTIPHASH”}}’
        ingress.citrix.com/monitor: ‘{“mongodbsvc”:{“type”:”tcp-ecv”}}’
spec:
    rules:
    - host: mongodb.beverages.com
      http:
        paths:
        - path: /
          backend:
            serviceName: mongodb-svc
            servicePort: 80
```


