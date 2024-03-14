# Redirect HTTP to Secure

If you want to redirect the HTTP to secure HTTP, you can use the annotation `ingress.citrix.com/insecure-termination: 'redirect'` in the Ingress resource. Citrix ingress controller configures the NetScaler such that the HTTP traffic is redirected to secure TLS.
Following is an example of the ingress resource for back-end service `service-test`.

            kind: Ingress
            metadata:
              annotations:
                ingress.citrix.com/insecure-termination: redirect
              name: redirect-http-to-secure
              namespace: netscaler
            spec:
              ingressClassName: netscaler
              rules:
              - host: example.com
                http:
                  paths:
                  - backend:
                      serviceName: service-test
                      servicePort: 80
                    path: /
              tls:
              - hosts:
                - example-test
                secretName: tls-secret
            ---
            apiVersion: networking.k8s.io/v1
            kind: IngressClass
            metadata:
              name: netscaler
            spec:
              controller: citrix.com/ingress-controller
            ---
            