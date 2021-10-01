
# Listener

The Listener CRD represents the endpoint information of the content switching load balancing virtual server. This topic contains a sample Listener CRD object and also explains the various attributes of the Listener CRD. For the complete CRD definition, see [Listener.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/contentrouting/Listener.yaml).

## Listener CRD object example

The following is an example of a Listener CRD object.

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: my-listener
  namespace: default
spec:
  certificates:
  - secret:
      name: my-secret
    # Secret named 'my-secret' in current namespace bound as default certificate
    default: true
  - secret:
      # Secret 'other-secret' in demo namespace bound as SNI certificate
      name: other-secret
      namespace: demo
  - preconfigured: second-secret
    # preconfigured certkey name in ADC
  vip: '192.168.0.1' # Virtual IP address to be used, not required when CPX is used as ingress device
  port: 443
  protocol: https
  redirectPort: 80
  secondaryVips:
  - "10.0.0.1"
  - "1.1.1.1"
  policies:
    httpprofile:
      config:
        websocket: "ENABLED"
    tcpprofile:
      config:
        sack: "ENABLED"
    sslprofile:
      config:
        ssl3: "ENABLED"
    sslciphers:
    - SECURE
    - MEDIUM
    analyticsprofile:
      config:
      - type: webinsight
        parameters:
           allhttpheaders: "ENABLED"
    csvserverConfig:
      rhistate: 'ACTIVE'
  routes:
    # Attach the policies from the below Routes
  - name: domain1-route
    namespace: default
  - name: domain2-route
    namespace: default
  - labelSelector:
      # Attach all HTTPRoutes with label route=my-route
      route: my-route
  # Default action when traffic matches none of the policies in the HTTPRoute
  defaultAction:
    backend:
      kube:
        namespace: default
        port: 80
        service: default-service
        backendConfig:
          lbConfig:
            # Use round robin LB method for default service
            lbmethod: ROUNDROBIN
          servicegroupConfig:
            # Client timeout of 20 seconds
            clttimeout: "20"

```
For more examples, see [Listener examples](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/contentrouting/Listener_examples).

## Listener.spec

The `Listener.spec` attribute defines the Listener custom resource specification. The following table explains the various fields in the `Listener.spec` attribute.

| Field         | Description                                                                                                            | Type&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;             | Required |
|---------------|------------------------------------------------------------------------------------------------------------------------|------------------|----------|
| `protocol`      |Specifies the protocol of the load balancing content switching virtual server. Allowed values are: `http` and `https`.                            | string           | yes      |
| `port`          | Specifies the port number of the load balancing content switching virtual server. The default port number for the HTTP protocol is 80 and the HTTPS protocol is 443.          | integer          | No       |
| `routes`        |Specifies the list of HTTPRoute resources that is to be attached to the Listener resource. The order of evaluation is as per the order of the list. That is, if multiple entries are present first route specified in the list has highest priority and so on.   | [ ] [routes](#Listenerroutes)      | No       |
| `certificates`  |Specifies the list of certificates for the SSL virtual server if the protocol is HTTPS. This field is required if the protocol is HTTPS.                   | [ ] [certificates](#Listenercertificates)  |  No       |
| `vip `          | Specifies the endpoint IP Address for the load balancing content switching virtual server. This address is required for Citrix ADC VPX and MPX devices, but not required for Citrix ADC CPXs present in the Kubernetes cluster. For Citrix ADC CPX, `vip` is same as the primary IP address of the Citrix ADC CPX allocated by the CNI.                                                | string           | No       |
| `defaultAction` | Specifies the default action to take if none of the HTTPRoute resources specified in `routes` match the traffic.| action           | No       |
| `policies`      | Specifies the option that enables you to customize HTTP, TCP, and SSL policies associated with the front-end virtual server.       | [ ] [Listener.policies](#Listenerpolicies)      | No      |
| `redirectPort`     | Specifies that the HTTP traffic on this port is redirected to the HTTPS port. | Integer        | No      |
| `secondaryVips`          | Specifies a set of IP addresses which are used as VIPs with the primary VIP. An IPset is created and these VIPs are added to the IPset.       | [ ] string       | No     |

## Listener.certificates

The `Listener.certificates` attribute defines the TLS certificate related information for the SSL virtual server.

Following is an example for the `Listener.certificates` attribute.
```yml
    certificates:
    - secret:
        name: my-secret
        namespace: demo
      default: true
    - preconfigured: configured-secret
