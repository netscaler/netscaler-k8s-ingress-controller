
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
          annotations:
            ingress.citrix.com/backend-ca-secret: '{"service-test": "tls-backend-ca-secret"}'
            ingress.citrix.com/backend-secret: '{"service-test": "tls-backend-secret"}'
            ingress.citrix.com/secure-backend: 'True'
          name: ingress-demo
          namespace: netscaler
        spec:
          ingressClassName: netscaler
          rules:
          - host: example.com
            http:
              paths:
              - backend:
                  service:
                    name: service-test
                    port:
                      number: 443
                path: /
                pathType: Prefix
          tls:
          - hosts:
            - example.com
            secretName: tls-secret
        ---
        apiVersion: networking.k8s.io/v1
        kind: IngressClass
        metadata:
          name: netscaler
        spec:
          controller: citrix.com/ingress-controller
        ---
        