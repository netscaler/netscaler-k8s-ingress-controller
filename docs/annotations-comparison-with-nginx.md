#  Comparison between Citrix ingress controller and NGINX ingress controller annotations

This topic provides a comparison between the various annotations provided by the Citrix ingress controller and NGINX ingress controller.

**Note:** This is not a comprehensive list of all Citrix annotations, but more of a comparison between annotations provided by Citrix and NGINX which offers similar functionalities. 

## SSL, TLS

The following table shows some of the NGINX and Citrix ingress controller annotations related to SSL and TLS. 


| NGINX annotation | Description | Citrix annotation |Description| Citrix documentation URL |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- |
| `nginx.org/redirect-to-https` |Server-side HTTPS enforcement through redirect for specific ingress resources based on the `http_x_forwarded_proto header`. |ingress.citrix.com/insecure-termination|Allow or deny HTTP traffic or redirect to HTTPs | [Annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/)|
| `nginx.ingress.kubernetes.io/ssl-redirect` |Sets an unconditional redirect rule for all incoming HTTP traffic to force incoming traffic over HTTPS. |ingress.citrix.com/insecure-termination|Allow or deny HTTP traffic or redirect to HTTPs | [Annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/)|
| `nginx.ingress.kubernetes.io/ssl-passthrough` | Enables SSL passthrough | ingress.citrix.com/ssl-passthrough | Enable SSL passthrough on the Ingress Citrix ADC | [SSL passthrough](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/certificate-management/ssl-passthrough/)|


In addition to the annotations specified in the table, Citrix also provides the following annotations related to SSL, TLS.

| Citrix Annotation   | Description |
| ------------------- | -------- |
| `ingress.citrix.com/secure-service-type` |Allows L4 load balancing for SSL over TCP. |
| `ingress.citrix.com/secure-port`    | Use this annotation to configure the port for HTTPS traffic. |
| `ingress.citrix.com/preconfigured-certkey`     | Enables using the certificates that are already configured on the Citrix ADC.  |
| `ingress.citrix.com/ca-secret` |Attaches the generated CA secret which is used for client certificate authentication for a service. |
| `ingress.citrix.com/secure-backend`    | Enables secure back end communication to a service.  |
| `ingress.citrix.com/backend-secret`     | Binds the certificate to SSL service.  This certificate is used when the Citrix ADC acts as a client to send the request to the back end server.  |
| `ingress.citrix.com/backend-ca-secret`     |Binds the CA certificate of the server to the SSL service on the Citrix ADC.  |


## Custom Parameters

Custom parameters and some of the SSL features like HTTP Strict Transport Security (HSTS) which are configured using annotations in NGINX are configured using profiles (HTTP, TCP, SSL) in Citrix ADC.

Citrix provides the following annotations for configuring SSL, HTTP, and TCP profiles respectively:

|Citrix annotations for profiles   |Some of the parameters you can configure| Citrix documentation URL|
| ------------------- | -------- |-----------|
| SSL profiles: </br>`ingress.citrix.com/frontend-sslprofile` <br>`ingress.citrix.com/backend-sslprofile`| HSTS, Server Name Indication (SNI)| For detailed information, see [SSL profiles](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/profiles/#ssl-profile). |
|HTTP profiles: </br>`ingress.citrix.com/frontend-httpprofile` <br>`ingress.citrix.com/backend-httpprofile`   |HTTP2, HTTP session timeouts (reqTimeout and reqTimeoutAction, adptTimeout, reusePoolTimeout). |For detailed information on HTTP profile configuration parameters, see the [HTTP use cases documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/http-use-cases/).|
|TCP profiles: </br>`ingress.citrix.com/frontend-tcpprofile` <br>`ingress.citrix.com/backend-tcpprofile`    | Idle TCP connection drop, TCP delayed acknowledgment, client side MPTCP session management, and TCP optimization (includes selective acknowledgment, forward acknowledgment, window scaling (WS), maximum segment size, bufferSize, and so on)|For detailed information on all the TCP parameters, see the [TCP use cases documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/tcp-use-cases/). |

## Back-end services

The following table shows some of the NGINX and Citrix ingress controller annotations for the back-end services:

 NGINX annotation | Description | Citrix annotation |Description| Citrix documentation URL |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- |
| `nginx.org/lb-method` |Sets the load balancing method. |`ingress.citrix.com/lbvserver`| Sets the load balancing algorithm, cookie persistence and so on.| [Annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/)|
|`nginx.com/health-checks` | Enables health checks. |`ingress.citrix.com/monitor`|Sets the monitoring type (health check in NGINX terms). | [Annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/)|


Apart from these annotations, Citrix also provides the following annotation for back end services:

| Citrix Annotation   | Description |
| ------------------- | -------- |
| `ingress.citrix.com/servicegroup` | Enables configuring Citrix ADC service group options. |

## Traffic distribution

The following table shows some of the NGINX and Citrix ingress controller annotations for Canary deployments:

| NGINX annotation | Description | Citrix annotation |Description| Citrix documentation URL |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- |
| `nginx.ingress.kubernetes.io/canary-by-header` |Specifies the header to use for notifying the Ingress to route the request to the service specified in the Canary Ingress. |`ingress.citrix.com/canary-by-header`|Applies the canary rules based on the HTTP request header. | [Simplified canary deployment](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/canary/canary/#simplified-canary-deployment-using-ingress-annotations)|
| `nginx.ingress.kubernetes.io/canary-weight` |Specifies the percentage of traffic to be directed to the canary version of the application. |`ingress.citrix.com/canary-weight`| Specifies the percentage of traffic to be directed to the canary version and the production version of an application. |[Simplified canary deployment](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/canary/canary/#simplified-canary-deployment-using-ingress-annotations) |
| `nginx.ingress.kubernetes.io/canary-by-header-value` | Specifies the header value to match for notifying the Ingress to route the request to the service specified in the Canary Ingress.|`ingress.citrix.com/canary-by-header-value`  |Applies the canary rules based on the HTTP request header value.  | [Simplified canary deployment](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/canary/canary/#simplified-canary-deployment-using-ingress-annotations)|


## Citrix CRDs

Some of the features configured using annotations for NGINX are configured using CRDS on Citrix ADC.

The following table shows some of the NGINX annotations and information on CRDs from Citrix which offers the same functionality. 

| NGINX annotation | Description |  Citrix CRDs |Description| Citrix documentation URL |
| --------------------- | ---------- | --------------------------- | ------------------------- | --------------- |
| `nginx.ingress.kubernetes.io/rewrite-target` |Redirect HTTP requests to a Target URI. |Rewrite and Responder CRD|Redirecting HTTP traffic to a specific URL|[Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/)|
| `nginx.ingress.kubernetes.io/limit-rps` or `nginx.ingress.kubernetes.io/limit-rpm`|Rate limit number of requests accepted from a given IP per each second or minute. |Rate limit CRD| Rate limit requests to the resources on the back-end server or services | [Rate limit CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rate-limit/)|
| `nginx.ingress.kubernetes.io/whitelist-source-range` |Specifies allowed client IP source ranges. | Rewrite and Responder CRD |Creates a list of trusted IP addresses or IP address ranges from which users can access your domains. | [Allowlisting or blocklisting IP addresses](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/ip-whitelist-blacklist/)|