```

The following table explains the various fields in the `Listener.certificates` attribute.

| Field         | Description                                                                                                                                     | Type                | Required |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|----------|
| `secret`       | Specifies TLS certificates specified through the Kubernetes secret resource. The secret must contain keys `tls.crt` and `tls.key`. These keys contain the certificate and private key. Either the secret or the preconfigured field is required. All certificates are bound to the SSL virtual server as SNI certificates.                                                                        | [certificates.secret](#ListenercertificatesSecret) | No       |
| `preconfigured` | Specifies the name of the preconfigured TLS `certkey` in Citrix ADC, and this field is applicable only for Tier-1 VPX and MPX devices. The `certkey` must be present before the actual deployment of the Listener resource and otherwise deployment of the resource fails with an error. The Citrix ingress controller does not manage the life cycle of `certkey`. So, you have to manage any addition or deletion of `certkey`  manually. Either the secret or the preconfigured field is required.                                          | string              | No       |
| `default`       | Specifies the default certificate. Only one of the certificates can be marked as default. The default certificate is presented if virtual server receives the traffic without an SNI field. This certificate can be used to access the HTTPS application using the IP Address. Applicable values are `true` and `false` | boolean                | No       |


## Listener.certificates.Secret

This attribute represents the Kubernetes secret resource for the TLS certificates that has to be bound to the SSL virtual server.

The following table explains the various fields in the `Listener.certificate.Secret` attribute.

| Field     | Description                    | Type   | Required |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|
| `name`      |Specifies the name of the Kubernetes secret resource. The secret must contain keys named `tls.crt` and `tls.key`. These keys contain the certificate and private key. If more than one `tls.crt` field is present in the secret object, then the first certificate is considered as a server certificate and remaining certificates are considered as intermediate CA certificates. Also, certificates are linked recursively to each other starting from the server certificate.                                                                                              | string | yes      |
| `namespace` |Specifies the namespace of the Kubernetes secret resource. If this value is not specified, the namespace is considered as same as the Listener resource.                                                                                                                                                                                                | string | No       |

## Listener.routes

This attribute represents the list of HTTPRoute objects that are attached to the Listener resource.
The following table explains the various fields in the `Listener.routes` attribute.

| Field         | Description                                                                                                                                                                              | Type   | Required |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|
| `name`          | Specifies the name of the HTTPRoute resource evaluated for the routing decision to the back end server. Either the `name` or the `labelSelector` is required.                                                                                   | string | No       |
| `namespace`     | Specifies the namespace of the HTTPRoute resource. The default value is the name space of the Listener resource.                                                                                                 | string | No       |
| `labelSelector` | Specifies the label selector of the HTTPRoute resource. This field provides another way to attach HTTPRoute resources. HTTPRoute objects with label keys and values matching this selector are automatically attached to the listener resource. If routes get attached through the labelSelector, routes are attached without any specific order. Exception for this rule is a route with a default path ('/') which is always attached at the end. As shown in the example, any HTTPRoute objects with labels and are attached to the listener object. For more information on labels and selectors, see the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).          | object | No       |

## Listener.action

This attribute represents the default action if a request to the load balancing virtual server does not match any of the route objects presented in the [Listener.routes](#Listenerroutes) field.

The following table explains the various fields in the `Listener.action` attribute.

| Field    | Description                                                                          | Type            | Required |
|----------|--------------------------------------------------------------------------------------|-----------------|----------|
| `backend`  | The default action for this field is to send the traffic to a back-end service. Either the back end or the redirect is required. | [action.backend](#Listeneractionbackend)  | No       |
| `redirect` | The default action is to redirect the traffic. Either the back end or redirect is required.      | [action.redirect](#Listeneractionredirect) | No    |


## Listener.action.backend

This attribute specifies the back end service for the default action.
The following table explains the various fields in the `Listener.action.backend` attribute.

| Field | Description                                            | Type                | Required |
|-------|--------------------------------------------------------|---------------------|----------|
| `kube`  | Specifies the Kubernetes service information for the back end service. | [action.backend.kube](#Listeneractionbackendkube) |          |

## Listener.action.backend.kube

This attribute represents the Kubernetes back end service for the default back end. If the service is of type `NodePort` or `Loadbalancer`, the node IP address and NodePort are used to send the traffic to the back end.

Following is an example for the `Listener.action.backend.kube` attribute.
```yml
        kube:
          service: default-service
          namespace: default
          port: 80
          backendConfig:
            lbConfig:
              lbmethod: ROUNDROBIN
            servicegroupConfig:
              clttimeout: '20'
```

The following table explains the various fields in the `Listener.action.backend.kube` attribute.

| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `service `      | Specifies the name of the Kubernetes service for the default back end.      | string        | yes      |
| `namespace`     | Specifies the namespace of the Kubernetes service for the default back end. | string        | yes      |
| `port`          | Specifies the port number of the Kubernetes service for the default back end.      | integer       | yes      |
| `backendConfig` | Specifies the back-end configurations for the default back end.          | [BackendConfig](#BackendConfig) | no       |

## BackendConfig

This attribute represents the back end configurations of Citrix ADC.
Following is an example for the `BackendConfig` attribute.
```yml
    backendConfig:
     sercureBackend: true
     lbConfig:
       lbmethod: ROUNDROBIN
     servicegroupConfig:
       clttimeout: '20'
