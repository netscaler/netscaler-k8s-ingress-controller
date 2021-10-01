# HTTPRoute

HTTPRoute is a custom resource which defines the routing decision for content switching.
Currently HTTPRoute supports routing based on the following:

- Host name based routing
- Path based routing
- HTTP header Name based routing
- HTTP header name and value based routing
- Cookie based routing
- Query parameter based routing
- HTTP method based routing
- Routing using Citrix ADC policy expressions

You can define one or more rules as part of an HTTPRoute object with each rule acts as a matching criteria for routing. An action is defined for each rule when the matching criteria is met for the incoming HTTP request. An action could be one of 'backend' in which the traffic is load balanced to the backend service or 'redirect' where the redirect response is sent back to the client. 'Backend' action creates Content switching policies in ADC and 'redirect' action creates responder policies in ADC.

There are three different ways of matching criteria as explained in the following table:

| Matching criteria | Description                                                     |
|-------------------|-----------------------------------------------------------------|
| `exact`           | Exactly matches the incoming request. This criteria is case insensitive.          |
| `prefix`          | Matches prefix of the incoming request. For example: `/a` matches to `/a/b` and `/a/c`.         |
| `contains`         | Matches if the incoming request contains the specified keyword. |

This topic contains a sample HTTPRoute CRD object and also explains the various attributes of the HTTPRoute CRD. For the complete CRD definition, see [HTTPRoute.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/contentrouting/HTTPRoute.yaml).

## HTTP CRD object example

The following is a sample HTTP CRD object.

```yml
apiVersion: citrix.com/v1
kind: HTTPRoute
metadata:
  name: test-route
  labels:
    domain: abc.com
spec:
  hostname:
  - abc.com
  rules:
  - name: exactpath
    match:
    - path:
        exact: /resources
    action:
      backend:
        kube:
          service: resource
          port: 80
  - name: prefixpath
    match:
    - path:
        prefix: /cart
    action:
      backend:
        kube:
          service: cart
          port: 80
  - name: header
    match:
    - headers:
      - headerName:
          contains: Mobile
    action:
      backend:
        kube:
          service: mobile
          port: 443
          backendConfig:
            secureBackend: true
            lbConfig:
              lbmethod: ROUNDROBIN
```

For more examples, see [HTTP Route Examples](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/contentrouting/HTTPRoute_examples).

## HTTPRoute.spec

HTTPRoute custom resource defines a spec field which represents the HTTP routing specification which has a list of rules with an action for each rule defined.

 The following table explains the various fields in the `HTTPRoute.spec` attribute.

