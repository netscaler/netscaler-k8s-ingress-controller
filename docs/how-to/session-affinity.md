# Configure session affinity or persistence on the Ingress Citrix ADC

Session affinity or persistence settings on the Ingress Citrix ADC allows you to direct client requests to the same selected server regardless of which virtual server in the group receives the client request. When the configured time for persistence expires, any virtual server in the group is selected for the incoming client requests.

If persistence is configured, it overrides the load balancing methods once the server has been selected. It maintains the states of connections on the servers represented by that virtual server. The Citrix ADC then uses the configured load balancing method for the initial selection of a server, but forwards to that same server all subsequent requests from the same client.

The most commonly used persistence type is persistence based on cookies.

## Configure persistence based on cookies

When you enable persistence based on cookies, the Citrix ADC adds an HTTP cookie into the `Set-Cookie` header field of the HTTP response. The cookie contains information about the service to which the HTTP requests must be sent. The client stores the cookie and includes it in all subsequent requests, and the ADC uses it to select the service for those requests.

The Citrix ADC inserts the cookie `<NSC_XXXX>= <ServiceIP> <ServicePort>`.

Where:

-  `<<NSC_XXXX>` is the virtual server ID that is derived from the virtual server name.
-  `<<ServiceIP>` is the hexadecimal value of the IP address of the service.
-  `<<ServicePort>` is the hexadecimal value of the port of the service.

The Citrix ADC encrypts `ServiceIP` and `ServicePort` when it inserts a cookie, and decrypts them when it receives a cookie.

For example, `a.com=ffffffff02091f1045525d5f4f58455e445a4a423660;expires=Fri, 23-Aug-2019 07:01:45`.

You can configure persistence setting on the ingress Citrix ADC, using the following Ingress annotation provided by the Citrix ingress controller:

    ingress.citrix.com/lbvserver: '{"apache":{"persistenceType":"COOKIEINSERT", "timeout":"20", "cookiename":"k8s_cookie"}}'

**Where**:

-  `timeout` specifies the duration of persistence. If session cookies are used with a `timeout` value of 0, no expiry time is specified by Citrix ADC regardless of the HTTP cookie version used. The session cookie expires when the Web browser is closed
-  `cookiename` specifies the name of cookie with a maximum of 32 characters. If not specified, cookie name is internally generated.
-  `persistenceType` here specifies the type of persistence to be used, `COOKIEINSERT` is used to cookie based persistence. Apart from cookie, other options can also be used along with appropriate arguments and other required parameters.

**Possible values are**: SOURCEIP, SSLSESSION, DESTIP, SRCIPDESTIP, and so on.

### Source IP address persistence

When source IP persistence is configured on the Ingress Citrix ADC, you can set persistence to an load balancing virtual server, that creating a stickiness for the subsequest requests from the same client.

The following is a sample Ingress annotation to configure source IP address persistence:

    ingress.citrix.com/lbvserver: '{"apache":{"persistenceType":"SOURCEIP", "timeout":"10"}}'

### SSL session ID persistence

When SSL session ID persistence is configured, the Citrix ADC appliance uses the SSL session ID, which is part of the SSL handshake process, to create a persistence session before the initial request is directed to a service. The load balancing virtual server directs subsequent requests that have the same SSL session ID to the same service. This type of persistence is used for SSL bridge services.

The following is a sample Ingress annotation to configure SSL session ID persistence:

    ingress.citrix.com/lbvserver: '{"apache":{"persistenceType":"SSLSESSION"}}'

### Destination IP address-based persistence

In this type of persistence, when the Ingress Citrix ADC receives a request from a new client, it creates a persistence session based on the IP address of the service selected by the virtual server (the destination IP address). Subsequently, it directs requests to the same destination IP to the same service. This type of persistence is used with link load balancing.

The following is a sample Ingress annotation to configure destination IP address-based persistence:

    ingress.citrix.com/lbvserver: '{"apache":{"persistenceType":"DESTIP"}}'

### Source and destination IP address-based persistence

In this type of persistence, when the Citrix ADC appliance receives a request, it creates a persistence session based on both the IP address of the client (the source IP address) and the IP address of the service selected by the virtual server (the destination IP address). Subsequently, it directs requests from the same source IP and to the same destination IP to the same service.

The following is a sample Ingress annotation to configure source and destination IP address-based persistence:

    ingress.citrix.com/lbvserver: '{"apache":{"persistenceType":"SRCIPDESTIP"}}'