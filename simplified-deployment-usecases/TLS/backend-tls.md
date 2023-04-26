
# Back-end TLS Support

Citrix ingress controller can configure NetScaler which can connect to a TLS enabled back-end server. The following annotations can be used for such configuration in the Ingress resource.

|Annotation| Description|
|----------|-------------|
| `ingress.citrix.com/secure-backend: "True"` | Enables secure back end communication to the back-end service. |
| `ingress.citrix.com/backend-secret: '{"< backend-service-name >": "< tls-secret-name >"}'`| Binds SSL Certificate for communicating with the back-end service |
| `ingress.citrix.com/backend-ca-secret: '{"< backend-service-name >": "< tls-secret-name >"}'`| CA certificate |

The following Ingress configures NetScaler to have a secure connection with the back-end service `service-test`.

        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: ingress-demo
          namespace: netscaler
          annotations:
           kubernetes.io/ingress.class: "netscaler"
           # annotation ingress.citrix.com/secure-backend will enable secure back end communication to the backend service.
           ingress.citrix.com/secure-backend: "True"
           # annotation ingress.citrix.com/backend-secret will bind SSL certificate for communicating with backend service
           ingress.citrix.com/backend-secret: '{"service-test": "tls-backend-secret"}'
           # annotaion ingress.citrix.com/backend-ca-secret will provide the CA certificate
           ingress.citrix.com/backend-ca-secret: '{"service-test": "tls-backend-ca-secret"}' 
        spec:
          tls:
          - secretName: tls-secret
            hosts: 
              - "example.com"
          rules:
          - host:  "example.com"
            http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service: 
                    name: service-test
                    port: 
                      number: 443