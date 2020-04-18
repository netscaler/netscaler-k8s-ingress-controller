# HTTP use cases

This topic covers various HTTP use cases that you can configure on the Ingress Citrix ADC using the annotations in the Citrix ingress controller.

The following table lists the HTTP use cases with sample annotations:

| Use case | Sample annotation |
| -------- | ----------------- |
| [Configuring HTTP/2](#configuring-http2) | `ingress.citrix.com/frontend-tcpprofile: '{"http2":"ENABLED"}'` </br> </br>`ingress.citrix.com/backend-tcpprofile: '{"apache":{"http2Direct" : "ENABLED"}'` </br></br> `ingress.citrix.com/backend-tcpprofile: '{"apache":{"http2Direct" : "ENABLED", "altsvc":"ENABLED"}'` |
| [Handling HTTP session timeouts](#handling-http-session-timeouts) | `ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "reqtimeoutaction":"DROP"}}'` </br> </br> `ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "adptimeout" : "ENABLE"}}'` </br> </br>  `ingress.citrix.com/backend-httpprofile: '{"apache":{"reusepooltimeout" : "20000"}}'` |

## Configuring HTTP/2

The Ingress Citrix ADC HTTP/2 on the client side as well on the server side. For more information, see HTTP/2 support on Citrix ADC. For an HTTP load balancing configuration on the Ingress Citrix ADC, it uses one of the following methods to start communicating with the client/server using HTTP/2.

The Ingress Citrix ADC provides configurable options in an HTTP profile for the HTTP/2 methods. These HTTP/2 options can be applied to the client side as well to the server side of an HTTPS or HTTP load balancing setup. The Citrix ingress controller provides annotations to configure HTTP profile on the Ingress Citrix ADC. You use these annotations to configure the various HTTP loads balancing configuration on the Ingress Citrix ADC to communicate with the client/server using HTTP/2.

>IMPORTANT: Ensure that the HTTP/2 Service Side global parameter (HTTP2Serverside) is enabled on the Ingress Citrix ADC. For more information, see nshttpparam.

### HTTP/2 upgrade

In this method, a client sends an HTTP/1.1 request to a server. The request includes an upgrade header, which asks the server for upgrading the connection to HTTP/2. If the server supports HTTP/2, the server accepts the upgrade request and notifies it in its response. The client and the server start communicating using HTTP/2 after the client receives the upgrade confirmation response.

Using the annotations for HTTP profiles, you can configure the HTTP/2 upgrade method on the Ingress Citrix ADC. The following is a sample annotation of HTTP profile to configure HTTP/2 upgrade method on the Ingress Citrix ADC:

    ingress.citrix.com/frontend-tcpprofile: '{"http2":"ENABLED"}'

### Direct HTTP/2

In this method, a client directly starts communicating to a server in HTTP/2 instead of using the HTTP/2 upgrade method. If the server does not support HTTP/2 or is not configured to directly accept HTTP/2 requests, it drops the HTTP/2 packets from the client. This method is helpful if the admin of the client device already knows that the server supports HTTP/2.

Using the annotations for HTTP profiles, you can configure the direct HTTP/2 method on the Ingress Citrix ADC. The following is a sample annotation of HTTP profile to configure the direct HTTP/2 method on the Ingress Citrix ADC:

    ingress.citrix.com/backend-tcpprofile: '{"apache":{"http2Direct" : "ENABLED"}'

### Direct HTTP/2 using Alternative Service (ALT-SVC)

In this method, a server advertises that it supports HTTP/2 to a client by including an Alternative Service (ALT-SVC) field in its HTTP/1.1 response. If the client is configured to understand the ALT-SVC field, the client and the server start directly communicating using HTTP/2 after the client receives the response.

The following is a sample annotation of HTTP profile to configure the direct HTTP/2 using alternative service (ALT-SVC) method on the Ingress Citrix ADC:

    ingress.citrix.com/backend-tcpprofile: '{"apache":{"http2Direct" : "ENABLED", "altsvc":"ENABLED"}'

## Handling HTTP session timeouts

To handle the different type of HTTP request and also to mitigate attacks such as, Slowloris DDoS attack, where in the clients initiate connections that you might want to restrict. On the Ingress Citrix ADC, you can configure the following timeouts for these scenarios:

-  reqTimeout and reqTimeoutAction
-  adptTimeout
-  reusePoolTimeout

### reqTimeout and reqTimeoutAction

In Citrix ADC, you can configure the HTTP request timeout value and the request timeout action using the `reqTimeout` and `reqTimeoutAction` parameter in the HTTP profile. The `reqTimeout` value is set in seconds and the HTTP request must complete within the specified time in the `reqTimeout` parameter. If the HTTP request does not complete within defined time, the specified request timeout action in the `reqTimeoutAction` is executed. The minimum timeout value you can set is 0 and the maximum is 86400. By default, the timeout value is set to 0.

Using the `reqTimeoutAction` parameter you can specify the type of action that must be taken in case the HTTP request timeout value (`reqTimeout`) elapses. You can specify the following actions:

-  RESET
-  DROP

Using the annotations for HTTP profiles, you can configure the HTTP request timeout and HTTP request timeout action. The following is a sample annotation of HTTP profile to configure the HTTP request timeout and HTTP request timeout action on the Ingress Citrix ADC:

    ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "reqtimeoutaction":"DROP"}}'

### adptTimeout

Instead of using a set timeout value for the requested sessions, you can also enable `adptTimeout`. The `adptTimeout` parameter adapts the request timeout as per the flow conditions. If enabled, then request timeout is increased or decreased internally and applied on the flow. By default, this parameter is set as DISABLED.

Using annotations for HTTP profiles, you can enable or disable the `adpttimeout` parameter as follows:

    ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "adptimeout" : "ENABLE"}}'

### reusePoolTimeout

You can configure a reuse pool timeout value to flush any idle server connections in from the reuse pool. If the server is idle for the configured amount of time, then the corresponding connections are flushed.

The minimum timeout value you can set is 0 and the maximum is 31536000. By default, the timeout value is set to 0.

Using annotations for HTTP profiles, you can configure the required timeout value as follows:

    ingress.citrix.com/backend-httpprofile: '{"apache":{"reusepooltimeout" : "20000"}}'