| Field         | Description                                                                                                            |     Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | Required |
|---------------|---------------------------------------------------------------------------------|---------------------------------------------------|---------------|
| `hostname`      | Specifies the list of host names of the server. The host name must be a valid subdomain as defined in RFC 1123, such as test.example.com. A wildcard host name in the form of `*.example.com` is also valid. In that case, any subdomain of `example.com` is considered for the matching. The default value is `*` which means to match all incoming HTTP requests.                      | string          | Yes      |
| `rules`         |Specifies the list of rules with a matching routing criteria associated with an action.  | [ ]  [rules](#HTTPRouterules)       | No       |

## HTTPRoute.rules

 The following table explains the various fields in the `HTTPRoute.rules` attribute.

| Field  | Description                                                                                                                                              |Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                                                                                     | Required |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------| --------------------------------------------------------------------------------------------| --------------|
| `name`  | Specifies a name to represent the rule. This field is used as an identifier in the content routing policy name in Citrix ADC.  <Br>**Note:** For each rule, the name must be unique.                  | string          | Yes      |
| `action` |Specifies an action for the matching rule.                   | rules.action    | Yes      |
| `match`  | List of matching routes with the same action. If more than one entry is present, this matching rule treated as an `OR` condition and the same action is chosen for any match. | [ ] [rules.match](#HTTPRouterulesmatch)  | No       |

## HTTPRoute.rules.match

 The following table explains the various fields in the `HTTPRoute.rules.match` attribute.

| Field            | Description                                                                                                                                    | Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                                  | Required |
|------------------|--------------------------------------------------------------------------------|   ----------------------------------------------------|----------|
| `path`             |Specifies URL path based routing rules.                                                                                                                   | [HTTPRoute.rules.match.path](#HTTPRouterulesmatchpath)          | No       |
| `headers`          |Specifies the list of header based matches for content routing. If there is more than one rule, this matching criteria is treated as an `AND` condition and all rules must match.                   | [ ] [HTTPRoute.rules.match.headers](#HTTPRouterulesmatchheaders)   | No       |
| `cookies`          |Specifies the list of cookie based matches for content routing. If there is more than one rule, this matching criteria is treated as an `AND` condition and all rules must match.                    | [ ] [HTTPRoute.rules.match.cookies](#HTTPRouterulesmatchcookies)     | No       |
| `queryParams`      |Specifies the list of query parameters for content routing. If there is more than one rule, this matching criteria is treated as an `AND` condition and all rules must match.                    | [ ] [HTTPRoute.rules.match.queryParams](#HTTPRouterulesmatchqueryParams) | No       |
| `method`           |Specifies HTTP method based routing rules. Possible options are: GET, POST, PUT, and so on. An action is chosen for the HTTP request with the matching method. | string                               | No       |
| `policyExpression` |Specifies Citrix ADC policy expression based routing rules. Any custom Citrix ADC policy expression can be specified for content routing rules. The Citrix ingress controller does not check the correctness of the expression. Hence, you must check the correctness of the expression. For more information on policy expression, see [Expression Prefix](https://docs.citrix.com/en-us/netscaler/media/expression-prefix.pdf). For example: `HTTP.REQ.URL.PATH.GET(1).EQ("foo")`      | string                               | No       |

## HTTPRoute.rules.match.path

This attribute specifies the path based matching for content routing.

Following is an example for the `HTTPRoute.rules.match.path` attribute.
```yml
     match:
     - path:
         prefix: /resources
     action:
       backend:
         kube:
           service: resource
           port: 80
---
     match:
     - path:
         regex: '/foo/[A-Z0-9]{3}'
     action:
       backend:
         kube:
           service: resource
           port: 80
```

The following table explains the various fields in the `HTTPRoute.rules.match.path` attribute.

| Field  | Description                                                                                                                                                 | Type   | Required |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|
| `prefix` | Specifies the prefix expression of paths as a matching criteria. If the beginning path of an HTTP request matches the specified path, perform a match. For example, `/a` matches URLs `/a` and `/a/b`.                                            | string | No       |
| `exact`  | Specifies the exact path as a matching criteria. Performs a match only if the request path exactly matches the specified path.                                                           | string | No       |
| `regex`  | Specifies regular expressions as a matching criteria for paths. Performs a match if the specified regular expression matches with the incoming request. Only regular expressions in the Perl Compatible Regular Expression (PCRE) format are supported. For more information on regular expressions supported by Citrix ADC, see [Regular Expressions](https://docs.citrix.com/en-us/netscaler/12/appexpert/policies-and-expressions/ns-regex-wrapper-con.html).                                                       | string | No       |

## HTTPRoute.rules.match.headers

This attribute represents the header based matching for content routing.

The following table explains the various fields in the `HTTPRoute.rules.match.headers` attribute.

| Field       | Description                                                                                                                           | Type                                      | Required |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|----------|
| `headerName`  | Specifies the header name as a matching criteria for content routing. If the header exists, it is used for matching. In this case, header value is not considered for matching.         | [HTTPRoute.rules.match.headers.headerName](#HTTPRouterulesmatchheadersheaderName)  | No       |
| `headerValue` | Specifies the header name and value as the matching criteria for content routing. For name, exact name is the matching criteria and matching criteria for value can be specified as `exact`, `regex`, or `contains` expression. | [HTTPRoute.rules.match.headers.headerValue](#HTTPRouterulesmatchheadersheaderValue) | No       |

## HTTPRoute.rules.match.headers.headerName

This attribute represents the header name based matching for content routing.

Following example shows sample snippets for the `HTTPRoute.rules.match.headers.headerName` attribute configuration.

```yml
    match:
    - headers:
      - headerName:
        exact: mobile
    action:
      backend:
        kube:
          service: mobile-service
          port: 80
---
    match:
    - headers:
       - headerName:
         regex: "Header-[a-z]{1}"
    action:
      backend:
        kube:
          service: resource-service
          port: 80
```

The following table explains the various fields in the `HTTPRoute.rules.match.headers.headerName` attribute.

| Field    | Description                                                                                               | Type    | Required |
|----------|-----------------------------------------------------------------------------------------------------------|---------|----------|
| `exact`    | Specifies the exact header name as matching criteria for routing.                                                                | string  | No       |
| `contains` | Specifies the string that is designated in the `contains` string as a matching criteria for the header name.                  | string  | No       |
| `regex`    | Specifies the regular expression as a matching criteria. Performs a match if the header name matches the specified regular expression. Only regular expressions in the PCRE format are supported.  | string  | No       |
| `not`      | The default value for this attribute is false. If this value is true, the header name must not exist in the incoming request.                              | boolean | No       |

## HTTPRoute.rules.match.headers.headerValue

This attribute represents the header name and value matching for content routing. The header name is matched exactly and value is matched according to the fields specified.

The following example shows sample snippets for the `HTTPRoute.rules.match.headers.headerValue` attribute configuration.
```yml

     match:
     - headers:
       - headerValue:
           name: Origin
           exact: mobile
           not: true
     action:
       backend:
         kube:
           service: mobile
           port: 80
---
     match:
     - headers:
       - headerValue:
           name: Origin
           prefix: header1
     action:
       backend:
         kube:
           service: service1
           port: 80
---
     match:
     - headers:
       - headerValue:
           name: Origin
           regex: "[a-z]{1}"
     action:
       backend:
         kube:
           service: example
           port: 80
```

The following table explains the various fields in the `HTTPRoute.rules.match.headers.headerValue` attribute.


| Field    | Description                                                                                                                                                                                                   | Type    | Required |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------|
| `name`     | Specifies the name of the header that must match a value. The `exact`, `contains`, and `regex` fields are used for matching the header value. If none of the `exact`, `contains`, and `regex` field is present, any value for the name is matched. | string  | Yes      |
| `exact`    | Matches if the value of the HTTP header with the name field matches exactly.| string  | No       |
| `contains` | Matches if the value of the HTTP header with the name field contains the designated string. | string  | No       |
| `regex`    | Matches if the value of the HTTP header with the name field matches the regular expression. Only regular expressions in the PCRE format are supported.                                                                    | string  | No       |
| `not`      | The default value for this attribute is false. If this value is true, the header name must not match the value. | boolean | No       |

## HTTPRoute.rules.match.cookies

This attribute represents the cookie based matching for content routing. The cookie header in the HTTP request is used for matching. A cookie with a name field is matched against a value if the value is present. If a value is not specified, it is matched for any value.

The following example shows sample snippets for the `HTTPRoute.rules.match.cookies` attribute configuration.

```yml
     match:
     - cookies:
       - name: version
         contains: v1
     action:
       backend:
         kube:
           service: v1-app
           port: 80
---
     match:
     - cookies:
       - name: version
         exact: v1
     action:
       backend:
         kube:
           service: v1-app
           port: 80
---
     match:
     - cookies:
       - name: version
         regex: '[a-z]{1}'
     action:
       backend:
         kube:
           service: v1-app
           port: 80
```

The following table explains the various fields in the `HTTPRoute.rules.match.cookies` attribute.

| Field    | Description                                                                                                                                                            | Type    | Required |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------|
| `name`     | Specifies the name of the cookie whose value is used for matching. If none of the matching criteria like `exact`, `regex` and `contains` is present for the cookie name, any value for the cookie name is matched if the name is present. | string  | Yes      |
| `exact`    | Matches if the value of the cookie with name field matches exactly.                                                                                                      | string  | No       |
| `contains` | Matches if the value of the cookie with name field contains the string specified.                                                                                   | string  | No       |
| `regex`    | Matches if the value of the cookie with name field matches the regular expression. Only regular expressions in the PCRE format are supported.                                     | string  | No       |
| `not`      |The default value for this attribute is false. If this value is true, the cookie with name must exist, but must not match the value.                                                             | boolean | No       |

## HTTPRoute.rules.match.queryParams

This attribute represents the HTTP query parameters in the URL matching for content routing.
```yml

    match:
     - queryParams:
       - name: version
         contains: v1
    action:
      backend:
        kube:
          service: v1-app
          port: 80
---
    match:
    - queryParams:
      - name: version
        regex: '[a-z]{1}'
    action:
      backend:
        kube:
          service: v1-app
          port: 80
---
     match:
     - queryParams:
      - name: version
        exact: v1
        not: true
     action:
       backend:
        kube:
          service: mobile
          port: 80
```

The following example shows sample snippets for the `HTTPRoute.rules.match.cookies` attribute configuration.

| Field    | Description                                                                                                                                                                             | Type    | Required |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------|
| `name`     | Specifies the name of the query parameter whose value is matched against. If none of the criteria like `exact`, `regex` and `contains` is present, any value for the query parameters name is matched if the name is present. | string  | Yes      |
| `exact`    | Matches if the value of the query parameter with the name field matches exactly.                                                                                                          | string  | No       |
| `contains` | Matches if the value of the query parameter with the name field contains the string specified.                                                                                       | string  | No       |
| `regex`    | Matches if the value of the query parameter with the name field matches the regular expression. Only PCRE format regular expression is supported                                          | string  | No       |
| `not`      | The default value for this attribute is false. If this value is true, the query parameter with name must exist, but must not match the value.                                                               | boolean | No |

## HTTPRoute.rules.action

This attribute represents the action for matching rules.

The following table explains the various fields in the `HTTPRoute.rules.action` attribute.

| Field    | Description                                                                          | Type            | Required |
|----------|--------------------------------------------------------------------------------------|-----------------|----------|
| `backend`  | The default action for this field is to send the traffic to a back-end service. Either the back end or the redirect is required. | [rules.action.backend](#HTTPRouterulesactionbackend)| No|
| `redirect` | The default action is to redirect the traffic. Either the back end or redirect is required.      | [rules.action.redirect](#HTTPRouterulesactionredirect) | No    |


## HTTPRoute.rules.action.backend

This attribute represents routing the traffic to back-end service.
The following table explains the various fields in the `HTTPRoute.rules.action.backend` attribute.

| Field | Description                                            | Type                | Required |
|-------|--------------------------------------------------------|---------------------|----------|
| `kube`  | Specifies the Kubernetes service information for the back end service. | [action.backend.kube](#Listeneractionbackendkube) |          |

## HTTPRoute.rules.action.backend.kube

This attribute represents the Kubernetes service for the default back end. Service must belong to the same namespace as HTTPRoute resource. If the service is of type `NodePort` or `Loadbalancer`, the list of node IP addresses and NodePort of those nodes with pods is used as back-end service in 7.

Following is an example for the `HTTPRoute.rules.action.backend.kube` attribute.

        kube:
          service: service
          namespace: default
          port: 80
          backendConfig:
            lbConfig:
              lbmethod: ROUNDROBIN
            servicegroupConfig:
              clttimeout: '20'

The following table explains the various fields in the `HTTPRoute.rules.action.backend.kube` attribute.

| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `service `      | Specifies the name of the Kubernetes service for the default back end.      | string        | Yes      |
| `port`          | Specifies the port number of the Kubernetes service for the default back end.      | integer       | Yes      |
| `backendConfig` | Specifies the back-end configurations for the default back end.          | [BackendConfig](#BackendConfig) | No       |

## BackendConfig

This attribute represents the back end configurations of Citrix ADC.
Following is an example for the `BackendConfig` attribute configuration.


    backendConfig:
     sercureBackend: true
     lbConfig:
       lbmethod: ROUNDROBIN
     servicegroupConfig:
       clttimeout: '20'


The following table explains the various fields in the `BackendConfig` attribute.

| Field              | Description                                                                                                                                                                             | Type   | Required |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|
| `secureBackend`      | Specifies whether the communication is secure or not. If the value of `secureBackend` field is  `true` secure communication is used to communicate with the back end. The default value is `false`, that means HTTP is used for the back end communication.                                            |        |          |
| `lbConfig`          | Specifies the Citrix ADC load balancing virtual server configurations for the given back end. One can specify key-value pairs as shown in the example which sets the LBVserver configurations for the back end. For all the valid configurations, see [LB virtual server configurations](https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/load-balancing/lbvserver/lbvserver/).             | object | No       |
| `servicegroupConfig` | Specifies the Citrix ADC service group configurations for the given back end. One can specify the key-value pairs as shown in the example which sets the service group configurations for the back end. For all the valid configurations, see [service group configurations](https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/basic/servicegroup/servicegroup/).| object | No       |

## HTTPRoute.rules.action.redirect

This attribute represents the redirect action.

    action:
      redirect:
       httpsRedirect: true
       responseCode: 302

The following table explains the various fields in the `HTTPRoute.rules.action.redirect` attribute.

| Field            | Description                                                                              | Type    | Required |
|------------------|------------------------------------------------------------------------------------------|---------|----------|
| `httpsRedirect`    | Redirects the HTTP traffic to HTTPS if this field is set to `yes`. Only the scheme is changed to HTTPS without modifying the other URL part. Either `httpsRedirect`, `hostRedirect` or `targetExpression` is required.                                     | boolean | No       |
| `hostRedirect`     | Rewrites the host name part of the URL to the value set in this attribute and redirect the traffic. Other part of the URL is not modified during redirection.        | string  | No       |
| `targetExpression` | Specifies the Citrix ADC expression for redirection. For example, to redirect traffic to HTTPS from HTTP, the following expression can be used: "\"https://\"+HTTP.REQ.HOSTNAME + HTTP.REQ.URL.HTTP_URL_SAFE".                     | string  | No       |
| `responseCode`    | Specifies the response code. The default response code is 302, which can be customized using this attribute.            | Integer | No       |