# TCP and HTTP use cases

This topic covers various TCP and HTTP use cases that you can configure on the Ingress Citrix ADC using the annotations in Citrix ingress controller.

The following table lists the TCP and HTTP use cases with sample annotations:

| Use case | Sample annotation |
| -------- | ----------------- |
| [Handling HTTP session timeouts](#handling-http-session-timeouts) | `ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "reqtimeoutaction":"DROP"}}'` </br> </br> `ingress.citrix.com/frontend-httpprofile: '{"apache":{"reqtimeout" : "10", "adptimeout" : "ENABLE"}}'` </br> </br>  `ingress.citrix.com/backend-httpprofile: '{"apache":{"reusepooltimeout" : "20000"}}'` |
| [Silently drop idle TCP connections](#silently-drop-idle-tcp-connections) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"DropHalfClosedConnOnTimeout" : "ENABLE", "DropEstConnOnTimeout":"ENABLE"}}'`|
| [Delayed TCP connection acknowledgments](#delayed-tcp-connection-acknowledgements) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"delayack" : "150"}}'` |
[Client side MPTCP session management](#client-side-mptcp-session-management) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"mptcp": "ENABLED", "mptcpSessionTimeout":"7200"}}'` |

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


## Silently drop idle TCP connections

In a network, large number of TCP connections become idle, and the Ingress Citrix ADC sends RST packets to close them. The packets sent over the channels activate those channels unnecessarily, causing a flood of messages that in turn causes the Ingress Citrix ADC to generate a flood of service-reject messages.

Using the `drophalfclosedconnontimeout` and `dropestconnontimeout` parameters in TCP profiles, you can silently drop TCP half closed connections on idle timeout or drop TCP established connections on an idle timeout. By default, these parameters are disabled on the Ingress Citrix ADC. If you enable both of them, neither a half closed connection nor an established connection causes an RST packet to be sent to the client when the connection times out. The Citrix ADC just drops the connection.

Using the annotations for TCP profiles, you can enable or disable the `drophalfclosedconnontimeout` and `dropestconnontimeout` on the Ingress Citrix ADC. The following is a sample annotation of TCP profile to enable these parameters:

    ingress.citrix.com/frontend-tcpprofile: '{"apache":{"drophalfclosedconnontimeout" : "enable", "dropestconnontimeout":"enable"}}'

## Delayed TCP connection acknowledgments

To avoid sending several ACK packets, Ingress Citrix ADC supports TCP delayed acknowledgment mechanism. It sends delayed ACK with a default timeout of 100 ms. Ingress Citrix ADC accumulates data packets and sends ACK only if it receives two data packets in continuation or if the timer expires. The minimum delay you can set for the TCP deployed ACK is 10 ms and the maximum is 300 ms. By default the delay is set to 100 ms.

Using the annotations for TCP profiles, you can manage the delayed ACK parameter. The following is a sample annotation of TCP profile to enable these parameters:

    ingress.citrix.com/frontend-tcpprofile: '{"apache":{"delayack" : "150"}}'

## Client side MPTCP session management

You perform TCP configuration on the Ingress Citrix ADC for MPTCP connections between the client and Ingress Citrix ADC. MPTCP connections are not supported between Citrix ADC and the back-end communication. Both the client and the Ingress Citrix ADC appliance must support the same MPTCP version.

You can enable MPTCP and set the MPTCP session timeout (`mptcpsessiontimeout`) in seconds using TCP profiles in the Ingress Citrix ADC. If the `mptcpsessiontimeout` value is not set then the MPTCP sessions are flushed after the client idle timeout. The minimum timeout value you can set is 0 and the maximum is 86400. By default, the timeout value is set to 0.

Using the annotations for TCP profiles, you can enable MPTCP and set the `mptcpsessiontimeout` parameter value on the Ingress Citrix ADC. The following is a sample annotation of TCP profile to enable MPTCP and set the `mptcpsessiontimeout` parameter value to 7200 on the Ingress Citrix ADC:

    ingress.citrix.com/frontend-tcpprofile: '{"apache":{"mptcp" : "ENABLED", "mptcpSessionTimeout":"7200"}}'
