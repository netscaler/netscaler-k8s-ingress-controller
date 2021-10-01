# Multi-port services support

There are situations where you need to expose more than one port for a service. The Citrix ingress controller supports configuring multiple port definitions on a service.
You can provide a service port name (supported from the Citrix ingress controller version 1.9.20 onwards) or port number for a targeted back end service while configuring the Ingress rules.

## Example: Multi-port service

Following is an example for multi-port service definitions.

**Ingress**

```yml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/frontend-ip: 192.101.12.111
  name: servicemultiportname
spec:
  rules:
  - host: app
    http:
      paths:
      - backend:
          service:
            name: myservice
            port:
              name: insecure
        path: /v1
        pathType: Prefix
  - host: app
    http:
      paths:
      - backend:
          service:
            name: my-service
            port:
              name: secure
        path: /v2
        pathType: Prefix
```                

**Multi-port service**

```yml

apiVersion: v1
kind: Service
metadata:
 name: myservice
spec:
 selector:
    app: myapp
 ports:
    - name: insecure
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: secure
      protocol: TCP
      port: 443
      targetPort: 9377
```
