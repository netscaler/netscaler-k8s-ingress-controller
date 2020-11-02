# TCP profile support for services of type LoadBalancer

This topic contains information on how to apply TCP profiles for services of type `LoadBalancer`. TCP profile support for service of type `LoadBalancer` is similar to TCP profile support on Ingress.
For information on TCP profile support on Ingress, see [TCP profile support on Ingress](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/profiles/#tcp-profile).

A TCP profile is a collection of TCP settings. Instead of configuring the settings on each entity, you can configure TCP settings in a profile and bind the profile to all the required entities.

The Citrix ingress controller provides the following service annotations for TCP profile for services of type `LoadBalancer`. You can use these annotations to define the TCP settings for the Citrix ADC.


| Service annotation | Description|
| ---------------- | ------------ |
| `service.citrix.com/frontend-tcpprofile` | Use this annotation to create the front-end TCP profile (**Client Plane**). |
| `service.citrix.com/backend-tcpprofile` | Use this annotation to create the back-end TCP profile (**Server Plane**). |

## User-defined TCP profiles

Using service annotations for TCP, you can create custom profiles with name same as cs virtual server or service group and bind to the corresponding virtual server(`frontend-tcpprofile`) and service group (`backend-tcpprofile`).

| Service annotation|  Sample |
| ---------------- |  ----- |
| `service.citrix.com/frontend-tcpprofile` | `service.citrix.com/frontend-tcpprofile: '{"ws":"enabled", "sack" : "enabled"}'`  |
| `service.citrix.com/backend-tcpprofile` |  `service.citrix.com/backend-tcpprofile: '{"ws":"enabled", "sack" : "enabled"}'`  |

## Built-in TCP profiles

Built-in TCP profiles do not create any profile and bind a given profile name in annotation to the corresponding virtual server(frontend-tcpprofile) and service group(backend-tcpprofile).

Following are examples for built-in TCP profiles.

    service.citrix.com/frontend-tcpprofile: "tcp_preconf_profile"
    service.citrix.com/backend-tcpprofile: '{"citrix-svc":"tcp_preconf_profile"}

## Example: Service of Type load balancer with the TCP profile configuration

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
      loadBalancerIP: 10.105.158.194
    ports:
     - name: tea-443
    port: 443
    targetPort: 443
    selector:
    name: tea-beverage


**Note:**
The TCP profile is supported for single port services.