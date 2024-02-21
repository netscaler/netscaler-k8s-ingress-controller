# Rewrite and redirect Support

Citrix ingress controller supports header and URL modification via [rewrite policies CRD](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/crds/rewrite-responder.html). This section provides different examples for header and URL modification and contains the following sections:

-  [Before You Begin](#before-you-begin)
-  [Examples for HTTP header manipulation](#http-header-manipulation)
-  [Examples for URL manipulation](#url-manipulation)
-  [Examples for blocking requests](#blocking-requests)
-  [Miscellaneous Examples](#miscellaneous-examples)

## Before you begin

1.  Create a Kubernetes cluster.

    You need a Kubernetes cluster and the kubectl command-line tool to communicate with the cluster. If you do not have a cluster created before, follow the instructions in [Create Kubernetes cluster](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/) to create the Kubernetes cluster.

1.  Deploy an application.

    In this document, you refer to the `echo-server` application. See this document for steps to deploy [here](steps-to-deploy-echo-server).

1.  Deploy the Citrix ingress controller.

    If you are using NetScaler VPX or MPX, follow [this instruction to deploy Citrix Ingress Controller (CIC) to configure the same. If you do not have NetScaler VPX or MPX, you can use NetScaler CPX and follow [this](<link>) to deploy CIC and CPX.

1.  Apply the rewrite policy CRD definition.

         $ kubectl apply -f https://raw.githubusercontent.com/netscaler/netscaler-k8s-ingress-controller/master/crd/rewrite-policy/rewrite-responder-policies-deployment.yaml 

    **Note:**
    If Ingress controller is deployed via Helm, the setting `crds.install=true` installs all Citrix supported CRD definitions.

## HTTP header manipulation

A few examples are presented in this section that demonstrates how HTTP headers are manipulated before they are sent to the back end application.

### HTTP header insertion

Addition of headers to the request before it is sent to the back end application.

#### Addition of single header: X-Forwarded-For

In this example:

If `X-Forwarded-For` the HTTP Header does not exist in the client request, the header is inserted with `CLIENT.IP.SRC`.

If the `X-Forwarded-For` header exists in the client request, `CLIENT.IP.SRC` is appended to the list.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: httpxforwardedforadd
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: insert_http_header
        target: X-Forwarded-For
        modify-expression: client.ip.src
        comment: 'HTTP Initial X-Forwarded-For header add'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("X-Forwarded-For").EXISTS.NOT'

    - servicenames:
        - echoserver
      rewrite-policy:
        operation: replace
        target: HTTP.REQ.HEADER("X-Forwarded-For")
        modify-expression: 'HTTP.REQ.HEADER("X-Forwarded-For").APPEND(",").APPEND(CLIENT.IP.SRC)'
        comment: 'HTTP Append X-Forwarded-For IPs'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("X-Forwarded-For").EXISTS'
```

<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl http://demo.example.com

**Response:**

```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
X-Forwarded-For=<CLIENT-IP>
```

**Request:**  curl --header "X-Forwarded-For: 1.2.3.4"  http://demo.example.com

**Response:**

```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
X-Forwarded-For=1.2.3.4,<CLIENT-IP>
```

Note:
This rewrite CRD creates two rewrite policies on the NetScaler.
</details>

### Addition of multiple headers in a single policy: X-Forwarded-For & X-Fowarded-Host

In this example, `X-Forwarded-For` and `X-Forwarded-Host` HTTP Headers are inserted for all requests sent to the back-end microservice.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: multiheaderadd
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: insert_after
        target: http.req.full_header.before_str("\r\n\r\n")
        modify-expression: '"\r\nX-Forwarded-For: "+ CLIENT.IP.SRC +"\r\nX-Forwarded-Host: "+ HTTP.REQ.HOSTNAME +"\r\n"'
        comment: 'Adding X-Forwarded-For and X-Forwarded-Proto for all requests'
        direction: REQUEST
        rewrite-criteria: 'true'
```
<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl http://demo.example.com

**Response:**

```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Host=demo.example.com
User-Agent=curl/7.47.0
X-Forwarded-For=<CLIENT-IP>
X-Forwarded-Host=demo.example.com
```

More Information:
This rewrite CRD creates one rewrite policy on the NetScaler.
</details>

### Addition of multiple headers in separate policies:  X-Forwarded-For & X-Fowarded-Host

In this example:
`X-Forwarded-For` and `X-Forwarded-Host` HTTP Headers are inserted for all requests sent to the back end microservice, if not already added by the client.
As a default, NetScaler stops evaluating all other rewrite policies once a policy is hit. By setting the `goto-priority-expression: NEXT` in the CRD, you instruct the NetScaler to evaluate the next policy in the list.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: httpxforwardedforadd
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      goto-priority-expression: NEXT
      rewrite-policy:
        operation: insert_http_header
        target: X-Forwarded-For
        modify-expression: client.ip.src
        comment: 'X-Forwarded-For header add'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("X-Forwarded-For").EXISTS.NOT'
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: insert_http_header
        target: X-Forwarded-Host
        modify-expression: HTTP.REQ.HOSTNAME
        comment: 'X-Forwarded-Host header add'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("X-Forwarded-Host").EXISTS.NOT'
```

<details>
<summary>
Verifying this Policy
</summary>


**Request:** curl http://demo.example.com

**Response:**
```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Host=demo.example.com
User-Agent=curl/7.47.0
X-Forwarded-For=<CLIENT-IP>
X-Forwarded-Host=demo.example.com
```

**Request:** curl --header "X-Forwarded-For: 1.2.3.4"  http://demo.example.com 

**Response:**

```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
X-Forwarded-For=1.2.3.4      <--------- Sent by Client
X-Forwarded-Host=demo.example.com   <--------- Inserted by Netscaler
```

**More Info:**
This rewrite CRD creates two rewrite policies on the NetScaler. The first rewrite policy has the `GotoPriority Expression: NEXT` set.

</details>

## HTTP Header rewrites

In this example,
`dummy-header` HTTP Header value sent from the client is replaced with the `"replaced-value"` before sending the request to the back end microservice.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: httpxforwardedforadd
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: replace
        target: HTTP.REQ.HEADER("dummy-header")
        modify-expression: '"replaced-value"'
        comment: "Replace dummy-header value"
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("dummy-header").EXISTS'
```
<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl --header "dummy-header: dummy"  http://demo.example.com

**Response:**

```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
dummy-header=replaced-value
```

**More Info:**
This rewrite CRD creates one rewrite policy on the NetScaler appliance.
</details>

## HTTP header removal

In this example, `dummy-header` header sent from the client is removed before sending the request to the back end microservice.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: removeheader
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: delete_http_header
        target: "dummy-header"
        comment: "Delete dummy-header inserted by Client"
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.HEADER("dummy-header").EXISTS'
```

<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl --header "dummy-header: dummy"  http://demo.example.com

**Response:**
```
CLIENT VALUES:
command=GET
path=/
real path=/
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
```

**More Info:**
This rewrite CRD creates one rewrite policy on the NetScaler.
</details>

## URL manipulation

A few examples are presented in this section that demonstrates how URLs are manipulated before they are sent to the back end application.

### Rewrite a single URL

In this example, the user‑friendly URL `http://mysite.com/listings/123` is rewritten to a URL handled by the microservice, `http://mysite.com/listing.html?listing=123`.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: customurlrerouting
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: replace
        target: 'http.req.url'
        modify-expression: '"/listing.html?listing=" + http.req.url.after_str("/listings/")'
        comment: 'Changing the url for custom re-routing cases'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.URL.STARTSWITH("/listings/")'
```
<details>
<summary>
Verifying this Policy
</summary>


**Request:** curl http://demo.example.com/listings/123 

**Response:**
```
CLIENT VALUES:
client_address=('10.106.170.68', 14780) (10.106.170.68)
command=GET
path=/listing.html?listing=123
real path=/listing.html
query=listing=123
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
```

**Note:**
This rewrite CRD creates one rewrite policy on the NetScaler. 
</details>

### Rewrite a pattern set of URLs

In this example, if the first subdirectory of the URL path belongs to a pattern set, `/new-apps` is inserted before it.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: urlpatsetrewrite
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: insert_before
        target:  "http.REQ.URL.PATH.GET(1)"
        modify-expression: '"new-apps/"'
        comment: 'If the first subdirectory of URLS belongs to a patset its rewritten'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.URL.PATH.GET(1).EQUALS_ANY("newapps")'
  patset:
    - name: newapps
      values:
        - 'app1'
        - 'app2'
```
<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl http://demo.example.com/app2

**Response:**
```
CLIENT VALUES:
command=GET
path=/new-apps/app2
real path=/new-apps/app2
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
```

**Note:**
This rewrite CRD creates one rewrite policy on the NetScaler.
</details>

### Rewrite multiple URLs in a single policy using string map

In this example, If the URL path matches the key of a string map, it is rewritten with the corresponding value.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: customurlrerouting
spec:
  ingressclass: netscaler-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: replace
        target: http.req.url
        modify-expression: HTTP.REQ.URL.PATH.MAP_STRING("urlrewritemapping")
        comment: 'If URLS belong to a key of a stringmap its rewritten with its corresponding value'
        direction: REQUEST
        rewrite-criteria: HTTP.REQ.URL.PATH.IS_STRINGMAP_KEY("urlrewritemapping")
  stringmap:
    - name: urlrewritemapping
      comment: Urls to be modified string
      values:
      - key: /app1
        value: /dev/app1
      - key: /app2
        value: /prod/app2     
```
<details>
<summary>
Verifying this Policy
</summary>


**Request-1:** curl http://demo.example.com/app1
**Response-1:**
```
CLIENT VALUES:
command=GET
path=/dev/app1
real path=/dev/app1
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
```

**Request-2:** curl http://demo.example.com/app2
**Response-2:**
```
CLIENT VALUES:
client_address=('10.106.170.68', 12565) (10.106.170.68)
command=GET
path=/prod/app2
real path=/prod/app2
query=
request_version=HTTP/1.1

SERVER VALUES:
server_version=BaseHTTP/0.6
sys_version=Python/3.5.0
protocol_version=HTTP/1.0

HEADERS RECEIVED:
Accept=*/*
Connection=Keep-Alive
Host=demo.example.com
User-Agent=curl/7.47.0
```

**More Info:**
This rewrite CRD creates one rewrite policy on the NetScaler. 
</details>

## Blocking requests

A few examples are presented in this section that demonstrates how certain client requests are allowed or denied access to the application.

### URL blocking

In this example, access to certain URLs provided via a pattern set is denied access.
 
```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklisturl
spec:
  ingressclass: cic-vpx
  responder-policies:
    - servicenames:
        - echoserver
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 401 Access denied"'
        respond-criteria: HTTP.REQ.URL.ENDSWITH_ANY("blocklisturl")
        comment: 'Blocklist certain Urls'
  patset:
    - name: blocklisturl
      values:
        - '/admin'
        - '/secret'
```

## IP address blocking

In this example, client IP addresses belonging to a certain CIDR is denied access.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklistips1
spec:
  ingressclass: netscaler-vpx
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: 'client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Blocklist certain IPs'
```

## File access blocking

In this example, access to extension like aspx, php, cgi, jsp is forbidden.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: filetyperejection
spec:
  ingressclass: netscaler-vpx
  responder-policies:
    - servicenames:
        - echoserver
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Access to file " + HTTP.REQ.URL.HTTP_URL_SAFE + " is Forbidden"'
        respond-criteria: 'HTTP.REQ.URL.ENDSWITH(".aspx").OR(HTTP.REQ.URL.ENDSWITH(".php")).OR(HTTP.REQ.URL.ENDSWITH(".cgi")).OR(HTTP.REQ.URL.ENDSWITH(".jsp"))'
        comment: 'File Type belongs to aspx,php,cgi,jsp are Forbidden'
```
<details>
<summary>
Verifying this Policy
</summary>

**Request:** curl http://demo.example.com/file.jsp -w "\n" -v

**Response:**
```
> GET /file.jsp HTTP/1.1
> Host: demo.example.com
> User-Agent: curl/7.47.0
> Accept: */*
>
< HTTP/1.1 403 Forbidden
* no chunk, no close, no size. Assume close to signal end
<
* Closing connection 0
Access to file /file.jsp is Forbidden
```

**Note:**
This rewrite CRD creates one responder policy on the NetScaler.
</details>

## Miscellaneous examples

### Adding proxy protocol headers

In this example, proxy protocol headers are inserted before sending the request to the back end microservice.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: httpxforwardedforadd
spec:
  ingressclass: cic-vpx
  rewrite-policies:
    - servicenames:
        - echoserver
      rewrite-policy:
        operation: insert_before
        target: http.req.full_header
        modify-expression: '"PROXY TCP4 " + CLIENT.IP.SRC + " " + CLIENT.IP.DST + " " + CLIENT.TCP.SRCPORT + " " + CLIENT.TCP.DSTPORT + "\r\n"'
        comment: 'Request header rewrite for HTTPvs'
        direction: REQUEST
        rewrite-criteria: 'HTTP.REQ.IS_VALID'
```

### Redirect to a new host name

In this example, requests are redirected from the old domain name to the home page of the new domain.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: redirectnewhost
spec:
  ingressclass: netscaler-vpx
  responder-policies:
  - servicenames:
      - echoserver
    responder-policy:
       redirect:
         url: '"new-domain-name.com"'
         redirect-status-code: 301
       respond-criteria: 'HTTP.REQ.HOSTNAME.CONTAINS("demo.example.com")'
       comment: 'Redirect to New Domain Name'
```

**Note:** If the URL has to be mapped with the new-domain-name, the only change on the URL attribute is as follows:

    url: '"new-domain-name.com" + http.req.url'

## Forcing all requests to use SSL or HTTPS

In this example, all requests are forced to use a secured (SSL/HTTPS) connection to your site.

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: httpxforwardedforadd
spec:
  ingressclass: netscaler-vpx
  responder-policies:
  - servicenames:
        - echoserver
    responder-policy:
       redirect:
          url: '"https://" +http.req.HOSTNAME.SERVER+":"+"443"+http.req.url'
       respond-criteria: 'http.req.is_valid'
       comment: 'http to https'
```