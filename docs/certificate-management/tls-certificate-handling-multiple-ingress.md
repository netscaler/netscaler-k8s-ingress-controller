# TLS certificate handling for multiple ingress

## Overview

The TLS handshake is the process that your web browser performs in the background process to create an HTTPs connection for you. In general, this process gets completed in a few seconds. Whenever a request comes to the server for enabling an HTTPs connection, the client and the server perform the TLS handshake. In a situation when there is a higher load to the server, the response from the server might become slow because the server has to complete the TLS handshake process.

To avoid this additional processing time from the server, the Citrix ADC instance can do the TLS handshake process to ensure the server response time is faster. A Citrix ADC appliance configured for TLS acceleration transparently accelerates TLS transactions by offloading TLS processing from the server. To configure TLS offloading, you need to configure a virtual server to intercept and process TLS transactions, and send the decrypted traffic to the server (unless you configure end-to-end encryption, in which case the traffic is re-encrypted). Upon receiving the response from the server, the appliance completes the secure transaction with the client. From the client’s perspective, the transaction seems to be directly with the server.

Configuring TLS offloading requires a TLS certificate and a key pair, which you must obtain if you do not already have a TLS certificate. Other TLS-related tasks that you might need to perform includes managing certificates, managing certificate revocation lists, configuring client authentication, and managing TLS actions and policies.

A non-FIPS Citrix ADC appliance stores the server’s private key on the hard disk. On a FIPS appliance, the key is stored in a cryptographic module known as a hardware security module (HSM).

All Citrix ADC instances that do not support a FIPS card (including virtual appliances) support the Thales nShield® Connect and SafeNet external HSMs. (MPX 9700/10500/12500/15500 appliances do not support an external HSM.)

!!! note "Note"
    FIPS-related options for some of the TLS configuration procedures described in this topic are specific to a FIPS-enabled Citrix ADC appliance.

## TLS Offload

In the Citrix ADC instance, the TLS offloading is configured in the Content Switching Virtual Server (CS Vserver). By default, each Citrix ADC instance can have one certificate and the application receives the traffic based on the policy bound to the certificate. However, you have the Server Name Indication (SNI) option to have multiple certificates bound to multiple applications. If you want to have one certificate, then you can disable the SNI option and the certificate is bound to the CS Vserver.

You can define all these requirements (certificate and domain name) in the Citrix Ingress Controller.

## Define certificates to Citrix Ingress Controller

Using the yaml, you can define a certificate under `args` and under `tls` section. If you have defined a certificate under `args`, then the certificate is bound to non-SNI certificate. If you have defined a certificate under `tls`, then the certificate is bound to SNI certificate.

The following is an example yaml that defines a certificate:

```yaml
---

kind: ClusterRole

apiVersion: rbac.authorization.k8s.io/v1beta1

metadata:

name: cic-k8s-role

rules:

- apiGroups: [""]

resources: ["services", "endpoints", "ingresses", "pods", "secrets", "nodes"]

verbs: ["*"]



- apiGroups: ["extensions"]

resources: ["ingresses", "ingresses/status"]

verbs: ["*"]

---

kind: ClusterRoleBinding

apiVersion: rbac.authorization.k8s.io/v1beta1

metadata:

name: cic-k8s-role

roleRef:

apiGroup: rbac.authorization.k8s.io

kind: ClusterRole

name: cic-k8s-role

subjects:

- kind: ServiceAccount

name: cic-k8s-role

namespace: default

apiVersion: rbac.authorization.k8s.io/v1

---

apiVersion: v1

kind: ServiceAccount

metadata:

name: cic-k8s-role

namespace: default

---

apiVersion: v1

kind: Pod

metadata:

name: cic-k8s-ingress-controller

labels:

app: cic-k8s-ingress-controller

spec:

serviceAccountName: cic-k8s-role

containers:

- name: cic-k8s-ingress-controller

image: "quay.io/citrix/citrix-k8s-ingress-controller:latest"

env:

# Set Citrix ADC NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)

- name: "NS_IP"

value: "x.x.x.x"

# Set username for Nitro

- name: "NS_USER"

valueFrom:

secretKeyRef:

name: nslogin

key: username

# Set user password for Nitro

- name: "NS_PASSWORD"

valueFrom:

secretKeyRef:

name: nslogin

key: password

# Set log level

- name: "EULA"

value: "yes"

args:

- --ingress-classes

   citrix

- --default-ssl-certificate

   # <secret name>
   Colddrink-secret

- --feature-node-watch

false

imagePullPolicy: Always
```

