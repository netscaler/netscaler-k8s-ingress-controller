# Define authentication and authorization policies on the Ingress Citrix ADC

Authentication and authorization policies are used to enforce access restrictions to the resources hosted by an application or API server. While you can verify the identity using the authentication policies, authorization policies are used to verify whether a specified request has the necessary permissions to access a resource.

Citrix provides a Kubernetes [CustomResourceDefinition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRD) called the **Auth CRD** that you can use with the Citrix ingress controller to define authentication policies on the ingress Citrix ADC.

## Auth CRD definition

The Auth CRD is available in the Citrix ingress controller GitHub repo at: [auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml). The Auth CRD provides [attributes](#auth-crd-attributes) for the various options that are required to define the authentication policies on the Ingress Citrix ADC.

## Auth CRD attributes

The Auth CRD provides the following attributes that you use to define the authentication policies:

-  `servicenames`
-  `authentication_mechanism`
-  `authentication_providers`
-  `authentication_policies`
-  `authorization_policies`
  
### Servicenames

The name of the services for which the authentication and authorization policies need to be applied.

### Authentication mechanism

The following authentication mechanisms are supported:

- Using request headers:  
Enables user authentication using the request header. You can use this mechanism when the credentials or API keys are passed in a header (typically Authorization header). For example, you can use authentication using request headers for basic, digest, bearer authentication, or API keys.

- Using forms:
You can use this mechanism with user or web authentication including the relying party configuration for OpenID connect and the service provider configuration for SAML.

When the authentication mechanism is not specified, the default is authentication using the request header.

The following are the attributes for forms based authentication.

| Attribute | Description |
| --------- | ----------- |
| `authentication_host` | Specifies a fully qualified domain name (FQDN) to which the user must be redirected for ADC authentication service. This FQDN should be unique and should resolve to the front-end IP address of Citrix ADC with Ingress/service type LoadBalancer or the VIP address of the Listener CRD.|
| `authentication_host_cert` | Specifies the name of the SSL certificate to be used with the `authentication_host`. This certificate is mandatory while performing authentication using the form.|
|`ingress_name`| Specifies the Ingress name for which the authentication using forms is applicable.|
| `lb_service_name`| Specifies the name of the service of type LoadBalancer for which the authentication using forms is applicable.|
|`listener_name`| The name of the Listener CRD for which the authentication using forms is applicable.|
| `vip` |Specifies the front-end IP address of the Ingress for which the authentication using forms is applicable. This attribute refers to the `frontend-ip` address provided with the Ingress. If there is more than one Ingress resource which uses the same frontend-ip, it is recommended to use vip.|

**Note:** While using forms, authentication can be enabled for all types of traffic. Currently, granular authentication is not supported.

### Authentication providers

The **providers** define the authentication mechanism and parameters that are required for the authentication mechanism. 

#### Basic authentication

Specifies that local authentication is used with the HTTP basic authentication scheme. To use basic authentication, you must create user accounts on the ingress Citrix ADC.

#### OAuth authentication

The OAuth authentication mechanism, requires an external identity provider to authenticate the client using oAuth2 and issue an Access token. When the client presents the Access token to a Citrix ADC as an access credential, the Citrix ADC validates the token using the configured values. If the token validation is successful then Citrix ADC grants access to the client.

##### OAuth authentication attributes

The following are the attributes for OAuth authentication:

| Attribute | Description |
| --------- | ----------- |
| `Issuer` | The identity (usually a URL) of the server whose tokens need to be accepted for authentication.|
| `jwks_uri` | The URL of the endpoint that contains JWKs (JSON Web Key) for JWT (JSON Web Token) verification.|
| `audience` | The identity of the service or application for which the token is applicable.|
| `token_in_hdr` | The custom header name where the token is present. The default value is the `Authorization` header.</br> **Note:** You can specify more than one header.|
| `token_in_param` | The query parameter where the token is present.|
|`signature_algorithms`| Specifies the list of signature algorithms which are allowed. By default HS256, RS256, and RS512 algorithms are allowed.|
| `introspect_url`| The URL of the introspection endpoint of the authentication server (IdP). If the access token presented is an opaque token, introspection is used for the token verification.|
| `client_credentials`| The name of the Kubernetes secrets object that contains the client id and client secret required to authenticate with the authentication server.|
| `claims_to_save`| The list of claims to be saved. Claims are used to create authorization policies.|

OpenID Connect (OIDC) is a simple identity layer on top of the OAuth 2.0 protocol. OIDC allows clients to verify the identity of the end-user based on the authentication performed by an authorization server, as well as to obtain basic profile information about the end-user. In addition to the OAuth attributes, you can use the following attributes to configure OIDC.

| Attribute | Description |
| --------- | ----------- |
| `metadata_url` | Specifies the URL that is used to get OAUTH or OIDC provider metadata.|
| `user_field` | Specifies the attribute in the token from which the user name should be extracted. By default, Citrix ADC examines the email attribute for user ID.|
| `default_group` | Specifies the group assigned to the request if authentication succeeds. This group is in addition to any extracted groups from the token. |
| `grant_type` | Specifies the type of flow to the token end point. The default value is `CODE`.|
| `pkce` | Specifies whether to enable Proof Key for Code Exchange (PKCE). The default value is `ENABLED`.|
| `token_ep_auth_method` | Specifies the authentication method to be used with the token end point. The default value is `client_secret_post`.|

#### SAML authentication

Security assertion markup language (SAML) is an XML-based open standard which enables authentication of users across products or organizations. The SAML authentication mechanism, requires an external identity provider to authenticate the client. SAML works by transferring the client identity from the identity provider to the Citrix ADC. On successful validation of the client identity, the Citrix ADC grants access to the client.

The following are the attributes for SAML authentication.

| Attribute | Description |
| --------- | ----------- |
| `metadata_url` | Specifies the URL used for obtaining SAML metadata. |
| `metadata_refresh_interval` | Specifies the interval in minutes for fetching metadata from the specified metadata URL.|
| `signing_cert` | Specifies the SSL certificate to sign requests from the service provider (SP) to the identity provider (IdP).|
| `audience` | Specifies the identity of the service or application for which the token is applicable.|
| `issuer_name` | Specifies the name used in requests sent from SP to IdP to identify the Citrix ADC.|
| `binding` | Specifies the transport mechanism of the SAML message. The default value is `POST`.|
| `artifact_resolution_service_url` | Specifies the URL of the artifact resolution service on IdP.|
| `logout_binding` | Specifies the transport mechanism of the SAML logout. The default value is `POST`.|
|`reject_unsigned_assertion`| Rejects unsigned SAML assertions. If this value is `ON`, it rejects assertion without signature.|
|`user_field`| Specifies the SAML user ID specified in the SAML assertion|
|`default_authentication_group`| Specifies the default group that is chosen when the authentication succeeds in addition to extracted groups.|
|`skewtime`| Specifies the allowed clock skew time in minutes on an incoming SAML assertion.|
|`attributes_to_save`| Specifies the list of attribute names separated by commas which needs to be extracted and stored as key-value pairs for the session on Citrix ADC.|

#### LDAP authentication

LDAP (Lightweight Directory Access Protocol) is an open, vendor-neutral, industry standard application protocol for accessing and maintaining distributed directory information services over an Internet Protocol (IP) network. A common use of LDAP is to provide a central place to store user names and passwords. LDAP allows many different applications and services to connect to the LDAP server to validate users.

**Note:** LDAP authentication is supported through both the authentication mechanisms using the request header or using forms.

The following are the attributes for LDAP authentication.

| Attribute | Description |
| --------- | ----------- |
| `server_ip` | Specifies the IP address assigned to the LDAP server. |
| `server_name` | Specifies the LDAP server name as an FQDN.|
| `server_port` | Specifies the port on which the LDAP server accepts connections. The default value is 389.|
| `base` | Specifies the base node on which to start LDAP searches. If the LDAP server is running locally, the default value of base is `dc=netscaler`, `dc=com`.|
| `server_login_credentials` | Specifies the Kubernetes secret object providing credentials to log in to the LDAP server. The secret data should have user name and password.|
| `login_name` | Specifies the **LDAP login name** attribute. The Citrix ADC uses the LDAP login name to query external LDAP servers or Active Directories.|
| `security_type` | Specifies the type of security used for communications between the Citrix ADC and the LDAP server. The default is TLS.|
| `validate_server_cert` | Validates LDAP server certificates. The default value is `NO`.|
|`hostname`|Specifies the host name for the LDAP server. If `validate_server_cert` is `ON`, this value must be the host name on the certificate from the LDAP. A host name mismatch causes a connection failure.|
|`sub_attribute_name`| Specifies the LDAP group subattribute name. This attribute is used for group extraction from the LDAP server.|
|`group_attribute_name`| Specifies the LDAP group attribute name. This attribute is used for group extraction on the LDAP server.|
|`search_filter`| Specifies the string to be combined with the default LDAP user search string to form the search value. For example, if the search filter "vpnallowed=true" is combined with the LDAP login name "samaccount" and the user-supplied user name is "bob", the result is the LDAP search string ""(&(vpnallowed=true)(samaccount=bob)"". Enclose the search string in two sets of double quotation marks.|
|`auth_timeout`| Specifies the number of seconds the Citrix ADC waits for a response from the server. The default value is 3.|
|`password_change`|Allows password change requests. The default value is `DISABLED`. |
|`attributes_to_save`| List of attribute names separated by comma which needs to be fetched from the LDAP server and stored as key-value pairs for the session on Citrix ADC. |

### Authentication policies

The **authentication_policies** allow you to define the traffic selection criteria to apply the authentication mechanism and also to specify the provider that you want to use for the selected traffic.

The following are the attributes for policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. </br>**Note:** The traffic is selected if the incoming request URI matches with any of the paths AND any of the listed methods. If the method is not specified then the path alone is used for the traffic selection criteria.|
| `provider` | Specifies the authentication mechanism that needs to be used. If the authentication mechanism is not provided, then authentication is not performed.|

**Note:** If you want to skip authentication for a specific end point, create a policy with the `provider` attribute set as empty list. Otherwise, the request is denied. 

### Authorization policies

Authorization policies allow you to define the traffic selection criteria to apply the authorization requirements for the selected traffic.

The following are the attributes for authorization policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. |
| `claims` | Specifies the claims required to access a specific API endpoint. `name` indicates the claim name and `values` indicate the required permissions. You can have more than one claim. If an empty list is specified, it implies that authorization is not required. </br> **Note:** Any claim that needs to be used for authorization, should be saved as part of authentication.|

**Note:** Citrix ADC requires both authentication and authorization policies for the API traffic. Therefore, you must configure an authorization policy with an authentication policy. Even if you do not have any authorization checks, you must create an authorization policy with empty claims. Otherwise, the request is denied with a 403 error.

**Note:** Authorization would be successful if the incoming request matches a policy (path, method, and claims). All policies are tried until there is a match. If it is required to selectively bypass authorization for a specific end point, an explicit policy needs to be created.

## Deploy the Auth CRD

Perform the following to deploy the Auth CRD:

1.  Download the CRD ([auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml)).

2.  Deploy the Auth CRD using the following command:

        kubectl create -f auth-crd.yaml

    For example:

        root@master:~# kubectl create -f auth-crd.yaml

        customresourcedefinition.apiextensions.k8s.io/authpolicies.citrix.com created

## How to write authentication and authorization policies

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the authentication policy configuration in a `.yaml` file. In the `.yaml` file, use `authpolicy` in the `kind` field and in the `spec` section add the **Auth CRD** attributes based on your requirement for the policy configuration.

After you deploy the `.yaml` file, the Citrix ingress controller applies the authentication policy configuration on the Ingress Citrix ADC device.

### Local auth provider

The following is a sample authentication and authorization policy definition for the local-auth-provider type ([local_auth.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/local_auth.yaml)).

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: authexample
spec:
    servicenames:
    - frontend

    authentication_providers:
        - name: "local-auth-provider"
          basic-local-db:

    authentication_policies:
        - resource:
            path:
              - '/orders/'
              - '/shipping/'
            method: [GET, POST]
          provider: ["local-auth-provider"]
        
        # skip authentication for this
        - resource:
            path:
              - '/products/'
            method: [GET]
          provider: []

    authorization_policies:
        # skip authorization
        - resource:
            path: []
            method: []
            claims: []
```

The sample policy definition performs the following:
- Citrix ADC performs the local authentication on the requests to the following:
  - **GET** or **POST** operation on orders and shipping end points.
- Citrix ADC does not perform the authentication for **GET** operation on the **products** endpoint.
- Citrix ADC does not apply any authorization permissions.

### oAuth JWT verification

The following is a sample authentication and authorization policy definition for oAuth JWT verification (oauth_jwt_auth.yaml).

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: authexample
spec:
    servicenames:
    - frontend

    authentication_providers:
      - name: "jwt-auth-provider"
        oauth:
           issuer: "https://sts.windows.net/tenant1/"
           jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0/keys"
           audience : ["https://api.service.net"]
           claims_to_save : ["scope"]

    authentication_policies:
        - resource:
            path:
              - '/orders/'
              - '/shipping/'
            method: [GET, POST]
          provider: ["jwt-auth-provider"]
        
        # skip authentication for this
        - resource:
            path:
              - '/products/'
            method: [GET]
          provider: []

    authorization_policies:
        - resource:
            path:
              - '/orders/'
              - '/shipping/'
            method: [POST]
            claims: 
              - name: "scope"
                values: ["read", "write"]
        - resource:
            path:
              - '/orders/'
            method: [GET]
            claims: 
              - name: "scope"
                values: ["read"]
        # skip authorization, no claims required
        - resource:
            path:
              - '/shipping/'
            method: [GET]
            claims: []
```
The sample policy definition performs the following:

- Citrix ADC performs JWT verification on the requests to the following:
  –	**GET** or **POST** operation on **orders** and **shipping** endpoints.
- Citrix ADC skips authentication for the **GET** operation on the **products** endpoint.
-	Citrix ADC requires the scope claim with `read` and `write` permissions for **POST** operation on **orders** and **shipping** endpoints.
-	Citrix ADC requires the scope claim with the read permission for **GET** operation on the **orders** endpoint.
-	Citrix ADC does not need any permissions for **GET** operation on the **shipping** end point.



For OAuth, if the token is present in a custom header, it can be specified using the `token_in_hdr` attribute as follows:


          oauth:
            issuer: "https://sts.windows.net/tenant1/"
            jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0/keys"
            audience : ["https://vault.azure.net"]
            token_in_hdr : [“custom-hdr1”]

Similarly, if the token is present in a query parameter, it can be specified using the `token_in_param` attribute as follows:

          oauth:
            issuer: "https://sts.windows.net/tenant1/"
            jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0keys"
            audience : ["https://vault.azure.net"]
            token_in_param : [“query-param1”]


### oAuth Introspection

The following is a sample authentication and authorization policy definition for oAuth JWT verification. ([oauth_intro_auth.yaml]())

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: authexample
spec:
    servicenames:
    - frontend

    authentication_providers:
        - name: "introspect-provider"
          oauth:
            issuer: "ns-idp"
            jwks_uri: "https://idp.aaa/oauth/idp/certs"
            audience : ["https://api.service.net"]
            client_credentials: "oauthsecret"
            introspect_url: https://idp.aaa/oauth/idp/introspect
            claims_to_save : ["scope"]

    authentication_policies:
        - resource:
            path: []
            method: []
          provider: ["introspect-provider"]
        
    authorization_policies:
        - resource:
            path: []
            method: [POST]
            claims: 
             - name: "scope"
               values: ["read", "write"]
        - resource:
            path: []
            method: [GET]
            claims: 
             - name: "scope"
               values: ["read"]
```
The sample policy definition performs the following:

-	Citrix ADC performs the oAuth introspection as specified in the provider “introspect-provider” for all requests.
-	Citrix ADC requires the scope claim with `read` and `write` permissions for all **POST** requests.
-	Citrix ADC requires the scope claim with the read permission for all **GET** requests.

### Creating a secrets object with client credentials for introspection

A Kubernetes secrets object is needed for configuring the OAuth introspection.
You can create a secret object in a similar way as shown in the following example:


    apiVersion: v1        
    kind: Secret          
    metadata:             
      name: oauthsecret
    type: Opaque        
    stringData:           
     client_id: "nsintro"
     client_secret: "nssintro"

**Note:**
Keys of the opaque secret object must be `client_id` and `client_secret`. A user can set the values for them as desired.

### SAML authentication using forms

The following is an example for SAML authentication using forms. In the example, `authhost-tls-cert-secret` and `saml-tls-cert-secret` are Kubernetes TLS secrets referring to certificate and key.

**Note:** When `certkey.cert` and `certkey.key` are certificate and key respectively for the authentication host, then the `authhost-tls-cert-secret` can be formed using the following command:

         kubectl create secret tls authhost-tls-cert-secret --key="certkey.key" --cert="certkey.cert

  Similarly, you can use this command to form `saml-tls-cert-secret` with the required certificate and key.

```yml

apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: samlexample
spec:
    servicenames:
    - frontend

    authentication_mechanism:
      using_forms:
        authentication_host: "fqdn_authenticaton_host"
        authentication_host_cert:
          tls_secret: authhost-tls-cert-secret
        ingress_name: “example-ingress”

    authentication_providers:
        - name: "saml-auth-provider"
          saml:
              metadata_url: "https://idp.aaa/metadata/samlidp/aaa"
              signing_cert:
                  tls_secret: saml-tls-cert-secret

    authentication_policies:

        - resource:
            path: []
            method: []
          provider: ["saml-auth-provider"]

    authorization_policies:

        - resource:
            path: []
            method: []
            claims: []

```
The sample policy definition performs the following:

-	Citrix ADC performs SAML authentication as specified in the provider `saml-auth-provider` for all requests. 
  **Note:** Granular authentication is not supported for the forms mechanism.
-	Citrix ADC requires the group claim with `admin` permission for all **POST** requests.
-	Citrix ADC does not require any specific permission for **GET** requests.

### OpenID Connect authentication using forms

The following is an example for creating OpenID Connect authentication to configure Citrix ADC in a Relaying Party (RP) role to authenticate users for an external identity provider. The `authentication_mechanism` must be set to `using_forms` to trigger the OpenID Connect procedures.

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: authoidc
spec:
    servicenames:
    - frontend
    authentication_mechanism:
        using_forms:
            authentication_host: "10.221.35.213"
            authentication_host_cert:
                 tls_secret: "oidc-tls-secret"
            ingress_name:  “example-ingress”

    authentication_providers:

        - name: "oidc-provider"
          oauth:
            audience : ["https://app1.citrix.com"]
            client_credentials: "oidcsecret"
            metadata_url: "https://10.221.35.214/oauth/idp/.well-known/openid-configuration"
            default_group: "groupA"
            user_field: "sub"
            pkce: "ENABLED"
            token_ep_auth_method: "client_secret_post"

    authentication_policies:

        - resource:
            path: []
            method: []
          provider: ["oidc-provider"]

    authorization_policies:

        #default - no authorization requirements
        - resource:
            path: []
            method: []
            claims: []
```
The sample policy definition performs the following:

-	Citrix ADC performs OIDC authentication (relying party) as specified in the provider “oidc-provider” for all requests.
  **Note:** Granular authentication is not supported for the forms mechanism.
- Citrix ADC does not require any authorization permissions.

### LDAP authentication using the request header

The following is an example for LDAP authentication using the request header.

In this example, `ldapcredential` is the Kubernetes secret referring to the LDAP server credentials. See the `ldap_secret.yaml` file for information on how to create LDAP server credentials.

```yml

apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: ldapexample
spec:
    servicenames:
    - frontend

    authentication_providers:
        - name: "ldap-auth-provider"
          ldap:
              server_ip: "192.2.156.160"
              base: 'dc=aaa,dc=local'
              login_name: accountname
              sub_attribute_name: CN
              server_login_credentials: ldapcredential

        - name: "local-auth-provider"
          basic-local-db:

    authentication_policies:

        - resource:
            path: []
            method: []
          provider: ["ldap-auth-provider"]


    authorization_policies:

        - resource:
            path: []
            method: []
            claims: []
```

**Note:** With the request header based authentication mechanism, granular authentication based on traffic is supported.

### LDAP authentication using forms

In the example `authhost-tls-cert-secret` is the Kubernetes TLS secret referring to certificate and key.

When `certkey.cert` and `certkey.key` are certificate and key respectively for the authentication host, then the `authhost-tls-cert-secret`  can be formed using the following
 command:

        kubectl create secret tls authhost-tls-cert-secret --key="certkey.key" --cert="certkey.cert

In this example, `ldapcredential` is the Kubernetes secret referring to the LDAP server credentials. See the `ldap_secret.yaml` file for information on how to create LDAP server credentials.

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: ldapexample
spec:
    servicenames:
    - frontend

    authentication_mechanism:
      using_forms:
        authentication_host: "fqdn_authenticaton_host"
        authentication_host_cert:
          tls_secret: authhost-tls-cert-secret
        vip: "192.2.156.156"

    authentication_providers:
        - name: "ldap-auth-provider"
          ldap:
              server_ip: "192.2.156.160"
              base: 'dc=aaa,dc=local'
              login_name: accountname
              sub_attribute_name: CN
              server_login_credentials: ldapcredential

    authentication_policies:

        - resource:
            path: []
            method: []
          provider: ["ldap-auth-provider"]

    authorization_policies:

        - resource:
            path: []
            method: []
            claims: []

```

The sample policy definition performs the following:
-	Citrix ADC performs the LDAP authentication for entire traffic (all requests).
-	Citrix ADC does not apply any authorization permission.


**LDAP_secret.yaml**


The following is an example for `LDAP_secret.yaml`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ldapcredential
type: Opaque
stringData:
  username: 'ldap_server_username'
  password: 'ldap_server_password'

```
        