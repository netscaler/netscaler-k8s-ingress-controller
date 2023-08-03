# Create a self-signed certificate and linking into Kubernetes secret

Use the steps in the procedure to create a self-signed certificate using OpenSSL and link into Kubernetes secret. You can use this secret to secure your Ingress.

## Create a self-signed certificate

You can create a TLS secret by using the following steps. In this procedure, a self-signed certificate and key are created.
You can link it to the Kubernetes secret and use that secret in the Ingress for securing the Ingress.

        openssl genrsa -out cert_key.pem 2048
        openssl req -new -key cert_key.pem -out cert_csr.pem -subj "/CN=example.com"
        openssl x509 -req -in cert_csr.pem -sha256 -days 365 -extensions v3_ca -signkey cert_key.pem -CAcreateserial -out cert_cert.pem

**Note:** Here, `example.com` is used for reference. You must replace `example.com` with the required domain name.

**Note:** In the example, the generated certificate has a validity of one year as the days are mentioned as 365.

## Linking the certificate to a Kubernetes secret

Perform the following steps to link the certificate to the Kubernetes secret.

1.  Run the following command to create a Kubernetes secret based on the TLS certificate that you have created.

        kubectl create secret tls tls-secret --cert=cert_cert.pem --key=cert_key.pem

1.  Run the following command to view the secret that contains the TLS certificate information:

        kubectl get secret tls-secret

## Deploy the Ingress

 Create and apply the Ingress configuration. The following YAML can be used for reference.

    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: ingress-demo
      namespace: netscaler
      annotations:
       kubernetes.io/ingress.class: "netscaler"      
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
                  number: 80
