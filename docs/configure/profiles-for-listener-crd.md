# Profile support for the Listener CRD

You can use individual entities such as [HTTP profile](https://docs.citrix.com/en-us/citrix-adc/current-release/system/http-configurations.html#sample-http-configurations), [TCP profile](https://docs.citrix.com/en-us/citrix-adc/current-release/system/tcp-configurations.html), and [SSL profile](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ssl-profiles.html) to configure HTTP, TCP, and SSL respectively for the Listener CRD. Profile support for the Listener CRD helps you to customize the default protocol behavior. You can also select the SSL ciphers for the SSL virtual server.

## HTTP profile

An [HTTP profile](https://docs.citrix.com/en-us/citrix-adc/current-release/system/http-configurations.html#sample-http-configurations) is a collection of HTTP settings. A default HTTP profile called `nshttp_default_profile` is configured to set the HTTP configurations. These configurations are applied, by default, globally to all services and virtual servers. You can customize the HTTP configurations for a Listener resource by specifying `spec.policies.httpprofile`. If specified, Citrix ingress controller creates a new HTTP profile with the default values derived from the default HTTP profile and configures the values specified.

It helps to derive the default values from the default HTTP profile and configures the values specified.

The following example YAML shows how to enable websocket for a given front-end virtual server.

```yml
    apiVersion: citrix.com/v1
    kind: Listener
    metadata:
      name: test-listener
      namespace: default
    spec:
      vip: x.x.x.x
      port: 80
      protocol: http
      policies:
        httpprofile:
          config:
            websocket: "ENABLED"
```
For information about all the possible key-value pairs for the HTTP profile see, [HTTP profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ns/nshttpprofile/).

**Note:** The ‘name’ is auto-generated.

You can also specify a built-in HTTP profile or a pre-configured HTTP profile and bind it to the front-end virtual server as shown in the following example.

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: x.x.x.x
  port: 80
  protocol: http
  policies:
    httpprofile:
      preconfigured: 'nshttp_default_strict_validation'
```

## TCP profile

A TCP profile is a collection of TCP settings. A default TCP profile called `nstcp_default_profile` is configured to set the TCP configurations. These configurations are applied, by default, globally to all services and virtual servers. You can customize the TCP settings by specifying `spec.policies.tcpprofile`. When you specify `spec.policies.tcpprofile`, Citrix ingress controller creates a TCP profile that is derived from the default TCP profile and applies the values provided in the specification, and binds it to the front-end virtual server.

For information about all the possible key-value pairs for a TCP profile, see [TCP profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ns/nstcpprofile/).

**Note:** The name is auto-generated.

The following example shows how to enable `tcpfastopen` and `HyStart` for the front-end virtual server.

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: x.x.x.x
  port: 80
  protocol: http
  policies:
    tcpprofile:
      config:
        tcpfastopen: "ENABLED"
        hystart: "ENABLED"
```
You can also specify a built-in TCP profile or a pre-configured TCP profile name as shown in the following example:

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: x.x.x.x
  port: 80
  protocol: http
  policies:
    tcpprofile:
      preconfigured: 'nstcp_default_Mobile_profile'
```

## SSL profile

An SSL profile is a collection of settings for SSL entities. SSL profile makes configuration easier and flexible. You can configure the settings in a profile and bind that profile to a virtual server instead of configuring the settings on each entity. An SSL profile allows you to customize many SSL parameters such as TLS protocol and ciphers. For more information about SSL profile, see [SSL profile infrastructure](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ssl-profiles/ssl-enabling-the-default-profile.html).

**Note:** By default, Citrix ADC creates a legacy SSL profile. The legacy SSL profile has many drawbacks including non-support for advanced protocols such as SSLv3. Hence, it is recommended to enable the default SSL profiles in Citrix ADC before Citrix ingress controller is launched.

To enable the advanced SSL profile, use the following command in the Citrix ADC command line:

    set ssl parameter -defaultProfile ENABLED

The command enables the default SSL profile for all the existing SSL virtual servers and the SSL service groups.

You can specify `spec.policies.sslprofile` to customize the SSL profile. When specified, Citrix ingress controller creates an SSL profile derived from the default SSL front-end profile: `ns_default_ssl_profile_frontend`.

For information about key-value pairs supported in the SSL profile, see [SSL profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/ssl/ssl/).

**Note:** The ‘name’ is auto-generated.

The following example shows how to enable TLS1.3 and HSTS for the front-end virtual server.

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: x.x.x.x
  port: 443
  certificates:
  - secret:
      name: my-cert
  protocol: https
  policies:
    sslprofile:
      config:
        tls13: "ENABLED"
        hsts: "ENABLED"

```

You can specify a built-in or pre-configured SSL profile name as shown in the following example:

```yml
apiVersion: citrix.com/v1
kind: Listener
metadata:
  name: test-listener
  namespace: default
spec:
  vip: x.x.x.x
  port: 443
  certificates:
  - secret:
      name: my-cert
  protocol: https
  policies:
    sslprofile:
      preconfigured: 'ns_default_ssl_profile_secure_frontend'
```

## SSL ciphers

The Ingress Citrix ADC has [built-in cipher groups](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-ADC-appliances.html). By default, virtual servers use a DEFAULT cipher group for an SSL transaction. To use ciphers which are not part of the DEFAULT cipher group, you must explicitly bind them to an SSL profile. You can use `spec.policies.sslciphers` to provide a list of ciphers, list of [built-in cipher groups](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-ADC-appliances.html), or the list of [user-defined cipher groups](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-ADC-appliances/configure-user-defined-cipher-groups-on-the-adc-appliance.html). 

**Note:** The order of priority of ciphers is the same order defined in the list. The first one in the list gets the first priority and likewise.

The following example shows how to provide a list of built-in cipher suites.

```yml
  apiVersion: citrix.com/v1
  kind: Listener
  metadata:
    name: test-listener
    namespace: default
  spec:
    vip: x.x.x.x
    port: 443
    certificates:
    - secret:
        name: my-cert
    protocol: https
    policies:
      sslciphers:
      - 'TLS1.2-ECDHE-RSA-AES128-GCM-SHA256'
      - 'TLS1.2-ECDHE-RSA-AES256-GCM-SHA384'
      - 'TLS1.2-ECDHE-RSA-AES-128-SHA256'
      - 'TLS1.2-ECDHE-RSA-AES-256-SHA384'
```

For information about the list of cipher suites available in Citrix ADC, see [SSL profile infrastructure](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-adc-appliances.html).

Ensure that Citrix ADC has a user-defined cipher group for using a user-defined cipher group. Perform the following steps to configure a user-defined cipher group: 

1.	Create a user-defined cipher group. For example, `MY-CUSTOM-GROUP`.
2.	Bind all the required ciphers to the user-defined cipher group.
3.	Note down the user-defined cipher group name.

For detailed instructions, see [Configure a user-defined cipher group](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-ADC-appliances/configure-user-defined-cipher-groups-on-the-adc-appliance.html#configure-a-user-defined-cipher-group-by-using-the-cli).

**Note:** The order of priority of ciphers is the same order defined in the list. The first one in the list gets the first priority and likewise.

The following example shows how to provide a list of built-in cipher groups and/or user defined cipher group. The user-defined cipher groups must be present in Citrix ADC before you apply it to Listener.

```yml
  apiVersion: citrix.com/v1
  kind: Listener
  metadata:
    name: test-listener
    namespace: default
  spec:
    vip: x.x.x.x
    port: 443
    certificates:
    - secret:
        name: my-cert
    protocol: https
    policies:
      sslciphers:
      - 'SECURE'
      - 'HIGH'
      - 'MY-CUSTOM-CIPHERS'
```

In the preceding example, `SECURE` and `HIGH` are built-in cipher groups in Citrix ADC. `MY-CUSTOM-CIPHERS` is the pre-configured user-defined cipher groups. 

**Note:** If you have specified the pre-configured SSL profile, you must bind the ciphers manually through Citrix ADC and `spec.policies.sslciphers` is not applied on the pre-configured SSL profile.

**Note:** The built-in cipher groups can be used in Tier-1 and Tier-2 Citrix ADC. The user-defined cipher group can be used only in a Tier-1 Citrix ADC.

## Analytics profile

Analytics profile enables Citrix ADC to export the type of transactions or data to an external platform. If you are using [Citrix ADC Observability Exporter](https://github.com/citrix/citrix-observability-exporter) to collect metrics and transactions data and export it to endpoints such Elasticsearch or Prometheus, you can configure the analytics profile to select the type of data that needs to be exported.

**Note:** For the Analytics profile to be functional, you must configure the Citrix ADC Observability Exporter. [Analytics configuration support using ConfigMap](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map-coe/#:~:text=You%20can%20use%20Citrix%20Observability,the%20Citrix%20ingress%20controller%20configuration).

The following example shows how to enable `webinsight` and `tcpinsight` in the analytics profile. 

```yml
apiVersion: citrix.com/v1
  kind: Listener
  metadata:
    name: test-listener
    namespace: default
  spec:
    vip: x.x.x.x
    port: 443
    certificates:
    - secret:
        name: my-cert
    protocol: https
    policies:
     analyticsprofile:
       config:
       - type: webinsight
       - type: tcpinsight
```

The following example shows how to select the additional parameters for the type of `webinsight` which you want to be exported to Citrix ADC Observability Exporter. For information about the valid key-value pair, see [Analytics Profile](https://developer-docs.citrix.com/projects/citrix-adc-nitro-api-reference/en/latest/configuration/analytics/analyticsprofile/).

```yml
apiVersion: citrix.com/v1
  kind: Listener
  metadata:
    name: test-listener
    namespace: default
  spec:
    vip: x.x.x.x
    port: 443
    certificates:
    - secret:
        name: my-cert
    protocol: https
    policies:
     analyticsprofile:
       config:
       - type: webinsight
         parameters:
           httpdomainname: "ENABLED"
           httplocation: "ENABLED"
```

The following example shows how to use pre-configured analytics profiles.

```yml
  apiVersion: citrix.com/v1
  kind: Listener
  metadata:
    name: test-listener
    namespace: default
  spec:
    vip: x.x.x.x
    port: 443
    certificates:
    - secret:
        name: my-cert
    protocol: https
    policies:
     analyticsprofile:
       preconfigured:
       - 'custom-websingiht-analytics-profile'
       - 'custom-tcpinsight-analytics-profile'
```