# How to load balance Ingress traffic to TCP or UDP based application

In a Kubernetes environment, an Ingress is an object that allows access to the Kubernetes services from outside the Kubernetes cluster. Standard Kubernetes Ingress resources assume that all the traffic is HTTP-based and do not cater to non-HTTP based protocols such as, TCP, TCP-SSL, and UDP. Hence, you cannot expose critical applications based on layer 7 protocols such as DNS, FTP, or LDAP using the standard Kubernetes Ingress.

Citrix provides a solution using Ingress annotations to load balance TCP or UDP based Ingress traffic. When you specify these annotations in the Ingress resource definition, the [Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/) configures the Citrix ADC to load balance TCP or UDP based Ingress traffic.

You can use the following [annotations](/docs/configure/annotations.md) in your Kubernetes Ingress resource definition to load balance the TCP or UDP based Ingress traffic:

-  `ingress.citrix.com/insecure-service-type`: The annotation enables L4 load balancing with TCP, UDP, or ANY as protocol for Citrix ADC.
-  `ingress.citrix.com/insecure-port`: The annotation configures the TCP port. The annotation is helpful when micro service access is required on a non-standard port. By default, port 80 is configured.

You can also use the standard Kubernetes solution of creating a `service` of `type LoadBalancer`  with Citrix ADC. You can find out more about [Service Type LoadBalancer in Citrix ADC](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).

**Sample:** Ingress definition for TCP-based Ingress.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/insecure-port: “6379”
    ingress.citrix.com/insecure-service-type: “tcp”
    kubernetes.io/ingress.class: “guestbook”
  name: redis-master-ingress
spec:
  defaultBackend:
    service:
      name: redis-master-pods
      port:
        number: 6379
```

**Sample:** Ingress definition for UDP-based Ingress. The following is a sample for Citrix ingress controller version 1.1.1:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/insecure-port: “5084”
    ingress.citrix.com/insecure-service-type: “udp”
  name: udp-ingress
spec:
  defaultBackend:
    service:
      name: frontend
      port:
        name: udp-53 /* Service port name defined in the service defination */
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

**Sample:** Ingress definition for UDP-based Ingress. The following is a sample for Citrix ingress controller version 1.5.25:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/insecure-port: “5084”
    ingress.citrix.com/insecure-service-type: “udp”
  name: udp-ingress
spec:
  defaultBackend:
    service:
      name: frontend
      port:
        number: 53
```

## Load balance Ingress traffic based on TCP over SSL

Citrix ingress controller provides an `‘ingress.citrix.com/secure-service-type: ssl_tcp` annotation that you can use to load balance Ingress traffic based on TCP over SSL.

**Sample:** Ingress definition for TCP over SSL based Ingress.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/secure-service-type: “ssl_tcp”
    ingress.citrix.com/secure_backend: ‘{“frontendcolddrinks”:”True”}’
    kubernetes.io/ingress.class: “colddrink”
  name: colddrinks-ingress
spec:
  defaultBackend:
    service:
      name: frontend-colddrinks
      port:
        number: 443
  tls:
  - secretName: “colddrink-secret”
```

## Monitor and improve the performance of your TCP or UDP based applications

Application developers can closely monitor the health of TCP or UDP based applications through rich monitors (such as TCP-ECV, UDP-ECV) in Citrix ADC. The ECV (extended content validation) monitors help in checking whether the
application is returning expected content or not.

Also, the application performance can be improved by using persistence methods such as `Source IP`. You can use these Citrix ADC features through [Smart Annotations](/docs/configure/annotations.md#smart-annotations) in
Kubernetes. The following is one such example:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/csvserver: ‘{“l2conn”:”on”}’
    ingress.citrix.com/frontend-ip: “192.168.1.1”
    ingress.citrix.com/insecure-port: “80”
    ingress.citrix.com/lbvserver: ‘{“mongodb-svc”:{“lbmethod”:”SRCIPDESTIPHASH”}}’
    ingress.citrix.com/monitor: ‘{“mongodbsvc”:{“type”:”tcp-ecv”}}’
  name: mongodb
spec:
  rules:
  - host: mongodb.beverages.com
    http:
      paths:
      - backend:
          service:
            name: mongodb-svc
            port:
              number: 80
        path: /
        pathType: Prefix
```

For more information on the different deployment options supported by the Citrix ingress controller, see [Deployment topologies](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deployment-topologies/).

For more information on deploying the Citrix ingress controller:

- [Deploy the Citrix ingress controller using YAML](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/)

- [Deploy the Citrix ingress controller using Helm charts](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-helm/)
