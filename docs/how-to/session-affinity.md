# Configure session affinity or persistence on the Ingress Citrix ADC

Session affinity or persistence settings on the Ingress Citrix ADC allows you to direct client requests to the same selected server regardless of which virtual server in the group receives the client request. When the configured time for persistence expires, any virtual server in the group is selected for the incoming client requests.

If persistence is configured, it overrides the load balancing methods once the server has been selected. It maintains the states of connections on the servers represented by that virtual server. The Citrix ADC then uses the configured load balancing method for the initial selection of a server, but forwards to that same server all subsequent requests from the same client.

The most commonly used persistence type is persistence based on cookies.

For more information, see [Configure session affinity or persistence on the Ingress Citrix ADC](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/how-to/session-affinity.html).