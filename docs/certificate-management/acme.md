# Deploy HTTPS web application on Kubernetes with the Citrix ingress controller and Let`s Encrypt using cert-manager

[Let's Encrypt](https://letsencrypt.org/docs/) and the ACME (Automatic Certificate Management Environment) protocol enables you to set up an HTTPS server and automatically obtain a browser-trusted certificate. To get a certificate for your website’s domain from Let’s Encrypt, you have to demonstrate control over the domain by accomplishing certain challenges. A challenge is one among a list of specified tasks that only someone who controls the domain can accomplish.

Currently there are two types of challenges:

-  **HTTP-01 challenge:** HTTP-01 challenges are completed by posting a specified file in a specified location on a website. Let's Encrypt CA verifies the file by making an HTTP request on the HTTP URI to satisfy the challenge.

-  **DNS-01 challenge:**  DNS01 challenges are completed by providing a computed key that is present at a DNS TXT record. Once this TXT record has been propagated across the internet, the ACME server can successfully retrieve this key via a DNS lookup. The ACME server can validate that the client owns the domain for the requested certificate. With the correct permissions, cert-manager automatically presents this TXT record for your specified DNS provider.

On successful validation of the challenge, a certificate is granted for the domain.

This topic provides information on how to securely deploy an HTTPS web application on a Kubernetes cluster, using:

- The Citrix ingress controller

- JetStack's [cert-manager](https://github.com/jetstack/cert-manager) to provision TLS certificates from the [Let's Encrypt project](https://letsencrypt.org/docs/).

## Prerequisites

Ensure that you have:

-  The domain for which the certificate is requested is publicly accessible.
-  Enabled RBAC on your Kubernetes cluster.
-  Deployed Citrix ADC MPX, VPX, or CPX deployed in Tier 1 or Tier 2 deployment model.

    In the Tier 1 deployment model, Citrix ADC MPX or VPX is used as an Application Delivery Controller (ADC). The Citrix ingress controller running in Kubernetes cluster configures the virtual services for services running on Kubernetes cluster. Citrix ADC runs the virtual service on the publicly routable IP address and offloads SSL for client traffic with the help of the Let's Encrypt generated certificate.
  
    In the Tier 2 deployment model, a TCP service is configured on the Citrix ADC (VPX/MPX) running outside the Kubernetes cluster. This service is created to forward the traffic to Citrix ADC CPX instances running in the Kubernetes cluster. Citrix ADC CPX ends the SSL session and load-balances the traffic to actual service pods.

- Deployed the Citrix ingress controller. Click [here](../deployment-topologies.md#deployment-topologies.html) for various deployment scenarios.

- Opened port 80 for the virtual IP address on the firewall for the Let's Encrypt CA to validate the domain for HTTP01 challenge.

- A DNS domain that you control, where you host your web application for the ACME DNS01 challenge.

- Administrator permissions for all deployment steps. If you encounter failures due to permissions, make sure you have administrator permissions.

## Install cert-manager

To install cert-manager, see the [cert-manager installation documentation](https://cert-manager.io/docs/installation/kubernetes/).

You can install cert-manager either using manifest files or Helm chart.

Once you install the cert-manager, verify that cert-manager is up and running as explained [verifying the installation](https://cert-manager.io/docs/installation/kubernetes/#verifying-the-installation).

## Deploy a sample web application

Perform the following to deploy a sample web application:

**Note:**

  [Kuard](https://github.com/kubernetes-up-and-running/kuard), a Kubernetes demo application is used for reference in this topic.

1.  Create a deployment YAML file (`kuard-deployment.yaml`) for Kuard with the following configuration:

        apiVersion: apps/v1
        kind: Deployment
        metadata:
          labels:
            app: kuard
          name: kuard
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: kuard
          template:
            metadata:
              labels:
                app: kuard
            spec:
              containers:
              - image: gcr.io/kuar-demo/kuard-amd64:1
                imagePullPolicy: Always
                name: kuard
                ports:
                - containerPort: 8080
                  protocol: TCP

2. Deploy the Kuard deployment file (`kuard-deployment.yaml`) to your cluster, using the following commands:

        % kubectl create -f kuard-deployment.yaml
        deployment.extensions/kuard created
        % kubectl get pod -l app=kuard
        NAME                     READY   STATUS    RESTARTS   AGE
        kuard-6fc4d89bfb-djljt   1/1     Running   0          24s

3. Create a service for the deployment. Create a file called `service.yaml` with the following configuration:

        apiVersion: v1
        kind: Service
        metadata:
          name: kuard
        spec:
          ports:
          - port: 80
            targetPort: 8080
            protocol: TCP
          selector:
            app: kuard

4. Deploy and verify the service using the following commands:

        % kubectl create -f service.yaml
        service/kuard created
        % kubectl get svc kuard
        NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
        kuard   ClusterIP   10.103.49.171   <none>        80/TCP    13s

5. Expose this service to outside world by creating an Ingress that is deployed on Citrix ADC CPX or VPX as Content switching virtual server.

    **Note:** Ensures that you change the value of `kubernetes.io/ingress.class` to your ingress class on which the Citrix ingress controller is started.

            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              annotations:
                kubernetes.io/ingress.class: citrix
              name: kuard
            spec:
              rules:
              - host: kuard.example.com
                http:
                  paths:
                  - backend:
                      service:
                        name: kuard
                        port:
                          number: 80
                    pathType: ImplementationSpecific

      **Note:**
        You must change the value of `spec.rules.host` to the domain that you control. Ensure that a DNS entry exists to route the traffic to Citrix ADC CPX or VPX.

6.  Deploy the Ingress using the following command:

        % kubectl apply -f ingress.yml
        ingress.extensions/kuard created
        
        root@ubuntu-:~/cert-manager# kubectl get ingress
        NAME    HOSTS               ADDRESS   PORTS   AGE
        kuard   kuard.example.com             80      7s

7.  Verify that the Ingress is configured on Citrix ADC CPX or VPX by using the following command:

        $ kubectl exec -it cpx-ingress-5b85d7c69d-ngd72 /bin/bash
        root@cpx-ingress-55c88788fd-qd4rg:/# cli_script.sh 'show cs vserver'
        exec: show cs vserver
        1)  k8s-192.168.8.178_80_http (192.168.8.178:80) - HTTP Type: CONTENT
          State: UP
          Last state change was at Sat Jan  4 13:36:14 2020
          Time since last state change: 0 days, 00:18:01.950
          Client Idle Timeout: 180 sec
          Down state flush: ENABLED
          Disable Primary Vserver On Down : DISABLED
          Comment: uid=MPPL57E3AFY6NMNDGDKN2VT57HEZVOV53Z7DWKH44X2SGLIH4ZWQ====
          Appflow logging: ENABLED
          Port Rewrite : DISABLED
          State Update: DISABLED
          Default:  Content Precedence: RULE
          Vserver IP and Port insertion: OFF
          L2Conn: OFF Case Sensitivity: ON
          Authentication: OFF
          401 Based Authentication: OFF
          Push: DISABLED  Push VServer:
          Push Label Rule: none
          Persistence: NONE
          Listen Policy: NONE
          IcmpResponse: PASSIVE
          RHIstate:  PASSIVE
          Traffic Domain: 0
        Done

        root@cpx-ingress-55c88788fd-qd4rg/# exit
        exit

8. Verify that the webpage is correctly being served when requested using the `curl` command.

        % curl -sS -D - kuard.example.com -o /dev/null
        HTTP/1.1 200 OK
        Content-Length: 1458
        Content-Type: text/html
        Date: Thu, 21 Feb 2019 09:09:05 GMT

## Configure issuing ACME certificate using the HTTP challenge

This section describes a way to issue the ACME certificate using the HTTP validation. If you want to use the DNS validation, skip this section and proceed to the [next section](#issuing-an-acme-certificate-using-dns-challenge).

The HTTP validation using cert-manager is a simple way of getting a certificate from Let's Encrypt for your domain. In this method, you prove ownership of a domain by ensuring that a particular file is present at the domain. It is assumed that you control the domain if you are able to publish the given file under a given path.

### Deploy the Let's Encrypt ClusterIssuer with the HTTP01 challenge provider

The cert-manager supports two different CRDs for configuration, an `Issuer`, scoped to a single namespace, and a `ClusterIssuer`, with cluster-wide scope.

For the Citrix ingress controller to use the Ingress from any namespace, use `ClusterIssuer`. Alternatively, you can also create an `Issuer` for each namespace on which you are creating an Ingress resource.

 For more information, see cert-manager documentation for [HTTP validation](https://cert-manager.io/docs/tutorials/acme/http-validation/).

1. Create a file called `issuer-letsencrypt-staging.yaml` with the following configuration:

        apiVersion: cert-manager.io/v1alpha2
        kind: ClusterIssuer
        metadata:
          name: letsencrypt-staging
        spec:
          acme:
            # You must replace this email address with your own.
            # Let's Encrypt will use this to contact you about expiring
            # certificates, and issues related to your account.
            email: user@example.com
            server: https://acme-staging-v02.api.letsencrypt.org/directory
            privateKeySecretRef:
              # Secret resource used to store the account's private key.
              name: example-issuer-account-key
            # Add a single challenge solver, HTTP01 using citrix
            solvers:
            - http01:
                ingress:
                  class: citrix

    `spec.acme.solvers[].http01.ingress.class` refers to the Ingress class of Citrix ingress controller. If the Citrix ingress controller has no ingress class, you do not need to specify this field.
    **Note:**
      This is a sample `Clusterissuer` of cert-manager.io/v1alpha2 resource. For more information, see [cert-manager http01 documentation](https://cert-manager.io/docs/configuration/acme/http01/).

      The staging Let's Encrypt server issues fake certificate, but it is not bound by [the API rate limits of the production server](https://letsencrypt.org/docs/rate-limits/). This approach lets you set up and test your environment without worrying about rate limits. You can repeat the same step for the Let's Encrypt production server.

2. After you edit and save the file, deploy the file using the following command:

        % kubectl apply -f issuer-letsencrypt-staging.yaml
        clusterissuer "letsencrypt-staging" created

3. Verify that the issuer is created and registered to the ACME server.

        % kubectl get issuer
        NAME                  AGE
        letsencrypt-staging   8d

4.  Verify that the `ClusterIssuer` is properly registered using the command `kubectl describe issuer letsencrypt-staging`:

        % kubectl describe issuer letsencrypt-staging
        
        Status:
          Acme:
            Uri:  https://acme-staging-v02.api.letsencrypt.org/acme/acct/8200869
          Conditions:
            Last Transition Time:  2019-02-11T12:06:31Z
            Message:               The ACME account was registered with the ACME server
            Reason:                ACMEAccountRegistered
            Status:                True
            Type:                  Ready

### Issue certificate for the Ingress object

Once `ClusterIssuer` is successfully registered, you can get a certificate for the Ingress domain 'kuard.example.com'.

You can request a certificate for the specified Ingress resource using the following methods:

- Adding `Ingress-shim` annotations to the ingress object.  

- Creating a `certificate` CRD object.

The first method is quick and simple, but if you need more customization and granularity in terms of certificate renewal, you can choose the second method. You can choose the method according to your needs.

#### Adding `Ingress-shim` annotations to the Ingress object

In this approach, you add the following two annotations to the Ingress object for which you request a certificate from the ACME server.


    certmanager.io/cluster-issuer: "letsencrypt-staging"

**Note**
    You can find all supported annotations from cert-manager for `Ingress-shim`, at [supported-annotations](https://cert-manager.readthedocs.io/en/latest/tasks/issuing-certificates/ingress-shim.html#supported-annotations).

Also, modify the `ingress.yaml` to use TLS by specifying a secret.

```YAML

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    certmanager.io/cluster-issuer: letsencrypt-staging
    kubernetes.io/ingress.class: citrix
  name: kuard
spec:
  rules:
  - host: kuard.example.com
    http:
      paths:
      - backend:
          service:
            name: kuard
            port:
              number: 80
        pathType: ImplementationSpecific
  tls:
  - hosts:
    - kuard.example.com
    secretName: kuard-example-tls
```

The `cert-manager.io/cluster-issuer: "letsencrypt-staging"` annotation tells cert-manager to use the `letsencrypt-staging` cluster-wide issuer to request a certificate from Let's Encrypt's staging servers. Cert-manager creates a `certificate` object that is used to manage the lifecycle of the certificate for `kuard.example.com`. The value for the domain name and challenge method for the certificate object is derived from the ingress object. Cert-manager manages the contents of the secret as long as the Ingress is present in your cluster.

Deploy the `ingress.yaml` file using the following command:

    % kubectl apply -f ingress.yml
    ingress.extensions/kuard configured
    % kubectl get ingress kuard
    NAME    HOSTS               ADDRESS   PORTS     AGE
    kuard   kuard.example.com             80, 443   4h39m

#### Create a certificate CRD resource

Alternatively, you can deploy a certificate CRD object independent of the Ingress object. Documentation of "certificate" CRD can be found at [HTTP validation](https://cert-manager.io/docs/tutorials/acme/http-validation/).

1. Create the `certificate.yaml` file with the following configuration:

 
        apiVersion: cert-manager.io/v1alpha2
        kind: Certificate
        metadata:
          name: example-com
          namespace: default
        spec:
          secretName: kuard-example-tls
          issuerRef:
            name: letsencrypt-staging
          commonName: kuard.example.com
          dnsNames:
          - www.kuard.example.com

  
   
    The  `spec.secretName` key is the name of the secret where the certificate is stored on successfully issuing the certificate.

2. Deploy the `certificate.yaml` file on the Kubernetes cluster:

        kubectl create -f certificate.yaml
        certificate.cert-manager.io/example-com created

3. Verify that certificate custom resource is created by the cert-manager which represents the certificate specified in the Ingress. After few minutes, if ACME validation goes well, certificate 'READY' status is set to true.

        % kubectl get certificates.cert-manager.io kuard-example-tls
        NAME                READY   SECRET              AGE
        kuard-example-tls   True    kuard-example-tls   3m44s


        % kubectl get certificates.cert-manager.io kuard-example-tls
        Name:         kuard-example-tls
        Namespace:    default
        Labels:       <none>
        Annotations:  <none>
        API Version:  cert-manager.io/v1alpha2
        Kind:         Certificate
        Metadata:
          Creation Timestamp:  2020-01-04T17:36:26Z
          Generation:          1
          Owner References:
            API Version:           extensions/v1beta1
            Block Owner Deletion:  true
            Controller:            true
            Kind:                  Ingress
            Name:                  kuard
            UID:                   2cafa1b4-2ef7-11ea-8ba9-06bea3f4b04a
          Resource Version:        81263
          Self Link:               /apis/cert-manager.io/v1alpha2/namespaces/default/certificates/kuard-example-tls
          UID:                     bbfa5e51-2f18-11ea-8ba9-06bea3f4b04a
        Spec:
          Dns Names:
            acme.cloudpst.net
          Issuer Ref:
            Group:      cert-manager.io
            Kind:       ClusterIssuer
            Name:       letsencrypt-staging
          Secret Name:  kuard-example-tls
        Status:
          Conditions:
            Last Transition Time:  2020-01-04T17:36:28Z
            Message:               Certificate is up to date and has not expired
            Reason:                Ready
            Status:                True
            Type:                  Ready
          Not After:               2020-04-03T16:36:27Z
        Events:
          Type    Reason        Age   From          Message
          ----    ------        ----  ----          -------
          Normal  GeneratedKey  24m   cert-manager  Generated a new private key
          Normal  Requested     24m   cert-manager  Created new CertificateRequest resource "kuard-example-tls-3030465986"
          Normal  Issued        24m   cert-manager  Certificate issued successfully

4. Verify that the secret resource is created.

        % kubectl get secret  kuard-example-tls
          NAME                TYPE                DATA   AGE
          kuard-example-tls   kubernetes.io/tls   3      3m13s


## Issuing an ACME certificate using the DNS challenge

This section describes a way to use the DNS validation to get the ACME certificate from Let'sEncrypt CA. With a DNS-01 challenge, you prove the ownership of a domain by proving that you control its DNS records. This is done by creating a TXT record with specific content that proves you have control of the domain's DNS records. For detailed explanation of DNS challenge and best security practices in deploying DNS challenge, see [A Technical Deep Dive: Securing the Automation of ACME DNS Challenge Validation](https://www.eff.org/deeplinks/2018/02/technical-deep-dive-securing-automation-acme-dns-challenge-validation).

**Note**
In this procedure, `route53` is used as the DNS provider. For other providers, see cert-manager [documentation of DNS validation](https://cert-manager.io/docs/configuration/acme/dns01/).

### Deploy the Let's Encrypt ClusterIssuer with the DNS01 challenge provider

Perform the following to deploy the Let's Encrypt ClusterIssuer with the DNS01 challenge provider:

1. Create an AWS IAM user account and download the secret access key ID and secret access key.
2. Grant the following IAM policy to your user:
   
      [Route53 access policy](http://docs.cert-manager.io/en/latest/tasks/issuers/setup-acme/dns01/route53.html)
   
3. Create a Kubernetes secret `acme-route53` in `kube-system` namespace.
   
   
       % kubectl create secret generic acme-route53 --from-literal secret-access-key=<secret_access_key>

4. Create an `Issuer` or `ClusterIssuer` with the DNS01 challenge provider.
   
    You can provide multiple providers under DNS01, and specify which provider to be used at the time of certificate creation.
    You must have access to the DNS provider for cert-manager to create a TXT record. Credentials are stored in the Kubernetes secret specified in `spec.dns01.secretAccessKeySecretRef`. For detailed instructions on how to obtain credentials, see the DNS provider documentation.

          
          apiVersion: cert-manager.io/v1alpha2
          kind: ClusterIssuer
          metadata:
            name: letsencrypt-staging
            spec:
              acme:
              # You must replace this email address with your own.
              # Let's Encrypt will use this to contact you about expiring
              # certificates, and issues related to your account.
                email: user@example.com
                server: https://acme-staging-v02.api.letsencrypt.org/directory
                privateKeySecretRef:
                  name: example-issuer-account-key
                solvers:
                - dns01:
                    route53:
                      region: us-west-2
                      accessKeyID: <IAMKEY>
                      secretAccessKeySecretRef:
                        name: acme-route53
                        key: secret-access-key
    **Note**
        Replace `user@example.com` with your email address. For each domain mentioned in a DNS01 stanza, cert-manager uses the provider's credentials from the referenced Issuer to create a TXT record called `_acme-challenge`. This record is then verified by the ACME server to issue the certificate. For more information about the DNS provider configuration, and the list of supported providers, see [DNS01 reference doc](https://cert-manager.io/docs/configuration/acme/dns01/).

5.  After you edit and save the file, deploy the file using the following command:

        % kubectl apply -f acme_clusterissuer_dns.yaml
        clusterissuer "letsencrypt-staging" created

6.  Verify if the issuer is created and registered to the ACME server using the following command:

        % kubectl get issuer
        NAME                  AGE
        letsencrypt-staging   8d

7.  Verify if the `ClusterIssuer` is properly registered using the command `kubectl describe issuer letsencrypt-staging`:

        Status:
          Acme:
            Uri:  https://acme-staging-v02.api.letsencrypt.org/acme/acct/8200869
          Conditions:
            Last Transition Time:  2019-02-11T12:06:31Z
            Message:               The ACME account was registered with the ACME server
            Reason:                ACMEAccountRegistered
            Status:                True
            Type:                  Ready

### Issue certificate for the Ingress object

Once the issuer is successfully registered, you can get a certificate for the ingress domain `kuard.example.com`. Similar to HTTP01 challenge, there are two ways you can request the certificate for a specified Ingress resource:

-  Adding `Ingress-shim` annotations to the Ingress object.

-  Creating a `certificate` CRD object. For detailed instructions, see [Create a Certificate CRD resource](#create-a-certificate-crd-resource).

#### Adding `Ingress-shim` annotations to the ingress object

Add the following annotation to the Ingress object along with the `spec.tls` section:

```YAML
certmanager.io/cluster-issuer: "letsencrypt-staging"
```

```YAML
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
    kubernetes.io/ingress.class: citrix
  name: kuard
spec:
  rules:
  - host: kuard.example.com
    http:
      paths:
      - backend:
          service:
            name: kuard
            port:
              number: 80
        pathType: ImplementationSpecific
  tls:
  - hosts:
    - kuard.example.com
    secretName: kuard-example-tls
```

The cert-manager creates a `Certificate` CRD resource with the DNS01 challenge. It uses credentials specified in the `ClusterIssuer` to create a TXT record in the DNS server for the domain you own. Then, Let's Encypt CA validates the content of the TXT record to complete the challenge.

**Adding a `Certificate` CRD resource**

Alternatively, you can explicitly create a certificate custom resource definition resource to trigger automatic generation of certificates.

1. Create the `certificate.yaml` file with the following configuration:
   
    
    

        apiVersion: cert-manager.io/v1alpha2
        kind: Certificate
        metadata:
          name: example-com
          namespace: default
        spec:
          secretName: kuard-example-tls
          issuerRef:
            name: letsencrypt-staging
          commonName: kuard.example.com
          dnsNames:
          - www.kuard.example.com
     
     
  
    After successful validation of the domain name, certificate READY status is set to True.

2. Verify that the certificate is issued.

  
         % kubectl get certificate kuard-example-tls
           NAME           READY   SECRET              AGE
           -example-tls   True    kuard-example-tls   10m
  
    You can watch the progress of the certificate as it is issued, using the following command:

         % kubectl describe certificates kuard-example-tls  | tail -n 6
           Not After:               2020-04-04T13:34:23Z
           Events:
           Type    Reason     Age    From          Message
           ----    ------     ----   ----          -------
           Normal  Requested  11m    cert-manager  Created new CertificateRequest resource "kuard-example-tls-3030465986"
           Normal  Issued     7m21s  cert-manager  Certificate issued successfully

## Verify certificate in Citrix ADC

Letsencrypt CA successfully validated the domain and issued a new certificate for the domain. A `kubernetes.io/tls` secret is created with the `secretName` specified in the `tls:` field of the Ingress. Also, cert-manager automatically initiates a renewal, 30 days before the expiry.

For HTTP challenge, cert-manager creates a temporary Ingress resource to route the Let's Encrypt CA generated traffic to cert-manager pods. On successful validations of the domain, this temporary Ingress is deleted.

1. Verify that the secret is created using the following command:
    

        % kubectl get secret kuard-example-tls
        NAME                TYPE                DATA   AGE
        kuard-example-tls   kubernetes.io/tls   3      30m

    The Citrix ingress controller picks up the secret and binds the certificate to the content switching virtual server on the Citrix ADC CPX. If there are any intermediate CA certificates, it is automatically linked to the server certificate and presented to the client during SSL negotiation.

2. Log on to Citrix ADC CPX and verify if the certificate is bound to the SSL virtual server.

        % kubectl exec -it cpx-ingress-55c88788fd-n2x9r bash -c cpx-ingress
        Defaulting container name to cpx-ingress.
        Use 'kubectl describe pod/cpx-ingress-55c88788fd-n2x9r -n default' to see all of the containers in this pod.

        % cli_script.sh 'sh ssl vs k8s-192.168.8.178_443_ssl'
        exec: sh ssl vs k8s-192.168.8.178_443_ssl

          Advanced SSL configuration for VServer k8s-192.168.8.178_443_ssl:
          DH: DISABLED
          DH Private-Key Exponent Size Limit: DISABLED	Ephemeral RSA: ENABLED		Refresh Count: 0
          Session Reuse: ENABLED		Timeout: 120 seconds
          Cipher Redirect: DISABLED
          ClearText Port: 0
          Client Auth: DISABLED
          SSL Redirect: DISABLED
          Non FIPS Ciphers: DISABLED
          SNI: ENABLED
          OCSP Stapling: DISABLED
          HSTS: DISABLED
          HSTS IncludeSubDomains: NO
          HSTS Max-Age: 0
          HSTS Preload: NO
          SSLv3: ENABLED  TLSv1.0: ENABLED  TLSv1.1: ENABLED  TLSv1.2: ENABLED  TLSv1.3: DISABLED
          Push Encryption Trigger: Always
          Send Close-Notify: YES
          Strict Sig-Digest Check: DISABLED
          Zero RTT Early Data: DISABLED
          DHE Key Exchange With PSK: NO
          Tickets Per Authentication Context: 1
        , P_256, P_384, P_224, P_5216)	CertKey Name: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS	Server Certificate for SNI

        7)	Cipher Name: DEFAULT
          Description: Default cipher list with encryption strength >= 128bit
        Done

        % cli_script.sh 'sh certkey'
        1)	Name: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS
          Cert Path: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS.crt
          Key Path: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS.key
          Format: PEM
          Status: Valid,   Days to expiration:89
          Certificate Expiry Monitor: ENABLED
          Expiry Notification period: 30 days
          Certificate Type:	"Client Certificate"	"Server Certificate"
          Version: 3
          Serial Number: 03B2B57EA9E61A93F1D05EA3272FA95203C2
          Signature Algorithm: sha256WithRSAEncryption
          Issuer:  C=US,O=Let's Encrypt,CN=Let's Encrypt Authority X3
          Validity
            Not Before: Jan  5 13:34:23 2020 GMT
            Not After : Apr  4 13:34:23 2020 GMT
          Subject:  CN=acme.cloudpst.net
          Public Key Algorithm: rsaEncryption
          Public Key size: 2048
          Ocsp Response Status: NONE
        2)	Name: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS_ic1
          Cert Path: k8s-GVWNYGVZKKRHKF7MZVTLOAEZYBS.crt_ic1
          Format: PEM
          Status: Valid,   Days to expiration:437
          Certificate Expiry Monitor: ENABLED
          Expiry Notification period: 30 days
          Certificate Type:	"Intermediate CA"
          Version: 3
          Serial Number: 0A0141420000015385736A0B85ECA708
          Signature Algorithm: sha256WithRSAEncryption
          Issuer:  O=Digital Signature Trust Co.,CN=DST Root CA X3
          Validity
            Not Before: Mar 17 16:40:46 2016 GMT
            Not After : Mar 17 16:40:46 2021 GMT
          Subject:  C=US,O=Let's Encrypt,CN=Let's Encrypt Authority X3
          Public Key Algorithm: rsaEncryption
          Public Key size: 2048
          Ocsp Response Status: NONE
        Done




The HTTPS webserver is now UP with a fake LE signed certificate. Next step is to move to production with the actual Let's Encrypt certificates.

## Move to production

After successfully testing with Let's Encrypt-staging, you can get the actual Let's Encrypt certificate.

You need to change Let's Encrypt endpoint from `https:acme-staging-v02.api.letsencrypt.org/directory` to `https:acme-v02.api.letsencrypt.org/directory`

Then, change the name of the ClusterIssuer from `letsencrypt-staging` to `letsencrypt-production`


```yaml

apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # You must replace this email address with your own.
    # Let's Encrypt will use this to contact you about expiring
    # certificates, and issues related to your account.
    email: user@example.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      # Secret resource used to store the account's private key.
      name: example-issuer-account-key
    # Add a single challenge solver, HTTP01 using citrix
    solvers:
    - http01:
        ingress:
          class: citrix
```


**Note:**
    Replace `user@example.com` with your email address.

Deploy the file using the following command:

    % kubectl apply -f letsencrypt-prod.yaml
    clusterissuer "letsencrypt-prod" created

Now repeat the procedure of modifying the annotation in Ingress or creating a CRD certificate which triggers the generation of new certificate.

**Note**
    Ensure that you delete the old secret so that cert-manager starts a fresh challenge with the production CA.

    % kubectl delete secret kuard-example-tls
    secret "kuard-example-tls" deleted

Once the HTTP website is up, you can redirect the traffic from HTTP to HTTPS using the annotation `ingress.citrix.com/insecure-termination: redirect` in the ingress object.

## Troubleshooting

Since the certificate generation involves multiple components, this section summarizes the troubleshooting techniques that you can use if there was failures.

### Verify the status of certificate generation

The certificate CRD object defines the life cycle management of generation and renewal of certificates. You can view the status of the certificate using the `kubectl describe` command as follows.

    % kubectl get certificate
    NAME                READY   SECRET              AGE
    kuard-example-tls   False   kuard-example-tls   9s

    %  kubectl describe certificate kuard-example-tls

    Status:
      Conditions:
        Last Transition Time:  2019-03-05T09:50:29Z
        Message:               Certificate does not exist
        Reason:                NotFound
        Status:                False
        Type:                  Ready
    Events:
      Type    Reason        Age   From          Message
      ----    ------        ----  ----          -------
      Normal  OrderCreated  22s   cert-manager  Created Order resource "kuard-example-tls-1754626579"

Also you can view the major certificate events using the `kubectl events` command:

    kubectl get events
    LAST SEEN   TYPE     REASON              KIND          MESSAGE
    36s         Normal   Started             Challenge     Challenge scheduled for processing
    36s         Normal   Created             Order         Created Challenge resource "kuard-example-tls-1754626579-0" for domain "acme.cloudpst.net"
    38s         Normal   OrderCreated        Certificate   Created Order resource "kuard-example-tls-1754626579"
    38s         Normal   CreateCertificate   Ingress       Successfully created Certificate "kuard-example-tls"

### Analyze logs from cert-manager

If there is a failure, first step is to analyze logs from the cert-manager component. Identify the cert-manager pod using the following command:

    % kubectl get po -n cert-manager
    NAME                                    READY   STATUS      RESTARTS   AGE
    cert-manager-76d48d47bf-5w4vx           1/1     Running     0          23h
    cert-manager-webhook-67cfb86d56-6qtxr   1/1     Running     0          23h
    cert-manager-webhook-ca-sync-x4q6f      0/1     Completed   4          23h

Here `cert-manager-76d48d47bf-5w4vx` is the main cert-manager pod, and other two pods are cert-manager webhook pods.

Get the logs of the cert-manager using the following command:

    % kubectl logs -f cert-manager-76d48d47bf-5w4vx -n cert-manager

If there is any failure to get the certificate, the ERROR logs give details about the failure.

### Check the Kubernetes secret

Use the `kubectl describe` command to verify if both certificates and key are populated in Kubernetes secret.

    % kubectl describe secret kuard-example-tls
    Name:         kuard-example-tls
    Namespace:    default
    Labels:       certmanager.k8s.io/certificate-name=kuard-example-tls
    Annotations:  certmanager.k8s.io/alt-names: acme.cloudpst.net
                  certmanager.k8s.io/common-name: acme.cloudpst.net
                  certmanager.k8s.io/issuer-kind: ClusterIssuer
                  certmanager.k8s.io/issuer-name: letsencrypt-staging

    Type:  kubernetes.io/tls

    Data
    ====
    tls.crt:  3553 bytes
    tls.key:  1679 bytes
    ca.crt:   0 bytes

If both `tls.crt` and `tls.key` are populated in the Kubernetes secret, certificate generation is complete. If only `tls.key` is present, certificate generation is incomplete. Analyze the cert-manager logs for more details about the issue.

### Analyze logs from the Citrix ingress controller

If a Kubernetes secret is generated and complete, but it is not uploaded to the Citrix ADC, you can analyze logs from the Citrix ingress controller using the following command.

    % kubectl logs -f cpx-ingress-685c8bc976-zgz8q  