```

The following table explains the various fields in the `BackendConfig` attribute.

| Field              | Description                                                                                                                                                                             | Type   | Required |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|
| `secureBackend`      | Specifies whether the communication is secure or not. If the value of the `secureBackend` field is  `true` secure communication is used to communicate with the back end. The default value is `false`, that means HTTP is used for the back end communication.                                            |        |          |
| `lbConfig`          | Specifies the Citrix ADC load balancing virtual server configurations for the given back end. One can specify key-value pairs as shown in the example which sets the LBVserver configurations for the back end. For all the valid configurations, see [LB virtual server configurations](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/lb/lbvserver/).             | object | No       |
| `servicegroupConfig` | Specifies the Citrix ADC service group configurations for the given back end. One can specify the key-value pairs as shown in the example which sets the service group configurations for the back end. For all the valid configurations, see [service group configurations](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/basic/servicegroup/).| object | No       |

## Listener.action.redirect
```yml
    defaultAction:
      redirect:
       httpsRedirect: true
       responseCode: 302
```

The following table explains the various fields in the `Listener.action.redirect` attribute.

| Field            | Description                                                                              | Type    | Required |
|------------------|------------------------------------------------------------------------------------------|---------|----------|
| `httpsRedirect`    | Redirects the HTTP traffic to HTTPS if this field is set to `yes`. Only the scheme is changed to HTTPS without modifying the other URL part. Either `httpsRedirect`, `hostRedirect` or `targetExpression` is required.                                     | boolean | No       |
| `hostRedirect`     | Rewrites the host name part of the URL to the value set here and redirect the traffic. Other part of the URL is not modified during redirection.        | string  | No       |
| `targetExpression` | Specifies the Citrix ADC expression for redirection. For example, to redirect traffic to HTTPS from HTTP, the following expression can be used: *"\"https://\"+HTTP.REQ.HOSTNAME + HTTP.REQ.URL.HTTP_URL_SAFE"*.                     | string  | No       |
| `responseCode`    | Specifies the response code. The default response code is 302, which can be customized using this attribute.            | Integer | No       |

## Listener.policies

This attribute represents the default policies which are used for the Listener when policies are not specified. By using `Listener.policies`, you can customize the TCP, HTTP, and SSL behavior.

Following is an example for the `Listener.policies` attribute.
```yml
    policies:
     httpprofile:
      config:
       websocket: "ENABLED"
     tcpprofile:
      config:
       sack: "ENABLED"
     sslprofile:
      config:
       ssl3: "ENABLED"
     sslciphers:
      - HIGH
      - MEDIUM
      analyticsprofile:
       config:
       - type: webinsight
         parameters:
          allhttpheaders: "ENABLED"
      csvserverConfig:
       rhistate: 'ACTIVE'
       stateupdate: ‘ENABLED’
```
The following table explains the various fields in the `Listener.policies` attribute.

| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `httpprofile`      | Specifies the HTTP configuration for the front end virtual server.      | [Listener.policies.httpprofile](#Listenerpolicieshttpprofile)        | No      |
| `tcpprofile`     | Specifies the TCP configuration for the front-end virtual server. | [Listener.policies.tcpprofile](#Listenerpoliciestcpprofile)        | No      |
| `sslprofile`          | Specifies the SSL configuration for the front-end virtual server      | [Listener.policies.sslprofile](#Listenerpoliciessslprofile)       | No      |
| `sslciphers` | Specifies the list of ciphers which are to be bound to the SSL profile. The order is as specified in the list with the higher priority is provided to the first in the list and so on. You can use any SSL ciphers available in Citrix ADC or user created cipher groups in this field. For information about the list of ciphers available in the Citrix ADC, see [Ciphers in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-adc-appliances.html).| [ ] string | No       |
| `analyticsprofile`      | Specifies the analytics profile configuration for the front-end virtual server     | [Listener.policies.analyticsprofile](#Listenerpoliciesanalyticsprofile)        | No      |
| `csvserverConfig`     | Specifies the front-end CS virtual server configuration for the Listener. You can specify the key value pair as shown in the example which sets the CS virtual server configuration for the front-end.  | Object        | No     |

## Listener.policies.tcpprofile

This attribute represents the TCP profile settings for the front-end CS virtual server.

Following is an example for the `Listener.policies.tcpprofile` attribute.
```yml
    policies:
     tcpprofile:
      config:
       sack: "ENABLED"
       nagle: “ENABLED”
