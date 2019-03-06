# Deploying HTTPS web application on Kubernetes with Citrix Ingress Controller and Hashicorp Vault using cert-manager

This topic provies a sample workflow that leverages HashiCorp Vault as self-signed CA to automate TLS certificate provisioning, revocation, and renewal for an ingress resources deployed with Citrix ingress controller using cert-manager.

Specifically, the workflow uses the Vault PKI Secrets Engine to create a CA. This tutorial assumes that you've a Vault server installed and reachable from Kubernetes cluster.  Vault's PKI engine is suitable for internal applications and for external facing applications that require public trust, you can refer [automating TLS certificates using letsencrypt CA](./ACME.md)

The workflow uses a Vault secret engine and Auth Methods, refer the following Vault documentation for full list of features:

-  [Vault Secrets Engines](https://www.vaultproject.io/docs/secrets/index.html)

-  [Vault Auth Methods](https://www.vaultproject.io/docs/auth/index.html)

This topic provides you information on how to deploy an HTTPS web application on a Kubernetes cluster, using:

-  Citrix ingress controller (CIC)
-  JetStack's [cert-manager](https://github.com/jetstack/cert-manager) to provision TLS certificates from [Hashicorp Vault](https://www.vaultproject.io/)
-  [Hashicorp Vault](https://www.vaultproject.io/)

## Prerequisites

Ensure that you have:

-  The Vault server is installed, unsealed and is reachable from Kubernetes cluster.

-  Enabled RBAC  on your Kubernetes cluster.

-  Deployed Citrix ADC MPX, VPX or CPX deployed in Tier 1 or Tier 2 deployment model.

    In Tier 1 deployment model,  Citrix ADC MPX or VPX is used as a Application Delivery Controller (ADC) and Citrix Ingress Controller (CIC) running in kubernetes cluster configures the virtual services for the services running on kubernetes cluster. Citrix ADC runs the virtual service on the publicly routable IP address and offloads SSL for client traffic with the help of Let's Encrypt generated certificate.
  
    Similarly in Tier 2 deployment model, a TCP service is configured on the Citrix ADC (VPX/MPX) running outside the Kubernetes cluster to forward the traffic to Citrix ADC CPX instances running in kubernetes cluster.  Citrix ADC CPX ends the SSL session and load-balances the traffic to actual service pods.

-  Deployed Citrix ingress controller. Click [here](../deployment/README.md) for various deployment scenarios.

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
    root@ubuntu-vivek-225:~/cert-manager# kubectl get ingress
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

## Configure Hashicorp Vault as  Certificate Authority

Setup an intermediate CA certificate signing request using Hashicorp Vault. This Vault endpoint is used by cert-manager to sign the certificate for the ingress resources.

### Prerequistes

Ensure that you have installed the `jq` utility.

### Create a root CA

For the sample workflow you can generate your own Root Certificate Authority within the Vault. In a production environment, you should use an external Root CA to sign the intermediate CA that Vault uses to generate certificates. If you have a root CA generated elsewhere, skip this step. 

>**Note:**
>
> `PKI_ROOT` is a path where you mount the root CA, typically it is 'pki'. ${DOMAIN} in this procedure is `example.com`

```
% vault secrets enable -path="${PKI_ROOT}" pki

# Set the max TTL for the root CA to 10 years
% vault secrets tune -max-lease-ttl=87600h "${PKI_ROOT}"

% vault write -format=json "${PKI_ROOT}"/root/generate/internal \
 common_name="${DOMAIN} CA root" ttl=87600h | tee \
>(jq -r .data.certificate > ca.pem) \
>(jq -r .data.issuing_ca > issuing_ca.pem) \
>(jq -r .data.private_key > ca-key.pem)

#Configure the CA and CRL URLs:

% vault write "${PKI_ROOT}"/config/urls \
       issuing_certificates="${VAULT_ADDR}/v1/${PKI_ROOT}/ca" \
       crl_distribution_points="${VAULT_ADDR}/v1/${PKI_ROOT}/crl"
```

### Generate an intermediate CA

After creating the root CA,  create an intermediate CSR using the root CA. Perform the following:

1.  Enable pki from a different path `PKI_INT` from root CA, typically `pki\_int`. Use the following command:

    ```
    % vault secrets enable -path=${PKI_INT} pki
    Set the max TTL to 3 year

    % vault secrets tune -max-lease-ttl=26280h ${PKI_INT}
    ```

2.  Generate CSR for `${DOMAIN}` that needs to be signed by the root CA, the key is stored internally to vault. Use the following command:

    ```
    % vault write -format=json "${PKI_INT}"/intermediate/generate/internal \
    common_name="${DOMAIN} CA intermediate" ttl=43800h | tee \
    >(jq -r .data.csr > pki_int.csr) \
    >(jq -r .data.private_key > pki_int.pem)
    ```

3.  Generate and sign the `${DOMAIN}` certificate as an intermediate CA using root CA, store it as `intermediate.cert.pem`. Use the following command:

    ```
    % vault write -format=json "${PKI_ROOT}"/root/sign-intermediate csr=@pki_int.csr \
            format=pem_bundle \
            | jq -r '.data.certificate' > intermediate.cert.pem
    ```

    If you are using an external root CA, skip the above step and sign the CSR manually using root CA.

4.  Once the CSR is signed and the root CA returns a certificate, it needs to added back into the Vault using the following command:

    ```
    % vault write "${PKI_INT}"/intermediate/set-signed certificate=@intermediate.cert.pem

    ```

5.  Set the CA and CRL location using the following command:

    ```
    vault write "${PKI_INT}"/config/urls issuing_certificates="${VAULT_ADDR}/v1/${PKI_INT}/ca" crl_distribution_points="${VAULT_ADDR}/v1/${PKI_INT}/crl"

    ```

An intermediate CA is setup and can be used to sign certificates for ingress resources.

### Configure a role

A role is a logical name which maps to policies, administrator can control the certificate generation through the roles.

Create a role for the intermediate CA that provides a set of policies for issuing or signing the certificates using this CA.

There are many configurations that can be configured when creating roles, for more information see, [Vault role documentation](https://www.vaultproject.io/api/secret/pki/index.html#create-update-role).

For the workflow, create a role "***kube-ingress***" that allows you to sign certificates of `${DOMAIN}` and its subdomains with a TTL of 90 days.

```
# with a Max TTL of 90 days
vault write ${PKI_INT}/roles/kube-ingress \
          allowed_domains=${DOMAIN} \
          allow_subdomains=true \
          max_ttl="2160h"
```

## Create Approle based authentication

After configuring an intermediate CA to sign the certificates, you need to provide an authentication mechanism for cert-manager to use the vault for signing the certificates. Cert-manager supports Approle auth method which provides a way for the applications to access the Vault defined roles.

An "***AppRole***" represents a set of Vault policies and login constraints that must be met to receive a token with those policies. For detailed understanding of this Auth method, see [Approle documentation](https://www.vaultproject.io/docs/auth/approle.html).

### Create an Approle

Create a approle named "***Kube-role***" secret id must not expire for cert-manager to use this for authentication, hence dont set TTL or set it to 0. 

```
% vault auth enable approle of token ttl 5 minutes

% vault write auth/approle/role/kube-role \
    token_ttl=5m \
    token_max_ttl=10m
```

### Associate a policy with the Approle

Perform the following the associate a policy with Approle:

1.  Create a file `pki_int.hcl` with following configuration to allow the signing endpoints of the intermediate CA. 

    ```
    path "${PKI_INT}/sign/*" {
          capabilities = ["create","update"]
        }
    ```

2.  Add the file to a new policy called `kube_allow_sign`. Use the following command:

    ```
    vault policy write kube-allow-sign pki_int.hcl
    ```

3.  Update this policy to the approle. Use the following command:

    ```
    vault write auth/approle/role/kube-role policies=kube-allow-sign
    ```

The `kube-role` approle allows you to sign the CSR with intermediate CA.

### Generate the Role id and Secret id

Role id and Secret id is used by cert-manager to authenticate with Vault.

Generate role id and Secret id and encode the `secret_id` with Base64. Perform the following:

```
% vault read auth/approle/role/kube-role/role-id
role_id     db02de05-fa39-4855-059b-67221c5c2f63

% vault write -f auth/approle/role/kube-role/secret-id
secret_id               6a174c20-f6de-a53c-74d2-6018fcceff64
secret_id_accessor      c454f7e5-996e-7230-6074-6ef26b7bcf86

# encode secret_id with base64
% echo 6a174c20-f6de-a53c-74d2-6018fcceff64 | Base64
NmExNzRjMjAtZjZkZS1hNTNjLTc0ZDItNjAxOGZjY2VmZjY0Cg==

```

## Configure issuing certificates in Kubernetes

After you have configured the Vault as intermediate CA, and the Approle auth method for cert-manager to access the Vault. You need to configure the certificate for the ingress.

### Create a secret with Approle secret-id

Perform the following to create a secret with Approle scret-id:

1.  Create a secret file called `secretid.yaml` with following configuration:

    ```YAML
    apiVersion: v1
    kind: Secret
    type: Opaque
    metadata:
      name: cert-manager-vault-approle
      namespace: cert-manager
    data:
      secretId: "NmExNzRjMjAtZjZkZS1hNTNjLTc0ZDItNjAxOGZjY2VmZjY0Cg=="
    ````

    >**Note:**
    >
    >`data.secretId` is the base64 encoded SecretId generated in [Generate the Role id and Secret id](#generate-the-role-id-and-secret-id). If you're using a Issuer resource in the next step, Secret must be in same namespace as the `Issuer`. For `ClusterIssuer`, secret must be in `cert-manager` namespace.

2.  Deploy the secret file (`secretid.yaml`) using the following command:

    ```
    % kubectl create -f secretid.yaml 

    ```

### Deploy the Vault cluster issuer

cert-manager supports two different CRDs for configuration, an `Issuer`, which is scoped to a single namespace, and a `ClusterIssuer`, which is cluster-wide. For the workflow, you need to use `ClusterIssuer`.

Perform the following:

1.  Create a file called `issuer-vault.yaml` with the following configuration:

    ```YAML
    apiVersion: certmanager.k8s.io/v1alpha1
    kind: ClusterIssuer
    metadata:
      name: vault-issuer
    spec:
      vault:
        path: ${PKI_INT}/sign/kube-ingress
        server: https://vault_ip
        caBundle: <base64 encoded caBundle PEM file>
        auth:
          appRole:
            path: approle
            roleId: "db02de05-fa39-4855-059b-67221c5c2f63"
            secretRef:
              name: cert-manager-vault-approle
              key: secretId
    ```

    Replace `PKI_INT` with appropriate path of the intermediate CA. `SecretRef` is the kubernetes secret name created in the previos step. Replace `roleId` with the `role_id` retrieved from Vault.
    An optional base64 encoded caBundle in PEM format can be provided to validate the TLS connection to the Vault Server. When caBundle is set it replaces the CA bundle inside the container running the cert-manager. This parameter has no effect if the connection used is in plain HTTP.

2.  Deploy the file (`issuer-vault.yaml`) using the following command:

    ```
    % kubectl create -f issuer-vault.yaml
    ```

3.  Using the following command verify if the Vault cluster issuer is successfully authenticated with the Vault:

    ```
    % kubectl describe clusterIssuer vault-issuer  | tail -n 7
      Conditions:
        Last Transition Time:  2019-02-26T06:18:40Z
        Message:               Vault verified
        Reason:                VaultVerified
        Status:                True
        Type:                  Ready
    Events:                    <none>
    ```

### Create a "certificate" CRD object for the certificate

Once the issuer is successfully registered , you need to get the certificate for the ingress domain `kuard.example.com`.

You need to create a "certificate" resource with the commonName and dnsNames. For more information, see [cert-manager documenataion](https://cert-manager.readthedocs.io/en/latest/reference/certificates.html). You can specify multiple dnsNames which will be used for SAN field in the certificate.

To create a "cerficate" CRD object for the certificate, perform the following:

1.  Create a file called `certificate.yaml` with the following configuration:

    ```YAML
    apiVersion: certmanager.k8s.io/v1alpha1
    kind: Certificate
    metadata:
      name: kuard-example-tls
      namespace: default
    spec:
      secretName: kuard-example-tls
      issuerRef:
        kind: ClusterIssuer
        name: vault-issuer
      commonName: kuard.example.com
      duration: 720h
      #Renew before 7 days of expiry
      renewBefore: 168h
      commonName: kuard.example.com
      dnsNames:
      - www.kuard.example.com
    ```

    The certificate will have CN=`kuard.example.com` and SAN=`Kuard.example.com,www.kuard.example.com`.
    `spec.secretName` is the name of the secret where the certificate is stored after the certificate is issued successfully.

2.  Deploy the file (`certificate.yaml`) on the Kubernetes cluster using the following command:

    ```
    kubectl create -f certificate.yaml
    certificate.certmanager.k8s.io/kuard-example-tls created
    ```

### Verify if the certificate is issued

You can watch the progress of the certificate as it's issued using the following command:

```
% ubectl describe certificates kuard-example-tls  | grep -A5 Events
Events:
  Type    Reason      Age   From          Message
  ----    ------      ----  ----          -------
  Normal  CertIssued  48s   cert-manager  Certificate issued successfully
```

>**Important**:
>
>At this point, it is quite possible that you may encounter some error due to Vault policies, go back to vault and fix it.

After succesful signing, a `kubernetes.io/tls` secret is created with the `secretName` specified in the `Certificate` resource.

```
% kubectl get secret kuard-example-tls
NAME                TYPE                DATA   AGE
kuard-exmaple-tls   kubernetes.io/tls   3      4m20s
```

## Modify the ingress to use the generated Secret

Edit the original ingress and add a `spec.tls` section specifying the secret `kuard-example-tls` as shown below:

```YAML
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: kuard
  annotations:
    kubernetes.io/ingress.class: "citrix"
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

Deploy the ingress using the following command:

```
% kubectl apply -f ingress.yml
ingress.extensions/kuard created

% kubectl get ingress kuard
NAME    HOSTS               ADDRESS   PORTS     AGE
kuard   kuard.example.com             80, 443   12s

```

Logon to CPX and verify if the Certificate is bound to the SSL virtual server.

```
kubectl exec -it cpx-ingress-668bf6695f-4fwh8 bash
cli_script.sh 'shsslvs'
exec: shsslvs
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

root@cpx-ingress-668bf6695f-4fwh8:/# cli_script.sh 'shsslvs k8s-10.244.3.148:443:ssl'
exec: shsslvs k8s-10.244.3.148:443:ssl

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
, P_256, P_384, P_224, P_5216)	CertKey Name: k8s-LMO3O3U6KC6WXKCBJAQY6K6X6JO	Server Certificate for SNI

7)	Cipher Name: DEFAULT
	Description: Default cipher list with encryption strength >= 128bit
Done

root@cpx-ingress-668bf6695f-4fwh8:/# cli_script.sh 'sh certkey k8s-LMO3O3U6KC6WXKCBJAQY6K6X6JO'
exec: sh certkey k8s-LMO3O3U6KC6WXKCBJAQY6K6X6JO
	Name: k8s-LMO3O3U6KC6WXKCBJAQY6K6X6JO		Status: Valid,   Days to expiration:0
	Version: 3
	Serial Number: 524C1D9306F784A2F5277C05C2A120D5258D9A2F
	Signature Algorithm: sha256WithRSAEncryption
	Issuer:  CN=example.com CA intermediate
	Validity
		Not Before: Feb 26 06:48:39 2019 GMT
		Not After : Feb 27 06:49:09 2019 GMT
	Certificate Type:	"Client Certificate"	"Server Certificate"
	Subject:  CN=kuard.example.com
	Public Key Algorithm: rsaEncryption
	Public Key size: 2048
	Ocsp Response Status: NONE
	2)	 URI:http://127.0.0.1:8200/v1/pki_int/crl
	3)	VServer name: k8s-10.244.3.148:443:ssl	Server Certificate for SNI
Done

```

The HTTPS webserver is UP with the vault signed certificate. Cert-manager automatically renews the certificate as specified in the 'RenewBefore" parameter in the Certificate, before expiry of the certificate.

>**Note:**
>
>The vault signing the certificate will fail if a certificate's expiry is beyond the expiry of the root CA or intermediate CA, hence ensure that these CA certificates are renewed manually well before they expiry.




 



 


