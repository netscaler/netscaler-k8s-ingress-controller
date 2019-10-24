# TCP use cases

This topic covers various TCP use cases that you can configure on the Ingress Citrix ADC using the annotations in the Citrix ingress controller.

The following table lists the TCP use cases with sample annotations:

| Use case | Sample annotation |
| -------- | ----------------- |
| [Silently drop idle TCP connections](#silently-drop-idle-tcp-connections) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"DropHalfClosedConnOnTimeout" : "ENABLE", "DropEstConnOnTimeout":"ENABLE"}}'`|
| [Delayed TCP connection acknowledgments](#delayed-tcp-connection-acknowledgements) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"delayack" : "150"}}'` |
[Client side MPTCP session management](#client-side-mptcp-session-management) | `ingress.citrix.com/frontend-tcpprofile: '{"apache":{"mptcp": "ENABLED", "mptcpSessionTimeout":"7200"}}'` |
| [TCP Optimization](#tcp-optimization) | N/A |
| [Defending TCP against spoofing attacks](#defend-tcp-against-spoofing-attacks) | `ingress.citrix.com/frontend_tcpprofile: '{"rstwindowattenuate" : "enabled", "spoofSynDrop":"enabled"}` |

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

## TCP Optimization

Most of the relevant TCP optimization capabilities of the Ingress Citrix ADC are exposed through a corresponding TCP profile. Using the annotations for TCP profiles, you can enable the following TCP optimization capabilities on the Ingress Citrix ADC:

-  **Selective acknowledgment (SACK)**: TCP SACK addresses the problem of multiple packet losses which reduces the overall throughput capacity. With selective acknowledgment the receiver can inform the sender about all the segments which are received successfully, enabling sender to only retransmit the segments which were lost. This technique helps T1 improve overall throughput and reduce the connection latency.

    The following is a sample annotation of TCP profile to enable SACK on the Ingress Citrix ADC:

        ingress.citrix.com/frontend_tcpprofile: '{"sack" : "enabled"}

-  **Forward acknowledgment (FACK)**: To avoid TCP congestion by explicitly measuring the total number of data bytes outstanding in the network, and helping the sender (either T1 or a client) control the amount of data injected into the network during retransmission timeouts.

    The following is a sample annotation of TCP profile to enable FACK on the Ingress Citrix ADC:

        ingress.citrix.com/frontend_tcpprofile: '{"fack" : "enabled"}

-  **Window Scaling (WS)**: TCP Window scaling allows increasing the TCP receive window size beyond 65535 bytes. It helps improving TCP performance overall and specially in high bandwidth and long delay networks. It helps with reducing latency and improving response time over TCP.

    The following is a sample annotation of TCP profile to enable WS on the Ingress Citrix ADC:

        ingress.citrix.com/frontend_tcpprofile: '{"ws" : "enabled", "wsval" : "9"}

    Where `wsval` is the factor used to calculate the new window size. The argument is mandatory only when window scaling is enabled.  The minimum value you can set is 0 and the maximum is 14. By default, the value is set to 4.

-  **Maximum Segment Size (MSS)**: MSS of a single TCP segment. This value depends on the MTU setting on intermediate routers and end clients. A value of 1460 corresponds to an MTU of 1500.

    The following is a sample annotation of TCP profile to enable MSS on the Ingress Citrix ADC:

        ingress.citrix.com/frontend_tcpprofile: '{"mss" : "1460", "maxPktPerMss" : "512"}

    Where:
    -  `mss` is the MSS to use for the TCP connection. The minimum value you can set is 0 and the maximum is 9176.
    -  `maxPktPerMss` is the maximum number of TCP packets allowed per maximum segment size (MSS). The minimum value you can set is 0 and the maximum is 1460.

-  **Keep-Alive (KA)**: Send periodic TCP keep-alive (KA) probes to check if the peer is still up.

    The following is a sample annotation of TCP profile to enable TCP keep-alive (KA) on the Ingress Citrix ADC:

        ingress.citrix.com/frontend_tcpprofile: '{"ka" : "enabled", "kaprobeupdatelastactivity":"enabled", "KAconnIdleTime": "900",  "kamaxprobes" : "3",  "kaprobeinterval" : "75"}

    Where:
    -  `ka` is used to enable sending periodic TCP keep-alive (KA) probes to check if the peer is still up. Possible values: ENABLED, DISABLED. Default value: DISABLED.
    -  `kaprobeupdatelastactivity` updates the last activity for the connection after receiving keep-alive (KA) probes.  Possible values: ENABLED, DISABLED. Default value: ENABLED.
    -  `KAconnIdleTime` is the duration (in seconds) for the connection to be idle, before sending a keep-alive (KA) probe. The minimum value you can set is 1 and the maximum is 4095.
    -  `kaprobeinterval` is the time internal (in seconds) before the next keep-alive (KA) probe, if the peer does not respond. The minimum value you can set is 1 and the maximum is 4095.

-  **bufferSize:** Specify the TCP buffer size, in bytes. The minimum value you can set is 8190 and the maximum is 20971520. By default the value is set to 8190.

    The following is a sample annotation of TCP profile to specify the TCP buffer size:

        ingress.citrix.com/frontend_tcpprofile: '{"bufferSize" : "8190"}

-  **MPTCP**: Enable MPTCP and set the optional MPTCP configuration. The following is a sample annotation of TCP profile to enable MPTCP and se the optional MPTCP configurations:

        ingress.citrix.com/frontend_tcpprofile: '{"mptcp" : "enabled", "mptcpDropDataOnPreEstSF":"enabled", "mptcpFastOpen": "enabled", "mptcpSessionTimeout":"7200"}

-  **flavor**: Set the TCP congestion control algorithm. Valid values are Default, BIC, CUBIC, Westwood, and Nile. By default the value is set to Default. The following is a sample annotation of TCP profile to set the TCP congestion control algorithm:

        ingress.citrix.com/frontend_tcpprofile: '{"flavor" : "westwood"}

-  **Dynamic receive buffering**: Enable or disable dynamic receive buffering. When enabled, it allows the receive buffer to be adjusted dynamically based on memory and network conditions. Possible values: ENABLED, DISABLED, and the Default value: DISABLED.

    >**Note:** The buffer size argument must be set for dynamic adjustments to take place.

        ingress.citrix.com/frontend_tcpprofile: '{"dynamicReceiveBuffering" : "enabled"}

## Defend TCP against spoofing attacks

You can enable the Ingress Citrix ADC to defend TCP against spoof attacks using the `rstWindowAttenuation` in TCP profiles. By default the `rstWindowAttenuation` parameter is disabled. This parameter is enabled to protect the Ingress Citrix ADC against spoofing. If you enable, it replies with corrective acknowledgment (ACK) for an invalid sequence number. Possible values are Enabled or Disabled.

The following is a sample annotation of TCP profile to enable `rstWindowAttenuation` on the Ingress Citrix ADC:

    ingress.citrix.com/frontend_tcpprofile: '{"rstwindowattenuate" : "enabled", "spoofSynDrop":"enabled"}
