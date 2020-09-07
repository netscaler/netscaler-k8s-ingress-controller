
# Listener

The Listener CRD represents the endpoint information of the content switching load balancing virtual server. This topic contains a sample Listener CRD object and also explains the various attributes of the Listener CRD. For the complete CRD definition, see [Listener.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/contentrouting/Listener.yaml).

## Listener CRD object example

The following is an example of a Listener CRD object.

```yml

apiVersion: citrix.com/v1alpha1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: 192.168.0.1
  port: 443
  protocol: https
  certificates:
  - secret:
      name: my-secret
      namespace: demo
  - default: true
    preconfigured: configured-secret
  routes:
  - labelSelector:
      xyz: abc
  - name: domain-1
    namespace: default
  - name: domain-2
    namespace: default
  defaultAction:
    backend:
      kube:
        namespace: default
        port: 80
        service: default-service
        backendConfig:
          lbConfig:
            lbmethod: ROUNDROBIN
          servicegroupConfig:
            clttimeout: '20'
```

For more examples, see [Listener Examples](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/contentrouting/Listener_examples).

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

## Listener.certificates

The `Listener.certificates` attribute defines the TLS certificate related information for the SSL virtual server.

Following is an example for the `Listener.certificates` attribute.


    certificates:
        - secret:
           name: my-secret
           namespace: demo
          default: true
        - preconfigured: configured-secret

The following table explains the various fields in the `Listener.certificates` attribute.

| Field         | Description                                                                                                                                     | Type                | Required |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|----------|
| `secret`       | Specifies TLS certificates specified through the Kubernetes secret resource. The secret must contain keys `tls.crt` and `tls.key`. These keys contain the certificate and private key. Either the secret or the preconfigured field is required. All certificates are bound to the SSL virtual server as SNI certificates.                                                                        | [certificates.secret](#ListenercertificatesSecret) | No       |
| `preconfigured` | Specifies the name of the preconfigured TLS `certkey` in Citrix ADC, and this field is applicable only for Tier-1 VPX and MPX devices. The `certkey` must be present before the actual deployment of the Listener resource and otherwise deployment of the resource fails with an error. The Citrix ingress controller does not manage the life cycle of `certkey`. So, you have to manage any addition or deletion of `certkey`  manually. Either the secret or the preconfigured field is required.                                          | string              | No       |
| `default`       | Specifies the default certificate. Only one of the certificates can be marked as default. The default certificate is presented if virtual server receives the traffic without an SNI field. This certificate can be used to access the HTTPS application using the IP Address. Applicable values are `true` and `false` | boolean                | No       |
|               |                                                  |                     |          |

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

This attribute represents the default action if a request to the load balancing virtual server does not match any of the route objects presented in the `Listener.route` field.

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

        kube:
          service: default-service
          namespace: default
          port: 80
          backendConfig:
            lbConfig:
              lbmethod: ROUNDROBIN
            servicegroupConfig:
              clttimeout: '20'

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

## Listener.action.redirect

    defaultAction:
      redirect:
       httpsRedirect: true
       responseCode: 302

The following table explains the various fields in the `Listener.action.redirect` attribute.

| Field            | Description                                                                              | Type    | Required |
|------------------|------------------------------------------------------------------------------------------|---------|----------|
| `httpsRedirect`    | Redirects the HTTP traffic to HTTPS if this field is set to `yes`. Only the scheme is changed to HTTPS without modifying the other URL part. Either `httpsRedirect`, `hostRedirect` or `targetExpression` is required.                                     | boolean | No       |
| `hostRedirect`     | Rewrites the host name part of the URL to the value set here and redirect the traffic. Other part of the URL is not modified during redirection.        | string  | No       |
| `targetExpression` | Specifies the Citrix ADC expression for redirection. For example, to redirect traffic to HTTPS from HTTP, the following expression can be used: *"\"https://\"+HTTP.REQ.HOSTNAME + HTTP.REQ.URL.HTTP_URL_SAFE"*.                     | string  | No       |
| `responseCode`    | Specifies the response code. The default response code is 302, which can be customized using this attribute.            | Integer | No       |