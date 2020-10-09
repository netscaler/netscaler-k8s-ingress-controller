# Multi-port services support

There are situations where you need to expose more than one port for a service. The Citrix ingress controller supports configuring multiple port definitions on a service.
You can provide a service port name (supported from the Citrix ingress controller version 1.9.20 onwards) or port number for a targeted back end service while configuring the Ingress rules.

## Example: Multi-port service

Following is an example for multi-port service definitions.

**Ingress**

```yml

apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: servicemultiportname
  annotations:
    ingress.citrix.com/frontend-ip: "192.101.12.111"
spec:
  rules:
    - host: app
      http:
        paths:
        - path: /v1
          backend:
              serviceName: myservice
              servicePort: insecure
    - host: app
      http:
        paths:
        - path: /v2
          backend:
              serviceName: my-service
              servicePort: secure
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