---
    policies:
     tcpprofile:
      preconfigured: test-tcp-profile
```
The following table explains the various fields in the `Listener.policies.tcpprofile` attribute.

| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `preconfigured `      | Specifies the name of the preconfigured TCP profile that is to be used for the front-end CS virtual server. This profile must be present in the Citrix ADC before applying the policy. Otherwise, the Listener resource fails to apply. Either `preconfigured` or `config` is required.      | string        | No     |
| `config`     | Specifies the [TCP profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ns/nstcpprofile/) settings for the front-end virtual server. You can specify the key-value pair as shown in the example to tune the TCP characteristics of the virtual server.  | Object        | No      |

## Listener.policies.httpprofile

This attribute represents the HTTP configuration for the front-end CS virtual server.

Following is an example for the `Listener.policies.httpprofile` attribute.
```yml
    policies:
     httpprofile:
      config:
       websocket: "ENABLED"
---
    policies:
     httpprofile:
     preconfigured: test-http-profile
```
The following table explains the various fields in the `Listener.policies.httpprofile` attribute.

| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `preconfigured`      | Specifies the name of the preconfigured HTTP profile that is to be used for the front end CS virtual server. This profile must be present in the Citrix ADC before applying the policy. Otherwise, Listener resource fails to apply. Either `preconfigured` or `config` is required.      | string        | No      |
| `config`     | Specifies the [HTTP profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ns/nshttpprofile/)  settings for the front-end virtual server. You can specify the key-value pair as shown in the example to tune the HTTP protocol characteristics of the virtual server.  | Object        | No      |

## Listener.policies.sslprofile

This attribute represents the SSL profile for the front-end CS virtual server.

Following is an example for the `Listener.policies.sslprofile` attribute.
```yml
    policies:
     sslprofile:
      config:
       ssl3: "ENABLED"
---
    policies:
     sslprofile:
      preconfigured: test-ssl-profile
```
The following table explains the various fields in the `Listener.policies.sslprofile` attribute.


| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `preconfigured`      | Specifies the name of the preconfigured SSL profile that is to be used for the front-end SSL virtual server. This profile must be present in the Citrix ADC before applying the policy. Otherwise, the Listener resource fails to apply. Either `preconfigured` or `config` is required.    |string        | No      |
| `config`     | Specifies the [SSL profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ssl/sslprofile/) configuration for the front-end virtual server. You can specify the key-value pair as shown in the example to tune the SSL characteristics of the virtual server. **Note:** You must enable the default profiles using `set ssl parameter -defaultProfile ENABLED` in Citrix ADC for using the advanced SSL features.  | Object        | No      |

## Listener.policies.analyticsprofile

This attribute represents the analytics profile that is used to export counters and metrics to Citrix ADC Observability Exporter. By configuring this attribute, you can choose what is to be exported by creating and binding the analytics profile.

Following is an example for the `Listener.policies.analyticsprofile` attribute.

```yml
    policies:
     analyticsprofile:
      config:
      - type: webinsight
        parameters:
         allhttpheaders: "ENABLED"
---
    policies:
     analyticsprofile:
      preconfigured:
      - test-analytics-profile
      - test2-analytics-profile
```
The following table explains the various fields in the `Listener.policies.analyticsprofile` attribute.


| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `preconfigured`      | Specifies the list of preconfigured analytics profiles that needs to be bound to the front-end virtual server. These profiles must be present in the Citrix ADC before applying the policy. Otherwise, the Listener resource fails to apply. Either `preconfigured` or `config` is required.    | [ ] string        | No      |
| `config`     | Specifies the list of analytics profiles which is to be bound to the front-end virtual server. This determines the fields to be exported to Citrix ADC Observability Exporter.   | [ ] [Listener.policies.analyticsprofile.config](#Listenerpoliciesanalyticsprofileconfig)    | No      |

## Listener.policies.analyticsprofile.config

This attribute represents the analytics profile configuration for the different types of insights and HTTP header parameters which need to be exported.

The following table explains the various fields in the `Listener.policies.analyticsprofile.config` attribute.


| Field         | Description                                             | Type          | Required |
|---------------|---------------------------------------------------------|---------------|----------|
| `type`      | Specifies the type that determines the type of analytics profile to be enabled. You can enable one or more of the following types: `webinsight`, `tcpinsight`, `securityinsight`, `videoinsight`, `hdxinsight`, `gatewayinsight`, `timeseries`, `lsninsight`, and `botinsight`| string        | Yes      |
| `parameters`     | Specifies the additional parameters to be enabled as part of the [analytics profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/analytics/analyticsprofile/). You can specify the key-value pair as shown in the example. For example, using this field, you can select the HTTP parameters to be exported as part of `webinsight`   | Object        | No      |