# Configure TCP, HTTP, SSL support for services of type LoadBalancer

This topic contains information on how to apply TCP, HTTP, or SSL profiles for services of type `LoadBalancer`. TCP, HTTP, or SSL profile support for service of type `LoadBalancer` is similar to TCP profile support on Ingress.
For information on TCP, HTTP or SSL profile support on Ingress, see [TCP profile support on Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/profiles/#tcp-profile).

A profile is a collection of settings pertaining to the individual protocols. For example, a TCP profile is a collection of TCP settings. Instead of configuring the settings on each entity, you can configure the settings in a profile and bind the profile to all the required entities.

For services of type LoadBalancer, when there is more than one port defined, all ports must have the same protocol and the protocol must be one of TCP, UDP, and SCTP.

## User-defined profiles

Using service annotations for TCP, HTTP, and SSL, you can create custom profiles with the same name as content switching virtual server or service group and bind to the corresponding virtual server and service group.

## Built-in profiles

Built-in profiles do not create any profile and bind a given profile name in an annotation to the corresponding virtual server and service group. Here, given profiles can be built-in profiles available with the Citrix ADC or any profile created on the Citrix ADC to use with cloud native deployments.

## TCP profile support

The Citrix ingress controller provides the following service annotations for TCP profile for services of type `LoadBalancer`. You can use these annotations to define the TCP settings for the Citrix ADC.

| Service annotation | Description|
| ---------------- | ------------ |
| `service.citrix.com/frontend-tcpprofile` | Use this annotation to create the front-end TCP profile (**Client Plane**). |
| `service.citrix.com/backend-tcpprofile` | Use this annotation to create the back-end TCP profile (**Server Plane**). |

### User-defined TCP profiles

Using service annotations for TCP, you can create custom profiles with the same name as cs virtual server or service group and bind to the corresponding virtual server(`frontend-tcpprofile`) and service group (`backend-tcpprofile`).

| Service annotation|  Sample |
| ---------------- |  ----- |
| `service.citrix.com/frontend-tcpprofile` | `service.citrix.com/frontend-tcpprofile: '{"ws":"enabled", "sack" : "enabled"}'`  |
| `service.citrix.com/backend-tcpprofile` |  `service.citrix.com/backend-tcpprofile: '{"ws":"enabled", "sack" : "enabled"}'`  |

### Built-in TCP profiles

Built-in TCP profiles do not create any profile and bind a given profile name in the annotation to the corresponding virtual server(frontend-tcpprofile) and service group(backend-tcpprofile).

Following are examples for built-in TCP profiles.

    service.citrix.com/frontend-tcpprofile: "tcp_preconf_profile"
    service.citrix.com/backend-tcpprofile: "tcp_preconf_profile"

### Example: Service of Type load balancer with the TCP profile configuration

In this example, TCP profiles are configured for a sample application `tea-beverage`. This application is deployed and exposed using a service of type LoadBalancer using the [tea-profile-example.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/example/tcp-profile-typelb/tea-profile-example.yaml) file.

For step by step instruction for exposing services of type `LoadBalancer`, see [service of type `LoadBalancer`](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/).

Following is a snippet of the service configuration with TCP profile.

    apiVersion: v1
    kind: Service
    metadata:
    name: tea-beverage
    annotations:
      service.citrix.com/secure_backend: '{"443-tcp": "True"}'
      service.citrix.com/service_type: 'SSL'
      service.citrix.com/backend-tcpprofile: '{"ws":"ENABLED", "sack" : "enabled"}'
      service.citrix.com/frontend-tcpprofile: '{"ws":"ENABLED", "sack" : "enabled"}'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: tea-443
    port: 443
    targetPort: 443
    selector:
    name: tea-beverage

### Example: Service of Type load balancer with TCP configuration for multiple ports

Following is a snippet of the TCP profile configuration for a service with multiple ports.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-tcpprofile: '{"80-tcp":{"sack" : "enabled"}, "443-tcp":{"ws":"ENABLED"}}'
      service.citrix.com/backend-tcpprofile: '{"80-tcp":{"sack" : "enabled"}, "443-tcp":{"ws":"ENABLED"}}'
      service.citrix.com/service_type: 'TCP'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 80
       targetPort: 9376

     - name: https
       protocol: TCP
       port: 443
       targetPort: 9377
    selector:
     app: apache

### Example: Built-in TCP profile

Following is a sample snippet of the TCP profile configuration.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-tcpprofile: 'nstcp_internal_apps'
      service.citrix.com/backend-tcpprofile: 'nstcp_internal_apps'
      service.citrix.com/service_type: 'TCP'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 80
       targetPort: 9376
    selector:
     app: apache

## HTTP profile support for Service of Type `LoadBalancer`

The Citrix ingress controller provides the following service annotations configuring HTTP profiles for services of type `LoadBalancer`.
You can use these annotations to define the HTTP settings for the Citrix ADC.

| Service annotation | Description|
| ---------------- | ------------ |
| `service.citrix.com/frontend-httpprofile` | Use this annotation to create the front-end HTTP profile (**Client Plane**). |
| `service.citrix.com/backend-httpprofile` | Use this annotation to create the back-end HTTP profile (**Server Plane**). |

### User-defined HTTP profiles

Following are examples of user-defined HTTP profiles:

Without port-protocol:

`service.citrix.com/frontend-httpprofile: '{"dropinvalreqs":"enabled","markconnreqinval" : "enabled"}'`
`service.citrix.com/backend-httpprofile: '{"80-tcp":{"dropinvalreqs":"enabled"},"443-tcp":{"markconnreqinval" : "enabled"}}'`

With port-protocol:

`service.citrix.com/frontend-httpprofile: '{"80-tcp":{"dropinvalreqs":"enabled"},"443-tcp":{"markconnreqinval" : "enabled"}}'`
`service.citrix.com/backend-httpprofile: '{"80-tcp":{"dropinvalreqs":"enabled"},"443-tcp":{"markconnreqinval" : "enabled"}}'`


### Built-in HTTP profiles

Following are examples for built-in HTTP profiles.

      service.citrix.com/frontend-httpprofile: 'nshttp_default_internal_apps'
      service.citrix.com/backend-httpprofile: 'nshttp_default_internal_apps'

### Example: Service of Type `LoadBalancer` with HTTP profile configuration for single port

Following is a snippet of the service configuration with an HTTP profile.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-httpprofile: '{"dropinvalreqs":"enabled", "markconnreqinval" : "enabled"}'
      service.citrix.com/backend-httpprofile: '{"dropinvalreqs":"enabled", "markconnreqinval" : "enabled"}'
      service.citrix.com/service_type: 'HTTP'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: tea-443
       protocol: HTTP
       port: 80
       targetPort: 9376
    selector:
      app: apache

### Example: Service of Type `LoadBalancer` with HTTP profile configuration for multiple ports

Following is a snippet of the HTTP profile configuration for a service with multiple ports.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-httpprofile: '{"80-tcp":{"dropinvalreqs":"enabled"},"443-tcp":{"markconnreqinval" : "enabled"}}'
      service.citrix.com/backend-httpprofile: '{"80-tcp":{"dropinvalreqs":"enabled"},"443-tcp":{"markconnreqinval" : "enabled"}}'
      service.citrix.com/service_type: 'HTTP'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 80
       targetPort: 9376

     - name: https
       protocol: TCP
       port: 443
       targetPort: 9377
    selector:
      app: apache

### Example: Built-in HTTP profile

Following is a sample snippet of the built-in HTTP profile configuration.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-httpprofile: 'nshttp_default_internal_apps'
      service.citrix.com/backend-httpprofile: 'nshttp_default_internal_apps'
      service.citrix.com/service_type: 'HTTP'  
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 80
       targetPort: 9376
    selector:
     app: apache

## Service Type `Loadbalancer` with SSL profile

The Citrix ingress controller provides the following service annotations for the SSL profile for services of type `LoadBalancer`.
You can use these annotations to define the SSL settings for the Citrix ADC.

| Service annotation | Description|
| ---------------- | ------------ |
| `service.citrix.com/frontend-sslprofile` | Use this annotation to create the front-end SSL profile (**Client Plane**). |
| `service.citrix.com/backend-sslprofile` | Use this annotation to create the back-end SSL profile (**Server Plane**). |

### User-defined SSL profiles

Following are examples of user-defined SSL profiles:

  `service.citrix.com/frontend-sslprofile: '{"snienable": "enabled"}'`
  `service.citrix.com/backend-sslprofile: '{"snienable": "enabled", "commonname":"abc.com"}'`

### Built-in SSL profiles

Following are examples of built-in SSL profiles:

  `service.citrix.com/frontend-sslprofile: 'ns_default_ssl_profile_secure_frontend'`
  `service.citrix.com/backend-sslprofile: 'ns_default_ssl_profile_backend'`


### Example: Service of Type LoadBalancer with single port SSL profile

Following is a snippet of the service configuration with SSL profile.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-sslprofile: '{"snienable": "enabled"}'
      service.citrix.com/backend-sslprofile: '{"snienable": "enabled", "commonname":"abc.com"}'
      service.citrix.com/service_type: 'SSL'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - port: 80
       targetPort: 9376
    selector:
     app: apache

### Example: Service of Type LoadBalancer with SSL profile configuration for multiple ports

Following is the snippet of the SSL profile configuration for a service with multiple ports.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-sslprofile: '{"443-tcp":{"snienable": "enabled"}, "8443-tcp":{"clientauth":"enabled"}}'
      service.citrix.com/backend-sslprofile: '{"443-tcp": {"snienable": "enabled", "commonname":"abc.com"}, "8443-tcp":{"snienable": "enabled", "commonname":"def.com"}}'
      service.citrix.com/service_type: 'SSL'
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 443
       targetPort: 9376

     - name: https
       protocol: TCP
       port: 8443
       targetPort: 9377
    selector:
     app: apache

### Example: Built-in SSL profile

Following is a sample snippet of the built-in SSL profile configuration.

    apiVersion: v1
    kind: Service
    metadata:
    name: apache
    annotations:
      service.citrix.com/frontend-sslprofile: 'ns_default_ssl_profile_secure_frontend'
      service.citrix.com/backend-sslprofile: 'ns_default_ssl_profile_backend'
      service.citrix.com/service_type: 'ssl'  
    spec:
      type: LoadBalancer
      loadBalancerIP: 192.0.2.194
    ports:
     - name: http
       protocol: TCP
       port: 80
       targetPort: 9376
    selector:
     app: apache