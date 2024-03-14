# SSL profile

An [SSL profile](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ssl-profiles.html) is a collection of settings for SSL entities. It offers ease of configuration and flexibility. Instead of configuring the settings on each entity, you can configure them in a profile and bind the profile to all the entities that the settings apply to.

## Prerequisites

On the NetScaler, by default, SSL profile is not enable on the NetScaler. Ensure that you manually enable the SSL profile on the NetScaler. Enabling the SSL profile overrides all the existing SSL related setting on the NetScaler, for detailed information on SSL profiles, see [SSL profiles](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ssl-profiles.html).

SSL profiles are classified into two categories:

-  **Front end profiles**: containing parameters applicable to the front-end entity. That is, they apply to the entity that receives requests from a client.
-  **Back-end profiles**: containing parameters applicable to the back-end entity. That is, they apply to the entity that sends client requests to a server.

Once you enable SSL profiles on the NetScaler, a default front end profile (`ns_default_ssl_profile_frontend`) is applied to the SSL virtual server and a default back-end profile (`ns_default_ssl_profile_backend`) is applied to the service or service group on the NetScaler.

> **IMPORTANT:**
> SSL profile does not enable you to configure SSL certificate. For the SSL profile to work correctly, you must enable the default profile in NetScaler using the `set ssl parameter -defaultProfile ENABLED` command. Make sure that Citrix ingress controller is restarted after enabling default profile.
Set default SSL profile on NetScaler using the command `set ssl parameter -defaultProfile ENABLED` before deploying Citrix ingress controller. If you have already deployed Citrix ingress controller, then redeploy it. For more information about the SSL default profile, see [documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ssl-profiles/ssl-enabling-the-default-profile.html).

The Citrix ingress controller provides the following two smart annotations for SSL profile. You can use these annotations to customize the default front end profile (`ns_default_ssl_profile_frontend`) and back-end profile (`ns_default_ssl_profile_backend`) based on your requirement:

| Smart annotation | Description | Sample |
| ---------------- | ------------ | ----- |
| `ingress.citrix.com/frontend-sslprofile` | Use this annotation to create the front end SSL profile (**Client Plane**). The front end SSL profile is required only if you have enabled TLS on the Client Plane. | `ingress.citrix.com/frontend-sslprofile: '{"hsts":"enabled", "tls12" : "enabled"}'`  |
| `ingress.citrix.com/backend-sslprofile` | Use this annotation to create the back-end SSL profile (**Server Plane**). The SSL back end profile is required only if you use the [ingress.citrix.com/secure-backend](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/) annotation for the back-end. | `ingress.citrix.com/backend-sslprofile: '{"citrix-svc":{"hsts":"enabled", "tls1" : "enabled"}}'`  |

## Example: Using SSL Profile

This example shows how to apply SSL profiles.

            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              annotations:
                ingress.citrix.com/frontend-sslprofile: '{"hsts":"enabled", "tls13" : "enabled"}'
              name: ingress-ssl-profile
              namespace: netscaler
            spec:
              ingressClassName: netscaler
              rules:
              - host: example.com
                http:
                  paths:
                  - backend:
                      serviceName: service-test
                      servicePort: 80
                    path: /
              tls:
              - hosts:
                - example-test
                secretName: tls-secret
            ---
            apiVersion: networking.k8s.io/v1
            kind: IngressClass
            metadata:
              name: netscaler
            spec:
              controller: citrix.com/ingress-controller
            ---


## Example: Binding SSL cipher group

This example shows how to bind SSL cipher group to ingress.
For information on supported Ciphers on the NetScaler appliances, see [Ciphers available on the NetScaler appliances](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-adc-appliances.html).
For information about securing cipher, see [securing cipher](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/how-to/secure-ingress/#using-cipher-groups).

            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              annotations:
                ingress.citrix.com/frontend-sslprofile: '{"snienable": "enabled", "hsts":"enabled",
                  "tls13" : "enabled", "ciphers" : [{"ciphername": "test", "cipherpriority" :"1"}]}'
              name: ingress-ssl-cipher
              namespace: netscaler
            spec:
              ingressClassName: netscaler
              rules:
              - host: example.com
                http:
                  paths:
                  - backend:
                      serviceName: service-test
                      servicePort: 80
                    path: /
              tls:
              - hosts:
                - example-test
                secretName: tls-secret
            ---
            apiVersion: networking.k8s.io/v1
            kind: IngressClass
            metadata:
              name: netscaler
            spec:
              controller: citrix.com/ingress-controller
            ---
            

