# Redirect HTTP to Secure

If you want to redirect the HTTP to secure HTTP, you can use the annotation `ingress.citrix.com/insecure-termination: 'redirect'` in the Ingress resource. Citrix ingress controller configures the NetScaler such that the HTTP traffic is redirected to secure TLS.
Following is an example of the ingress resource for back-end service `service-test`.

            kind: Ingress
            metadata:
              name: redirect-http-to-secure
              namespace: 'netscaler'
              annotations:
                kubernetes.io/ingress.class: 'netscaler'
                # annotation ingress.citrix.com/insecure-termination will redirect HTTP traffic to secure TLS.
                ingress.citrix.com/insecure-termination: 'redirect'
            spec:
              rules:
              - host: "example.com"
                http:
                  paths:
                  - backend:
                      serviceName: service-test
                      servicePort: 80
                    path: /
              tls:
              - hosts:
                - "example-test"
                secretName: tls-secret