# Securing Ingress

The topic covers the various ways to secure your Ingress using Citrix ADC and the annotations provided by the Citrix ingress controller.

The following table lists the TLS use cases with sample annotations that you can use to secure your Ingress using the Ingress Citrix ADC and the Citrix ingress controller:

| Use cases | Sample annotations |
| --------- | ------------------ |
| [Enable TLSv1.3 protocol](#enable-tlsv13-protocol) | `ingress.citrix.com/frontend-sslprofile: '{"tls13":"enabled", "tls13sessionticketsperauthcontext":"1", "dhekeyexchangewithpsk":"yes"}'`|
| [HTTP strict transport security (HSTS)](#http-strict-transport-security-hsts) | `ingress.citrix.com/frontend-sslprofile: '{"hsts":"enabled", "maxage" : "157680000", "includesubdomain":"yes"}` |
| [OCSP stapling](#ocsp-stapling) | `ingress.citrix.com/frontend-sslprofile: '{"ocspstapling":"enabled"}'` |
| [Set client authentication to mandatory](#set-client-authentication-to-mandatory) | `ingress.citrix.com/frontend-sslprofile: '{"clientauth":"enabled", "clientcert" : "mandatory"}'`|
| [TLS session ticket extension](#tls-session-ticket-extension) | `ingress.citrix.com/frontend-sslprofile: '{"sessionticket" : "enabled", "sessionticketlifetime : "300"}'` |
| [SSL session reuse](#ssl-session-reuse) | `ingress.citrix.com/frontend-sslprofile: '{"sessreuse" : "enabled", "sesstimeout : "120"}'` |
| [Cipher groups](#using-cipher-groups) | `ingress.citrix.com/frontend-sslprofile:'{"snienable": "enabled", "ciphers" : [{"ciphername": "secure", "cipherpriority" :"1"}, {"ciphername": "SECURE", "cipherpriority" :"21"}]}'` |
| [Cipher redirect](#using-cipher-rediect) | `ingress.citrix.com/frontend-sslprofile:'{"snienable": "enabled", "ciphers" : [{"ciphername": "secure", "cipherpriority" :"1"}], "cipherredirect":"enabled", "cipherurl": "https://redirecturl"}'` |

## Enable TLS v1.3 protocol

Using the annotations for SSL profiles, you can enable TLS 1.3 protocol support on the SSL profile and set the  `tls13SessionTicketsPerAuthContext` and `dheKeyExchangeWithPsk` parameters in the SSL profile for the Ingress Citrix ADC.

The `tls13SessionTicketsPerAuthContext` parameter enables you to set the number of tickets the Ingress Citrix ADC issues anytime TLS 1.3 is negotiated, ticket-based resumption is enabled, and either a handshake completes or post-handhsake client authentication completes. The value can be increased to enable clients to open multiple parallel connections using a fresh ticket for each connection. The minimum value you can set is 1 and the maximum is 10. By default, the value is set to 1.

>Note: No tickets are sent if resumption is disabled.

The `dheKeyExchangeWithPsk` parameter allows you to specify whether the **Ingress Citrix ADC requires a DHE** key exchange to occur when a preshared key is accepted during a TLS 1.3 session resumption handshake. A DHE key exchange ensures forward secrecy, even if ticket keys are compromised, at the expense of extra resources required to carry out the **DHE** key exchange.

The following is a sample annotation for the HTTP profile to enable TLS 1.3 protocol support on SSL profile and set the  `tls13SessionTicketsPerAuthContext` and `dheKeyExchangeWithPsk` parameters in the SSL profile.

    ingress.citrix.com/frontend-sslprofile: '{"tls13":"ENABLED", "tls13sessionTicketsPerAuthContext":"1", "dheKeyExchangeWithPsk":"yes"}'

## HTTP strict transport security (HSTS)

The Ingress Citrix ADC appliances support HTTP strict transport security (HSTS) as an inbuilt option in SSL profiles. Using HSTS, a server can enforce the use of an HTTPS connection for all communication with a client. That is, the site can be accessed only by using HTTPS. Support for HSTS is required for A+ certification from SSL Labs. For more information, see [Citrix ADC support for HSTS](https://docs.citrix.com/en-us/citrix-adc/13/ssl/how-to-articles/ssl-support-for-hsts.html).

Using the annotations for SSL profiles, you can enable HSTS in an SSL front-end profile on the Ingress Citrix ADC. The following is a sample ingress annotation:

    ingress.citrix.com/frontend-sslprofile: '{"HSTS":"enabled", "maxage" : "157680000", "IncludeSubdomain":"yes"}'

Where:

-  `HSTS` - The state of HTTP Strict Transport Security (HSTS) on the SSL profile. Using HSTS, a server can enforce the use of an HTTPS connection for all communication with a client. The supported values are ENABLED and DISABLED. By default, the value is set to DISABLED.
-  `maxage` - Allows you to set the maximum time, in seconds, in the strict transport security (STS) header during which the client must send only HTTPS requests to the server. The minimum time you can set is 0 and the maximum is 4294967294. By default the value is to 0.
-  `IncludeSubdomains` - Allows you to enable HSTS for subdomains. If set to `Yes`, a client must send only HTTPS requests for subdomains. By default the value is set to No.

## OCSP stapling

The Ingress Citrix ADC can send the revocation status of a server certificate to a client, at the time of the SSL handshake, after validating the certificate status from an OCSP responder. The revocation status of a server certificate is “stapled” to the response the appliance sends to the client as part of the SSL handshake. For more information on Citrix ADC implementation of CRL and OCSP reports, see [OCSP stapling](https://docs.citrix.com/en-us/citrix-adc/12-1/ssl/ssl-11-1-ocsp-stapling-solution.html).

To use the OCSP stapling feature, you can enable it using an SSL profile with the following ingress annotation:

    ingress.citrix.com/frontend-sslprofile: '{"ocspStapling":"ENABLED"}'

>**IMPORTANT:**
>To use OCSP stapling you must add an OCSP responder on the Citrix ADC appliance.

## Set Client authentication to mandatory

Using the annotations for SSL profiles, you can enable client authentication, the Ingress Citrix ADC appliance asks for the client certificate during the SSL handshake.

The appliance checks the certificate presented by the client for normal constraints, such as the issuer signature and expiration date.

Here are some use cases:

-  Require a valid client certificate before website content is displayed. This restricts website content to only authorized machines and users.

-  Request a valid client certificate. If a valid client certificate is not provided, then prompt the user for multifactor authentication.

Client authentication can be set to mandatory, or optional.

-  When it is set as mandatory, if the SSL Client does not transmit a valid Client Certificate, then the connection is dropped. Valid means: signed/issued by a specific Certificate Authority, and not expired or revoked.
-  When it is optional, then the Citrix ADC requests the client certificate, but proceeds with the SSL transaction even if the client presents an invalid certificate or no certificate. This configuration is useful for authentication scenarios (for example require two-factor authentication if a valid Client Certificate is not provided)

Using the annotations for SSL profiles, you can enable client authentication on an SSL virtual server and set client authentication as **Mandatory**.

The following is a sample annotation of the SSL profile:

    ingress.citrix.com/frontend-sslprofile: '{"clientauth":"ENABLED", "clientcert" : "Mandatory"}'

>**Note:**
> Make sure that you bind the client-certificate to the SSL virtual server on the Ingress Citrix ADC.

## TLS session ticket extension

An SSL handshake is a CPU-intensive operation. If session reuse is enabled, the server or client key exchange operation is skipped for existing clients. They are allowed to resume their sessions. This improves the response time and increases the number of SSL transactions per second that a server can support. However, the server must store details of each session state, which consumes memory and is difficult to share among multiple servers if requests are load balanced across servers.

The Ingress Citrix ADC appliances support the SessionTicket TLS extension. Use of this extension indicates that the session details are stored on the client instead of on the server. The client must indicate that it supports this mechanism by including the session ticket TLS extension in the client Hello message. For new clients, this extension is empty. The server sends a new session ticket in the NewSessionTicket handshake message. The session ticket is encrypted by using a key-pair known only to the server. If a server cannot issue a new ticket currently, it completes a regular handshake.

Using the annotations for SSL profiles, you can enable the use of session tickets, as per the RFC 5077. Also, you can set the life time of the session tickets issued by the Ingress Citrix ADC, using the `sessionticketlifetime` parameter.

The following is the sample ingress annotation:

    ingress.citrix.com/frontend-sslprofile: '{"sessionticket" : "ENABLED", "sessionticketlifetime : "300"}'

## SSL session reuse

You can reuse an existing SSL session on a Citrix ADC appliance. While the SSL renegotiation process consists of a full SSL handshake, the SSL reuse consists of a partial handshake because the client sends the SSL ID with the request.

Using the annotations for SSL profiles, you can enable session reuse and also set the session timeout value (in seconds) on the Ingress Citrix ADC.

The following is the sample ingress annotation:

    ingress.citrix.com/frontend-sslprofile: '{"sessreuse" : "ENABLED", "sesstimeout : "120"}'

By default, the session reuse option is enabled on the appliance and the timeout value for the same is set to 120 seconds. Therefore, if a client sends a request on another TCP connection and the earlier SSL session ID within 120 seconds, then the appliance performs a partial handshake.

## Using cipher groups

The Ingress Citrix ADC ships with [built-in cipher groups](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ciphers-available-on-the-citrix-ADC-appliances.html). To use ciphers that are not part of the DEFAULT cipher group, you have to explicitly bind them to an SSL profile. You can also [create a user-defined cipher group](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ciphers-available-on-the-citrix-ADC-appliances/configure-user-defined-cipher-groups-on-the-adc-appliance.html) to bind to the SSL virtual server on the Ingress Citrix ADC.

The built-in cipher groups can be used in Tier-1 and Tier-2 Citrix ADC, and the user-defined cipher group can be used only in Tier-1 Citrix ADC.

To use a user-defined cipher group, ensure that the Citrix ADC has a user-defined cipher group. Perform the following:

1.  Create a user-defined cipher group. For example, `testgroup`.
2.  Bind all the required ciphers to the user-defined cipher group.
3.  Note down the user-defined cipher group name.

For detailed instructions, see [Configure a user-defined cipher group](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ciphers-available-on-the-citrix-ADC-appliances/configure-user-defined-cipher-groups-on-the-adc-appliance.html#configure-a-user-defined-cipher-group-by-using-the-cli).

Using the annotations for SSL profiles, you can bind the built-in cipher groups, a user-defined cipher group or both to the SSL profile.

The following is the syntax of the ingress annotation that you can use to bind the built-in cipher groups and a user-defined cipher group to an SSL profile:

    ingress.citrix.com/frontend-sslprofile:'{"sni":"enabled", "ciphers" : [{"ciphername": "SECURE", "cipherpriority" :"1"}, {"ciphername": "testgroup", "cipherpriority" :"2"}]}'

The ingress annotation binds the built-in cipher group, `SECURE`, and the user-defined cipher group, `testgroup`, to the SSL profile.

## Using cipher redirect

During the SSL handshake, the SSL client (usually a web browser) announces the suite of ciphers that it supports, in the configured order of cipher preference. From that list, the SSL server then selects a cipher that matches its own list of configured ciphers.

If the ciphers announced by the client does not match those ciphers configured on the SSL server, the SSL handshake fails. The failure is announced by a cryptic error message displayed in the browser. These messages rarely mention the exact cause of the error.

With cipher redirection, you can configure an SSL virtual server to deliver accurate, meaningful error messages when an SSL handshake fails. When the SSL handshake fails, the Citrix ADC appliance redirects the user to a previously configured URL or, if no URL is configured, displays an internally generated error page.

The following is the syntax of the ingress annotation that you can use to bind cipher groups and enable cipher redirect to redirect the request to `redirecturl`.

| [Cipher redirect](#using-cipher-rediect) | `ingress.citrix.com/frontend-sslprofile:'{"snienable": "enabled", "ciphers" : [{"ciphername": "secure", "cipherpriority" :"1"}], "cipherredirect":"enabled", "cipherurl": "https://redirecturl"}'` |