## Using built-in or existing user-defined SSL profiles on the NetScaler

You can use the individual smart annotations to configure the built-in profiles or existing user-defined profiles on the NetScaler for the front end and back-end configurations based on your requirement. For more information on default SSL profiles, see [Default SSL Profiles](https://docs.citrix.com/en-us/citrix-adc/13/ssl/ssl-profiles/ssl-appendix-b-default-frontend-backend-ssl-profile-settings.html).

For the front end configuration, you can provide the name of the built-in or existing user-defined profiles on the NetScaler. The following is a sample ingress annotation:

    ingress.citrix.com/frontend-sslprofile: "ssl_preconf_profile"

Where, 'ssl_preconf_profile' is the SSL profile that exists on the NetScaler.

For the back-end configuration, you must provide the name of the built-in or existing profile on the NetScaler and the back-end service name. The following is a sample ingress annotation:

    ingress.citrix.com/backend-sslprofile: '{"citrix-svc": "ssl_preconf_profile"}'

Where, 'ssl_preconf_profile' is the SSL profile that exists on the NetScaler and `citrix-svc` is the back-end service name.

**Sample SSL profile:**

    ingress.citrix.com/frontend-sslprofile: "ssl_preconf_profile"
    ingress.citrix.com/backend-sslprofile: '{"citrix-svc":"ssl_preconf_profile"}'

## Global front-end profile configuration using ConfigMap variables

If there is no front-end profiles annotation specified in any of the ingresses which share the front-end IP address, then the global values from the ConfigMap that is `FRONTEND_SSL_PROFILE` is used for the SSL front-end profiles respectively. The ConfigMap variable is used for the front-end profile if it is not overridden by front-end profiles smart annotation in one or more ingresses that shares a front-end IP address. If you need to enable or disable a feature using any front-end profile for all ingresses, you can use the variable `FRONTEND_SSL_PROFILE` for SSL profiles. For example, if you want to enable TLS 1.3 for all SSL ingresses, you can use `FRONTEND_SSL_PROFILE` to set this value instead of using the smart annotation in each ingress definition.
Refer [ConfigMap documentation](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/configure/profiles.md) to know how to use configmap with Citrix Ingress Controller.

### Configuration using FRONTEND_SSL_PROFILE

The `FRONTEND_SSL_PROFILE` variable is used for setting the SSL options for the front-end virtual server (client side) unless overridden by the `ingress.citrix.com/frontend-sslprofile` smart annotation in the ingress definition.

**Note:**
For the SSL profile to work correctly, you must enable the default profile in NetScaler using the `set ssl parameter -defaultProfile ENABLED` command. Make sure that Citrix ingress controller is restarted after enabling the default profile. The default profile is automatically enabled when NetScaler CPX is used as an ingress device. For more information about the SSL default profile, see the [SSL profile documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ssl-profiles/ssl-enabling-the-default-profile.html).

To use an existing profile on NetScaler or use a built-in SSL profile,

            apiVersion: v1
            kind: ConfigMap
            metadata:
            name: cic-configmap
            namespace: netscaler
            labels:
                app: citrix-ingress-controller
            data:
            FRONTEND_SSL_PROFILE: |
                preconfigured: my_ssl_profile

In this example, `my_ssl_profile` is the pre-existing SSL profile in NetScaler.

**Note:**
Default front end profile (`ns_default_ssl_profile_frontend`) is not supported using FRONTEND_SSL_PROFILE.preconfigured variable.

Alternatively, you can set the profile parameters as shown in the following example. See the [SSL profile NITRO documentation](https://developer-docs.citrix.com/projects/citrix-adm-nitro-api-reference/en/latest/configuration/instances/Citrix-ADC/ns_sslprofile/) for information on all possible key-values.

The following example shows binding SSL cipher groups to the SSL profile. The order is as specified in the list with the higher priority is provided to the first in the list and so on. You can use any SSL ciphers available in NetScaler or user-created cipher groups in this field. For information about the list of cyphers available in the NetScaler, see [Ciphers in NetScaler](https://docs.citrix.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-adc-appliances.html).

            apiVersion: v1
            kind: ConfigMap
            metadata:
            name: cic-configmap
            labels:
                app: citrix-ingress-controller
            data:
            FRONTEND_SSL_PROFILE: |
                config:
                tls13: 'ENABLED'
                ciphers:
                - TLS1.3-AES256-GCM-SHA384
                - TLS1.3-CHACHA20-POLY1305-SHA256