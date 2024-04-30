# Rewrite and Redirect Support

`Citrix Ingress Controller` supports header and URL modification via [rewritepolicies CRD](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/crds/rewrite-responder.html). 

## Table of Contents
1. [Before You Begin](#before-you-begin)
2. [Examples for HTTP Header Manipulation](#http-header-manipulation)
3. [Examples for URL Manipulation](#url-manipulation)
4. [Examples for Blocking Requests](#blocking-requests)
5. [Miscellaneous Examples](#miscellaneous-examples)

# 1 Before You Begin

1. **Create a Cluster**

    You need a Kubernetes cluster and kubectl command-line tool to communicate with the cluster.
2. **Deploy an Application**

    In this document we are referring to `echo-server` application (image: gcr.io/google_containers/echoserver:1.0)
3. **Deploy the Citrix Ingress Controller**

    If you are using NetScaler VPX or MPX, please follow [UNIFIED ingress controller](<link>) instructions to deploy Citrix Ingress Controller (CIC) to configure the same. If you do not have NetScaler VPX or MPX, you can use NetScaler CPX and follow [Dual Tier Ingress Controllder](<link>) to deploy CIC and CPX.
    > Note:
    Setting crds.install=true will install all citrix supported CRD Definitons.         

# 2 HTTP Header Manipulation

A few examples are presented in this section that demonstrate how HTTP headers are manipulated before they are sent to the backend application.

## 2.1 HTTP Header Insertion 

Addition of headers to the request before it is sent to the backend application.

### 2.1.1 Addition of Single header: X-Forwarded-For

In this example,

If `X-Forwarded-For` HTTP Header doesn't exist in the client request, the header is inserted with `CLIENT.IP.SRC`.

If `X-Forwarded-For` header already exists in the client request, `CLIENT.IP.SRC` is appended to the list. 

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
More Info: 
This rewrite CRD will create two rewrite policies on the Netscaler. 
</details>



### 2.1.2 Addition of Multiple Headers in a single policy: X-Forwarded-For & X-Fowarded-Host

In this example,
`X-Forwarded-For` and `X-Forwarded-Host` HTTP Headers are inserted for all request sent to the backend microservice.

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

More Info: 
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>



### 2.1.3 Addition of Multiple Headers in separate policies:  X-Forwarded-For & X-Fowarded-Host

In this example,
`X-Forwarded-For` and `X-Forwarded-Host` HTTP Headers are inserted for all requests sent to the backend microservice, if not already added by the client.
> As a default, Netscaler stops evaluating all other rewrite policies once a policy is hit. By setting the `goto-priority-expression: NEXT` in the CRD, we instruct the Netscaler to evaluate the next policy in the list.

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
This rewrite CRD will create two rewrite policies on the Netscaler. The first rewrite policy will have the `GotoPriority Expression: NEXT` set.

</details>


## 2.2 HTTP Header rewrite

In this example,
`dummy-header` HTTP Header value sent from the Client is replaced with `"replaced-value"` before sending the request to the backend microservice.

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
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>

## 2.3 HTTP Header removal 

In this example,
`dummy-header` Header sent from the Client is removed before sending the request to the backend microservice.

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
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>

 
# 3 URL Manipulation 

A few examples are presented in this section that demonstrate how URLs are manipulated before they are sent to the backend application.

### 3.1 Rewrite a single URL

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

**More Info:**
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>

### 3.2 Rewrite a patset of URLs.

In this example, if first subdirectory of the URL Path belongs to a patset, `/new-apps` is inserted before it.

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

**More Info:**
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>


### 3.3 Rewrite mulitple URLs in a single policy using stringmap

In this example, If the URL Path matches the Key of a stringmap, it is rewritten with the corresponding value.

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
This rewrite CRD will create one rewrite policies on the Netscaler. 
</details>

# 4 Blocking Requests

A few examples are presented in this section that demonstrate how certain client requests are allowed/denied access to the application. 

## 4.1 URL Blocking

In this example, access to certain URLs provided via a patset is denied access.
 
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
## 4.2 IP Blocking

In this example, Client IPs belonging to a certain CIDR is denied access.

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
## 4.3 File access Blocking 

In this example, access to file extension like aspx, php, cgi, jsp is forbidden.

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

**More Info:**
This rewrite CRD will create one responder policies on the Netscaler. 
</details>

# 5 Miscellaneous Examples

## 5.1 Adding Proxy Protocol Headers

In this example, Proxy Protocol header are inserted before sending the request to the backend microservice.

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

## 5.2 Redirect to a new Hostname

In this example, requests are redirected from the old domain name to the homepage of the new domain.

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

> If the url has to be mapped with the new-domain-name, the only change on the url attribute will be as follows:
  url: '"new-domain-name.com" + http.req.url'

## 5.3 Forcing all Requests to Use SSL/HTTPS

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


