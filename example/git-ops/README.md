# Sample configuration for deploying Citrix API gateway with GitOps

This topic provides a sample configuration for deploying Citrix API gateway with GitOps.
GitOps is supported with the following CRDs for APIs and security information specified in the Swagger files on Git.

 -  rewritepolicy

 -  ratelimit

 -  authpolicy

 -  waf

 -  bot

1. Create a Kubernetes secret with the login information for your Citrix ADC.

        kubectl create secret generic nslogin --from-literal=username=<username> --from-literal=password=<password>

   >**Note:**
   >Replace `username` and `password` with the login credentials of your Citrix ADC VPX.

1. Deploy Citrix ingress controller and apply CRD definition files through the following Helm commands:

        helm repo add citrix https://citrix.github.io/citrix-helm-charts/
        helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=nslogin,nodeWatch=true,crds.install=true
    
    >**Note:**
    >Replace `NSIP` with Citrix ADC VPX IP address.

     To install a specific version of the Helm chart (for example: 1.18.15), use the following command:
     
        helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=nslogin,crds.install=true --version 1.18.5

1. Copy the Swagger files provided in the [SwaggerFiles](./SwaggerFiles) folder to the Git repository.

1. Launch a sample application as a service.

        kubectl apply -f echoserver.yaml 


   >**Note**: In this example, [echoserver](./echoserver.yaml) is used as the sample application. This command creates the `echoserver` application as a service.

1. Apply the `rewritepolicy` CRD template file `rewrite-crd-prefixurl-rewrite.yaml` in the [TemplateCRDFiles](./TemplateCRDFiles) folder.

        kubectl apply -f TemplateCRDFiles/rewrite-crd-prefixurl-rewrite.yaml

1. Create Kubernetes secret for the Git credentials.

        kubectl apply -f secret.yaml
     >**Note:**
     >Replace the `username` and `password` with appropriate base64 encoded credentials in the s`ecret.yaml` file.

1. Create the API Gateway CRD instance.

        kubectl apply -f api-gateway-crd-instance.yaml

   Update the API gateway CRD instance file (api-gateway-crd-instance.yaml) with the following information:

   - `repository`: Provide the GIT Repository information
   - `branch`: The branch on the Git repository that needs to be referred.
   - `files`:  The path of Swagger files to be monitored on Git.
   - `ipaddress`: Provide the Citrix ADC content switching virtual server VIP IP address (The listener IP address on Citrix ADC).
   - `port`: Provide the port information for the listener (For HTTP, port 80 and for HTTPS port 443).
   - `protocol`:  HTTP or HTTPS (If the protocol is HTTPS, then there is a need of certificate information to be provided as a secret).

1. Create a certificate for the Citrix ADC listener if the protocol is HTTPS.

        kubectl create secret tls cert1 --key="cert.key" --cert="cert.crt"

   >**Note:**
   Replace `cert.key` and `cert.crt`  with the certificates to be used. If the protocol is HTTP, there is no need to create the secret.

1. Based on the protocol selected in the API Gateway CRD, try accessing the application through `http://ipaddress/v2/play/play_api` or `https://ipaddress/v2/play/play_api` URLs .

   >**Note:**
   Replace `ipaddress` in the URL with the IP address of the Citrix ADC content switching virtual server VIP (the listener IP address on the Citrix ADC). Replace the `play_api` with the API that needs to be accessed (For example: `tennis)`.

1. Try to modify the Swagger file APIs on Git or the template rewritepolicy CRD to evaluate the GitOps functionality.

Similar to the way `rewritepolicy` is used for evaluation, you can validate `Ratelimit`, `Auth`, `WAF`, and `BOT` CRD functionalities by applying the corresponding template CRD shared in the `TemplateCRDFiles` directory.