!!! note "Note"
    You must provide a default secret name in the yaml.

## Set up HTTP(S) Load Balancing with Ingress

**TLS**:

You can secure an Ingress by specifying a secret containing TLS pem. CIC configures the certificate resource in Citrix ADC and use it to encrypt the communication. The example in this section shows you how to secure an Ingress using TLS/SSL certificates.

**Import Existing Certificate**:

To import an existing certificate or key pair into a Kubernetes cluster, the following sample command can be used:

```bash
$ kubectl create secret tls colddrink-secret --namespace=team-colddrink --cert=path/to/tls.cert --key=path/to/tls.key

secret "colddrink-secret" created
```

The secret with a PEM formatted certificate under `tls.crt` key and the PEM formatted private key under `tls.key` key is created.

You can use the same command in the yaml:

```
apiVersion: v1
kind: Secret
metadata:
  name: colddrink-secret
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
```

The secret that is created can be used with CIC to secure the communication from client to Citrix ADC using TLS.

You can provide the secret to the yaml in two ways:

-  **Using CIC yaml file** - This is the non-SNI enabled HTTP traffic that is the default certificate for all HTTPs incoming traffic. This certificate does not have the full domain name.

-  **Using ingress yaml file** - This is the SNI-enabled HTTPs traffic that requires a domain name.

### Use cases

-  If you do not want to use any certificate, then there is no need to specify any secret-related information in the yaml.

-  In case of default certificate:

    For example, let us consider a secret `colddrink-secret` specified under `args` in the CIC yaml, then the secret is bound as non-SNI certificate.

```yaml
kind: ClusterRole

apiVersion: rbac.authorization.k8s.io/v1beta1

metadata:

name: cic-k8s-role

rules:

- apiGroups: [""]

resources: ["services", "endpoints", "ingresses", "pods", "secrets", "nodes"]

verbs: ["*"]



- apiGroups: ["extensions"]

resources: ["ingresses", "ingresses/status"]

verbs: ["*"]

---

kind: ClusterRoleBinding

apiVersion: rbac.authorization.k8s.io/v1beta1

metadata:

name: cic-k8s-role

roleRef:

apiGroup: rbac.authorization.k8s.io

kind: ClusterRole

name: cic-k8s-role

subjects:

- kind: ServiceAccount

name: cic-k8s-role

namespace: default

apiVersion: rbac.authorization.k8s.io/v1

---

apiVersion: v1

kind: ServiceAccount

metadata:

name: cic-k8s-role

namespace: default

---

apiVersion: v1

kind: Pod

metadata:

name: cic-k8s-ingress-controller

labels:

app: cic-k8s-ingress-controller

spec:

serviceAccountName: cic-k8s-role

containers:

- name: cic-k8s-ingress-controller

image: "quay.io/citrix/citrix-k8s-ingress-controller:latest"

env:

# Set Citrix ADC NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)

- name: "NS_IP"

value: "x.x.x.x"

# Set username for Nitro

- name: "NS_USER"

valueFrom:

secretKeyRef:

name: nslogin

key: username

# Set user password for Nitro

- name: "NS_PASSWORD"

valueFrom:

secretKeyRef:

name: nslogin

key: password

# Set log level

- name: "EULA"

value: "yes"

args:

- --ingress-classes

   citrix

- --default-ssl-certificate

   # <secret name>
   Colddrink-secret

- --feature-node-watch

false

imagePullPolicy: Always
```

