# Deploying HTTPS web application on Kubernetes with Citrix Ingress Controller and Let`s Encrypt using cert-manager

[Let's Encrypt](https://letsencrypt.org/docs/) and the ACME (Automatic Certificate Management Environment) protocol enables you to set up an HTTPS server and  automatically obtain a browser-trusted certificate. In order to get a certificate for your website’s domain from Let’sEncrypt, you have to demonstrate control over the domain. Currently there are two different challenge types, http-01 and dns-01.

A challenge is one of a list of specified tasks that only someone who controls the domain should be able to accomplish, such as:

-  **HTTP-01 challenge:** Posting a specified file in a specified location on a web site (the HTTP-01 challenge). LetsEncrypt CA will verify the file by making a HTTP request on the HTTP URI to satisfy the challenge.

-  **DNS-01 challenge:** Posting a specified DNS TXT record in the domain name system. Let's Encrypt will ask your domain's DNS servers for the value of the TXT record to satisfy the challenge.

On successful validation of the challenge, a certificate is granted for the domain.

This topic provides information on how to securely deploy an HTTPS web application on a Kubernetes cluster, using:

-  Citrix Ingress Controller (CIC)

-  JetStack's [cert-manager](https://github.com/jetstack/cert-manager) to provision TLS certificates from the [Let's Encrypt project](https://letsencrypt.org/docs/).

## Prerequisites

Ensure that you have:

-  Enabled RBAC on your Kubernetes cluster.

-  Deployed Citrix ADC MPX, VPX or CPX deployed in Tier 1 or Tier 2 deployment model.

    In Tier 1 deployment model,  Citrix ADC MPX or VPX is used as a Application Delivery Controller (ADC) and Citrix Ingress Controller (CIC) running in kubernetes cluster configures the virtual services for the services running on kubernetes cluster. Citrix ADC runs the virtual service on the publicly routable IP address and offloads SSL for client traffic with the help of Let's Encrypt generated certificate.
  
    Similarly in Tier 2 deployment model, a TCP service is configured on the Citrix ADC (VPX/MPX) running outside the Kubernetes cluster to forward the traffic to Citrix ADC CPX instances running in kubernetes cluster.  Citrix ADC CPX ends the SSL session and load-balances the traffic to actual service pods.

-  Deployed Citrix ingress controller. Click [here](../deployment/README.md) for various deployment scenarios.

-  Opened Port 80 for the Virtual IP address on the firewall for the Let's Encrypt CA to validate the domain for HTTP01 challenge.

-  A DNS domain that you control, where you host your web application for ACME DNS01 challenge.

-  Administrator permissions for all the deployment steps. If you encounter failures due to permissions, make sure you have administrator permission.

## Deploy cert-manager using the manifest file

To keep things simple, let's skip cert-manager's Helm installation, and instead use the supplied YAML manifests. Download the latest source of cert-manager from  `github.com/jetstack/cert-manager` repository using the following command:

```
wget https://github.com/jetstack/cert-manager/archive/v0.6.2.tar.gz
tar -zxvf v0.6.2.tar.gz
```

Then deploy the cert-manager using the following command:

```
kubectl apply -f deploy/manifests/cert-manager.yaml
```

Alternatively, you can also install the cert-manager with Helm, for more information see [cert-manager documentation](https://github.com/helm/charts/tree/master/stable/cert-manager)

Verify in the cert-manager is up and running using the following command:

```
% kubectl -n cert-manager get all
NAME                                       READY   STATUS    RESTARTS   AGE
pod/cert-manager-77fd74fb64-d68v7          1/1     Running   0          4m41s
pod/cert-manager-webhook-67bf86d45-k77jj   1/1     Running   0          4m41s

NAME                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/cert-manager-webhook   ClusterIP   10.108.161.154   <none>        443/TCP   13d

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cert-manager           1/1     1            1           13d
deployment.apps/cert-manager-webhook   1/1     1            1           13d

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/cert-manager-77fd74fb64          1         1         1       13d
replicaset.apps/cert-manager-webhook-67bf86d45   1         1         1       13d

NAME                                                COMPLETIONS   DURATION   AGE
job.batch/cert-manager-webhook-ca-sync              1/1           22s        13d
job.batch/cert-manager-webhook-ca-sync-1549756800   1/1           21s        10d
job.batch/cert-manager-webhook-ca-sync-1550361600   1/1           19s        3d8h

NAME                                         SCHEDULE   SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/cert-manager-webhook-ca-sync   @weekly    False     0        3d8h            13d
```

## Deploy a sample web application

Perform the following to deploy a sample web application:

> Note:
>
> [Kuard](https://github.com/kubernetes-up-and-running/kuard), a kubernetes demo application is used for reference in this topic.

1.  Create a deployment YAML file (`kuard-deployment.yaml`) for Kuard with the following configuration:

    ```YAML
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: kuard
    spec:
      replicas: 1
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
    ```

2.  Deploy Kuard deployment file (`kuard-deployment.yaml`) to your cluster, using the following commands:

    ```
    % kubectl create -f kuard-deployment.yaml
    deployment.extensions/kuard created
    % kubectl get pod -l app=kuard
    NAME                     READY   STATUS    RESTARTS   AGE
    kuard-6fc4d89bfb-djljt   1/1     Running   0          24s
    ```

3.  Create a service for the deployment. Create a file called `service.yaml` with the following configuration:

    ```YAML
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
    ```

4.  Deploy and verify the service using the following commands:

    ```
    % kubectl create -f service.yaml
    service/kuard created
    % kubectl get svc kuard
    NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
    kuard   ClusterIP   10.103.49.171   <none>        80/TCP    13s

    ```

5.  Expose this service to outside world by creating and Ingress that is deployed on Citrix ADC CPX or VPX as Content switching virtual server. 
    >**Note:**
    >
    > Ensure that you change `kubernetes.io/ingress.class` to your ingress class on which CIC is started.

    ```YAML
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: kuard
      annotations:
        kubernetes.io/ingress.class: "citrix"
    spec:
      rules:
      - host: kuard.example.com
        http:
          paths:
          - backend:
              serviceName: kuard
              servicePort: 80
    ```

    >**Important:**
    >
    >Change the value of `spec.rules.host` to the domain that you control. Ensure that a DNS entry exists to route the traffic to Citrix ADC CPX or VPX.

6.  Deploy the Ingress using the following command:

    ```
    % kubectl apply -f ingress.yml
    ingress.extensions/kuard created
    % kubectl get ingress
    NAME    HOSTS               ADDRESS   PORTS   AGE
    kuard   kuard.example.com             80      7s
    ```

7.  Verify if the ingress is configured on Citrix ADC CPX or VPX using the following command:

    ```
    kubectl exec -it cpx-ingress-5b85d7c69d-ngd72 /bin/bash
    root@cpx-ingress-5b85d7c69d-ngd72:/# cli_script.sh 'sh cs vs'
    exec: sh cs vs
    1)	k8s-10.244.1.50:80:http (10.244.1.50:80) - HTTP	Type: CONTENT
      State: UP
      Last state change was at Thu Feb 21 09:02:14 2019
      Time since last state change: 0 days, 00:00:41.140
      Client Idle Timeout: 180 sec
      Down state flush: ENABLED
      Disable Primary Vserver On Down : DISABLED
      Comment: uid=75VBGFO7NZXV7SCI4LSDJML2Q5X6FSNK6NXQPWGMDOYGBW2IMOGQ====
      Appflow logging: ENABLED
      Port Rewrite : DISABLED
      State Update: DISABLED
      Default: 	Content Precedence: RULE
      Vserver IP and Port insertion: OFF
      L2Conn: OFF	Case Sensitivity: ON
      Authentication: OFF
      401 Based Authentication: OFF
      Push: DISABLED	Push VServer:
      Push Label Rule: none
      Listen Policy: NONE
      IcmpResponse: PASSIVE
      RHIstate:  PASSIVE
      Traffic Domain: 0
    Done
    root@cpx-ingress-5b85d7c69d-ngd72:/# exit
    exit
    ```

8.  Verify if the page is correctly being served when requested using the `curl` command.

    ```
    % curl -sS -D - kuard.example.com -o /dev/null
    HTTP/1.1 200 OK
    Content-Length: 1458
    Content-Type: text/html
    Date: Thu, 21 Feb 2019 09:09:05 GMT

    ```

## Configure issuing ACME certificate using HTTP challenge

This section describes a way to issue ACME certificate using HTTP validation. If you want to use DNS validation , skip this section and proceed to the [next section](#issuing-an-acme-certificate-using-dns-challenge).

HTTP validation using cert-manager is very simple way of getting a certificate from Let's Encrypt for your domain,  wherein you prove ownership of a domain by ensuring that a particular file is present at the domain. It is assumed that you control the domain if you are able to publish the given file under a given path.

### Deploy the Let's Encrypt cluster issuer with http01 challenge provider

cert-manager supports two different CRDs for configuration, an `Issuer`, which is scoped to a single namespace, and a `ClusterIssuer`, which is cluster-wide.

For CIC to use ingress from any namespace,  use `ClusterIssuer`. Alternatively you can create an `Issuer` for each namespace on which you are creating an Ingress resource.

1.  Create a file called `issuer-letsencrypt-staging.yaml` with the following configuration: 

    ```YAML
    apiVersion: certmanager.k8s.io/v1alpha1
    kind: ClusterIssuer
    metadata:
      name: letsencrypt-staging
    spec:
      acme:
        # The ACME server URL
        server: https://acme-staging-v02.api.letsencrypt.org/directory
        # Email address used for ACME registration
        email: user@example.com
        # Name of a secret used to store the ACME account private key
        privateKeySecretRef:
          name: letsencrypt-staging
        # Enable the HTTP-01 challenge provider
        http01: {}
    ```

    >**Note:**
    >
    > http01 challenge provider is enabled in the `ClusterIssuer` CRD. Replace `user@example.com` with your email address. This is the email address that Let's Encrypt uses to communicate with you about certificates you request. For more information, see [Issuer reference docs](https://docs.cert-manager.io/en/latest/reference/issuers.html).
    >
    >The staging Let's Encrypt server issues fake certificate, but it is not bound by [the API rate limits of the production server](https://letsencrypt.org/docs/rate-limits/). This approach lets you set up and test your environment without worrying about rate limits. You can repeat the same step for LetsEncrypt Production server.

2.  After you edit and save the file, deploy the file using the following command:

    ```
    % kubectl apply -f issuer-letsencrypt-staging.yaml
    clusterissuer "letsencrypt-staging" created
    ```

3.  Verify in the issuer is created and registered to the ACME server.

    ```
    % kubectl get issuer
    NAME                  AGE
    letsencrypt-staging   8d
    ```

4.  Verify if the `ClusterIssuer` is properly registered using the command `kubectl describe issuer letsencrypt-staging`:

    ```
    Status:
      Acme:
        Uri:  https://acme-staging-v02.api.letsencrypt.org/acme/acct/8200869
      Conditions:
        Last Transition Time:  2019-02-11T12:06:31Z
        Message:               The ACME account was registered with the ACME server
        Reason:                ACMEAccountRegistered
        Status:                True
        Type:                  Ready
    ```

### Issue certificate for ingress object

Once the issuer is successfully registered , now lets proceed to get certificate for the ingress domain 'kuard.example.com'

You can request certificate for a given ingress resource using the following methods:

-  Adding `Ingress-shim` annotations to the ingress object.  

-  Creating a `certificate` CRD object.

First method is quick and simple, but if you need more customization and granularity in terms of certificate renewal, you can chose the second method. Depending on your selection, skip the other method.

#### Adding `Ingress-shim` annotations to Ingress object

In this approach, we'll add these two annotations to ingress object for which you request certificate to be issued by the ACME server.

```YAML
    kubernetes.io/tls-acme: "true"
    certmanager.k8s.io/cluster-issuer: "letsencrypt-staging"
```

>**Note:**
>
>You can find all supported annotations from cert-manager for ingress-shim, click [here](https://cert-manager.readthedocs.io/en/latest/tasks/issuing-certificates/ingress-shim.html#supported-annotations).

Also, modify the `ingress.yaml` to use TLS by specifying a secret.

```YAML
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: kuard
  annotations:
    kubernetes.io/ingress.class: "citrix"
    kubernetes.io/tls-acme: "true"
    certmanager.k8s.io/cluster-issuer: "letsencrypt-staging"
spec:
  tls:
  - hosts:
    - kuard.example.com
    secretName: kuard-example-tls
  rules:
  - host: kuard.example.com
    http:
      paths:
      - backend:
          serviceName: kuard
          servicePort: 80
```

The `kubernetes.io/tls-acme: "true"` annotation tells cert-manager to use the `letsencrypt-staging` cluster-wide issuer that was created earlier to request a certificate from Let's Encrypt's staging servers. Cert-manager creates a `certificate` object that is used to manage the life cycle of the certificate for `kuard.example.com`, and the value for the domain name and challenge method for the certificate object is derived from the ingress object. Cert-manager manages the contents of the secret as long as the Ingress is present in your cluster.

Deploy the `ingress.yaml` using the following command: 

```
% kubectl apply -f ingress.yml
ingress.extensions/kuard configured
% kubectl get ingress kuard
NAME    HOSTS               ADDRESS   PORTS     AGE
kuard   kuard.example.com             80, 443   4h39m
```

#### Create a Certificate CRD resource

Alternatively, you can deploy a certificate CRD object independent of ingress object. Documentation of "certificate" CRD can be found here.

Create a file with `certificate.yaml` with the following configuration:

```YAML
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
  name: kuard-example-tls
  namespace: default
spec:
  secretName: kuard-example-tls
  issuerRef:
    name: letsencrypt-staging
  commonName: kuard.example.com
  #Renew before 15 days of expiry
  renewBefore: 360h 
  dnsNames:
  - kuard.example.com
  acme:
    config:
    - http01:
        ingressClass: citrix
      domains:
      - kuard.example.com
```

`ingressClass` refers to the ingress class CIC or CPX is running and `spec.secretName` is the name of the secret where the certificate is stored on successful issuing the certificate.

Deploy the `certificate.yaml` on the Kubernetes cluster:

```
kubectl create -f certificate.yaml
certificate.certmanager.k8s.io/kuard-example-tls created
```

## Issuing an ACME certificate using DNS challenge

This section describes a way to use DNS validation to get ACME certificate from Let'sEncrypt CA. With a DNS-01 challenge, you prove the ownership of a domain by proving you control its DNS records. This is done by creating a TXT record with specific content that proves you have control of the domain's DNS records. For detailed explanation of DNS challenge and best security practices in deploying DNS challenge, see [A Technical Deep Dive: Securing the Automation of ACME DNS Challenge Validation](https://www.eff.org/deeplinks/2018/02/technical-deep-dive-securing-automation-acme-dns-challenge-validation).

### Deploy the Let's Encrypt cluster issuer with dns01 challenge provider

1.  Create an `Issuer` or `ClusterIssuer` with dns01 challenge provider. 

    You can provide multiple providers under dns01, and specify which provider to be used at the time of certificate creation.
    You need to have access to the DNS provider for cert-manager to create a TXT record, the credentials are stored in Kubernetes secret specified in `spec.dns01.secretAccessKeySecretRef`. For detailed instructions on how to obtain the credentials, see the DNS provider documentation.

    ```YAML
    apiVersion: certmanager.k8s.io/v1alpha1
    kind: ClusterIssuer
    metadata:
      name: letsencrypt-staging
    spec:
      acme:
        # The ACME server URL
        server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
        email: "user@example.com"
    # Name of a secret used to store the ACME account private key
        privateKeySecretRef:
          name: letsencrypt-staging
    # Enable the DNS-01 challenge provider
        dns01:
          providers:
          - name: dns
            route53:
              region: us-east-1
              hostedZoneID: YOURZONEID
              accessKeyID: YOURACCESSKEYID
              secretAccessKeySecretRef:
                name: acme-route53
                key: secret-access-key
    ```

    >**Note**:
    >
    >Replace `user@example.com` with your email address.
    >For each domain mentioned in a dns01 stanza, cert-manager will use the provider's credentials from the referenced Issuer to create a TXT record called _acme-challenge. This record will then be verified by the ACME server in order to issue the certificate. For more information about the DNS provider configuration, and the list of supported providers, see [dns01 reference doc](https://docs.cert-manager.io/en/latest/tasks/acme/configuring-dns01/).

2.  After you edit and save the file, deploy the file using the following command:

    ```
    % kubectl apply -f issuer-letsencrypt-staging.yaml
    clusterissuer "letsencrypt-staging" created
    ```

3.  Verify if the issuer is created and registered to the ACME server using the following command:

    ```
    % kubectl get issuer
    NAME                  AGE
    letsencrypt-staging   8d
    ```

4.  Verify if the `ClusterIssuer` is properly registered using the command `kubectl describe issuer letsencrypt-staging`:

    ```
    Status:
      Acme:
        Uri:  https://acme-staging-v02.api.letsencrypt.org/acme/acct/8200869
      Conditions:
        Last Transition Time:  2019-02-11T12:06:31Z
        Message:               The ACME account was registered with the ACME server
        Reason:                ACMEAccountRegistered
        Status:                True
        Type:                  Ready
    ```

### Issue certificate for ingress object

Once the issuer is successfully registered, lets proceed to get certificate for the ingress domain `kuard.example.com`. Similar to http01 challenge, there are two ways you can request the certificate for a given ingress resource:

-  Adding `Ingress-shim` annotations to the ingress object.

-  Creating a `certificate` CRD object. For detailed instructions, see [Create a Certificate CRD resource](#create-a-certificate-crd-resource)

#### Adding `Ingress-shim` annotations to the ingress object

Add the following annotations to the ingress object along with `spec.tls` section:

```YAML
    kubernetes.io/tls-acme: "true"
    certmanager.k8s.io/cluster-issuer: "letsencrypt-staging"
    certmanager.k8s.io/acme-challenge-type: "dns01"
    certmanager.k8s.io/acme-dns01-provider: dns
```

```YAML
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: kuard
  annotations:
    kubernetes.io/ingress.class: "citrix"
    kubernetes.io/tls-acme: "true"
    certmanager.k8s.io/cluster-issuer: "letsencrypt-staging"
    certmanager.k8s.io/acme-challenge-type: "dns01"
    certmanager.k8s.io/acme-dns01-provider: dns
spec:
  tls:
  - hosts:
    - kuard.example.com
    secretName: kuard-example-tls
  rules:
  - host: kuard.example.com
    http:
      paths:
      - backend:
          serviceName: kuard
          servicePort: 80
```

The cert-manager creates a `Certificate` CRD resource with dns01 challenge and it uses the credentials given in the `ClusterIssuer` to create a TXT record in the DNS server for the domain you own. Then, Let's Encrypt CA validates the content of the TXT record to complete the challenge.

## Verify if the certificate is issued

For HTTP challenge, cert-manager will create a temporary ingress resource to route the Let's Encrypt CA generated traffic to cert-manager pods. On successful validations of the domain, this temporary ingress is deleted.

You can watch the progress of the certificate as it's issued, use the following command:

```
% kubectl describe certificates kuard-example-tls  | tail -n 6
  Type    Reason         Age                From          Message
  ----    ------         ----               ----          -------
  Normal  Generated      25m                cert-manager  Generated new private key
  Normal  OrderCreated   14m (x2 over 25m)  cert-manager  Created Order resource "kuard-example-tls-1006173429"
  Normal  OrderComplete  13m (x2 over 25m)  cert-manager  Order "kuard-example-tls-1006173429" completed successfully
  Normal  CertIssued     13m (x2 over 25m)  cert-manager  Certificate issued successfully
```

Letsencrypt CA successfully validated the domain and issued a new certificate for the domain. A `kubernetes.io/tls` secret is created with the `secretName` specified in the `tls:` field of the Ingress. Also, cert-manager automatically initiates a renewal, 30 days before the expiry.

Verify in the secret is created using the following command:

```
% kubectl get secret kuard-example-tls
NAME                TYPE                DATA   AGE
kuard-example-tls   kubernetes.io/tls   3      30m
```

The secret is picked up by Citrix ingress controller and binds the certificate to the Content switching virtual server on the Citrix ADC CPX.

Logon to Citrix ADC CPX and verify if the certificate is bound to the SSL virtual server.

```
kubectl exec -it cpx-ingress-668bf6695f-4fwh8 bash
root@cpx-ingress-668bf6695f-4fwh8:/# cli_script.sh 'sh ssl vserver'
exec: sh ssl vserver
1) Vserver Name: k8s-10.244.3.148:443:ssl
	DH: DISABLED
	DH Private-Key Exponent Size Limit: DISABLED	Ephemeral RSA: ENABLED		Refresh Count: 0
	Session Reuse: ENABLED		Timeout: 120 seconds
	Cipher Redirect: DISABLED
	SSLv2 Redirect: DISABLED
	ClearText Port: 0
	Client Auth: DISABLED
	SSL Redirect: DISABLED
	Non FIPS Ciphers: DISABLED
	SNI: ENABLED
	OCSP Stapling: DISABLED
	HSTS: DISABLED
	HSTS IncludeSubDomains: NO
	HSTS Max-Age: 0
	SSLv2: DISABLED  SSLv3: ENABLED  TLSv1.0: ENABLED  TLSv1.1: ENABLED  TLSv1.2: ENABLED  TLSv1.3: DISABLED
	Push Encryption Trigger: Always
	Send Close-Notify: YES
	Strict Sig-Digest Check: DISABLED
	Zero RTT Early Data: DISABLED
	DHE Key Exchange With PSK: NO
	Tickets Per Authentication Context: 1
Done
root@cpx-ingress-668bf6695f-4fwh8:/# cli_script.sh 'sh ssl vserver k8s-10.244.3.148:443:ssl'
exec: sh ssl vserver k8s-10.244.3.148:443:ssl

	Advanced SSL configuration for VServer k8s-10.244.3.148:443:ssl:
	DH: DISABLED
	DH Private-Key Exponent Size Limit: DISABLED	Ephemeral RSA: ENABLED		Refresh Count: 0
	Session Reuse: ENABLED		Timeout: 120 seconds
	Cipher Redirect: DISABLED
	SSLv2 Redirect: DISABLED
	ClearText Port: 0
	Client Auth: DISABLED
	SSL Redirect: DISABLED
	Non FIPS Ciphers: DISABLED
	SNI: ENABLED
	OCSP Stapling: DISABLED
	HSTS: DISABLED
	HSTS IncludeSubDomains: NO
	HSTS Max-Age: 0
	SSLv2: DISABLED  SSLv3: ENABLED  TLSv1.0: ENABLED  TLSv1.1: ENABLED  TLSv1.2: ENABLED  TLSv1.3: DISABLED
	Push Encryption Trigger: Always
	Send Close-Notify: YES
	Strict Sig-Digest Check: DISABLED
	Zero RTT Early Data: DISABLED
	DHE Key Exchange With PSK: NO
	Tickets Per Authentication Context: 1
, P_256, P_384, P_224, P_5216)	CertKey Name: k8s-VN4RXHGMCZSTMQZOQ3XGBVMM2OO	Server Certificate for SNI

7)	Cipher Name: DEFAULT
	Description: Default cipher list with encryption strength >= 128bit
Done


rcli_script.sh 'sh certkey k8s-VN4RXHGMCZSTMQZOQ3XGBVMM2OO'
exec: sh certkey k8s-VN4RXHGMCZSTMQZOQ3XGBVMM2OO
	Name: k8s-VN4RXHGMCZSTMQZOQ3XGBVMM2OO		Status: Valid,   Days to expiration:89
	Version: 3
	Serial Number: FA0DFEDAB578C0228273927DA7C5E17CF098
	Signature Algorithm: sha256WithRSAEncryption
	Issuer:  CN=Fake LE Intermediate X1
	Validity
		Not Before: Feb 25 08:00:38 2019 GMT
		Not After : May 26 08:00:38 2019 GMT
	Certificate Type:	"Client Certificate"	"Server Certificate"
	Subject:  CN=kuard.example.com
	Public Key Algorithm: rsaEncryption
	Public Key size: 2048
	Ocsp Response Status: NONE
	2)	VServer name: k8s-10.244.3.148:443:ssl	Server Certificate for SNI
Done
```

The HTTPS webserver is now UP with fake LE signed certificate. Next step is to move to production with actual Letsencrypt certificate.

## Move to production

After successfully testing with LetsEncrypt-staging, you can get the actual LetsEncrypt certificates.

You need to change Letsencrypt endpoint from `https:acme-staging-v02.api.letsencrypt.org/directory` to `https:acme-v02.api.letsencrypt.org/directory`

Then, change the name of the ClusterIssuer from `letsencrypt-staging` to `letsencrypt-production`

```YAML
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
  namespace: cert-manager
spec:
  acme:
    email: user@example.com
    http01: {}
    privateKeySecretRef:
      name: letsencrypt-prod
    server: https://acme-v02.api.letsencrypt.org/directory
```

>**Note:** Replace `user@example.com` with your email address.

Deploy the file using the following command:

```
% kubectl apply -f letsencrypt-prod.yaml
clusterissuer "letsencrypt-prod" created
```

Now repeat the procedure of modifying the annotation in ingress or creating a new CRD certificate which will trigger the generation of new certificate.

>**Note:**
>Ensure that you delete the old secret so that cert-manager starts a fresh challenge with the production CA.

```
% kubectl delete secret kuard-example-tls
secret "kuard-example-tls" deleted
```

Once the HTTP website is up, you can redirect the traffic from HTTP to HTTPS using the annotation `ingress.citrix.com/insecure-termination: redirect` in the ingress object.

## Troubleshooting

Since the certificate generation involves multiple components, this section summarizes the troubleshooting techniques that you can use in case of failures.

### Verify the current status of certificate generation

Certificate CRD object defines the life cycle management of generation and renewal of the certificates. You can view the status of the certificate using `kubectl describe` command as shown below.

```
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
```

Also you can view the major certificate events using the `kubectl events` commands:

```
kubectl get events
LAST SEEN   TYPE     REASON              KIND          MESSAGE
36s         Normal   Started             Challenge     Challenge scheduled for processing
36s         Normal   Created             Order         Created Challenge resource "kuard-example-tls-1754626579-0" for domain "acme.cloudpst.net"
38s         Normal   OrderCreated        Certificate   Created Order resource "kuard-example-tls-1754626579"
38s         Normal   CreateCertificate   Ingress       Successfully created Certificate "kuard-example-tls"
```

### Analyse the logs from cert-manager

In case of failure, first step is to analyse the logs from the cert-manager component.  Identify the cert-manager pod using  the following command:

```
kubectl get po -n cert-manager
NAME                                    READY   STATUS      RESTARTS   AGE
cert-manager-76d48d47bf-5w4vx           1/1     Running     0          23h
cert-manager-webhook-67cfb86d56-6qtxr   1/1     Running     0          23h
cert-manager-webhook-ca-sync-x4q6f      0/1     Completed   4          23h
```

Here `cert-manager-76d48d47bf-5w4vx` is the main cert-manager pod, and other two pods are cert-manager webhook pods.

Get the logs of the cert-manager using the following command:

```
kubectl logs -f cert-manager-76d48d47bf-5w4vx -n cert-manager
```

If there is any failure to get the certificate, the ERROR logs gives details about the failure.

### Check the Kubernetes secret

Use `kubectl describe` command to verify if both certificates and key is populated in Kubernetes secret.

```
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

```

If both `tls.crt` and `tls.key` are  populated in the kubernetes secret, certificate generation is complete.  If only tls.key is present, certificate generation is incomplete, Analyze the cert-manager logs for more details about the issue.

### Analyse the logs from Citrix Ingress Controller

If kubernetes secret is generated and complete, but this secret is not uploaded to Citrix ADC CPX or VPX, you can analyze the logs from citrix ingress controller using `kubectl logs` command.

```
% kubectl logs -f cpx-ingress-685c8bc976-zgz8q
```