You need to also add an empty secret in ingress file to enable default certificate for that service.

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: colddrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “colddrink’

spec:
  tls:
  - secretName:
  rules:
  - host:  items.colddrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-colddrinks
          servicePort: 443

```

`tls` section is required to ensure that the `frontend-colddrinks` service has the HTTPs traffic and need tls secret for encryption. Hence, secret provided as default under CIC is used for this service.

**Assumptions**:

-  There can be at most 1 default secret under `args` in CIC yaml that is considered as default certificate for all HTTPs traffic.

-  This default certificate is used globally for all services managed by this CIC yaml file.

-  Need to add empty secret name under TLS section to enable TLS feature for that service.

-  No TLS section is required with ingress if TLS feature not required.

All HTTPs request uses default certificate without matching the CN name of certificate used with secret.

**Secret in CIC ingress Yaml (SNI enabled)**:

The secret in ingress can be added in two ways:

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: colddrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “colddrink’

spec:
  tls:
  - secretName: colddrink.secret
    hosts:
    - items.colddrink.beverages
  rules:
  - host:  items.colddrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-colddrinks
          servicePort: 443

```

or

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: colddrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “colddrink’

spec:
  tls:
 - hosts:
   - items.colddrink.beverages
    secretName: colddrink.secret
  rules:
  - host:  items.colddrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-colddrinks
          servicePort: 443

```

**Assumptions**:

-  Secret given under TLS binds to Citrix ADC and performs strict name matching for the host name given under CN name of the certificate.

-  Certificate used for secret given under TLS section must have CN name otherwise it does not bind to Citrix ADC.

-  Default certificate if provided is binded along with the secret given under TLS section. Default certificate is used for the following HTTPs requests:

    -  `curl -1 -v -k https://1.1.1.1/`

    -  `curl -1 -v -k -H 'HOST:*.colddrink.beverages' https://1.1.1.1/`

    while, secret given under TLS section is used for request with full domain name.

    `curl -1 -v -k https://items.colddrink.beverages/`

    If any request received that does not match with certificates CN name fails.

    For example, `curl -1 -v -k https://items.hotdrink.beverages/`

-  **Multiple ingress**

**Secret in CIC ingress yaml (SNI enabled)**:

If multiple ingress files is used for different services, then all secrets will be used together to bind with context switch virtual server of Citrix ADC instance.

Example 1: `Hotdrink_Ingress.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: hotdrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “hotdrink’

spec:
  tls:
  - secretName: hotdrink.secret
    hosts:
    - items.hotdrink.beverages
  rules:
  - host:  items.hotdrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-hotdrinks
          servicePort: 443

```

`Colddrink_Ingress.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: colddrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “colddrink’

spec:
  tls:
 - hosts:
   - items.colddrink.beverages
    secretName: colddrink.secret
  rules:
  - host:  items.colddrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-colddrinks
          servicePort: 443

```

Example 2: The same secret used in 2 ingress file is handled internally and would not affect the behavior of other ingress, in case of addition or removal of either of ingress yaml.

`Hotdrink.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: hotdrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “hotdrink’

spec:
  tls:
  - secretName: hotdrink.secret
    hosts:
    - items.hotdrink.beverages

  rules:
  - host:  items.hotdrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-hotdrinks
          servicePort: 443

```

`Colddrink.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: colddrinks-ingress
  annotations:
   kubernetes.io/ingress.class: “colddrink’

spec:
  tls:
  - secretName: hotdrink.secret
    hosts:
    - items.hotdrink.beverages
  - secretName: colddrink.secret
    hosts:
    - items.colddrink.beverages

  rules:
  - host:  items.colddrink.beverages
    http:
      paths:
      - path: /
        backend:
          serviceName: frontend-colddrinks
          servicePort: 443

```