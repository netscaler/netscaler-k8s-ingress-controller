# Define authentication and authorization policies on the Ingress Citrix ADC

Authentication policies are used to enforce access restrictions to the resources hosted by an application or API server.

Citrix provides a Kubernetes [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) called the **Auth CRD** that you can use with the Citrix ingress controller to define authentication policies on the ingress Citrix ADC.

## Auth CRD definition

The Auth CRD is available in the Citrix ingress controller GitHub repo at: [auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml). The Auth CRD provides [attributes](#auth-crd-attributes) for various options that are required to define the authentication policies on the Ingress Citrix ADC.

The following is the Auth CRD definition:

```yml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: authpolicies.citrix.com
spec:
  group: citrix.com
  version: v1beta1
  names:
    kind: authpolicy
    plural: authpolicies
    singular: authpolicy 
  scope: Namespaced
  subresources:
    status: {}
  additionalPrinterColumns:
    - name: Status
      type: string
      description: "Current Status of the CRD"
      JSONPath: .status.state
    - name: Message
      type: string
      description: "Status Message"
      JSONPath: .status.status_message
  validation:
    openAPIV3Schema:
      type: object 
      properties:
        spec:
          type: object 
          properties:
            servicenames:
              description: 'Name of the service for which the policies applied'
              type: array
              items:
                type: string
                maxLength: 127
            auth_providers:
              description: 'Auth Config for required auth providers, one or more of these can be created'
              type: array
              items:
                  description: " create config for a single auth provider of a particular type"
                  type: object 
                  properties:
                    name:
                      description: 'Name for this provider, has to be unique, referenced by auth policies'
                      type: string
                      maxLength: 127

                    oauth:
                      description: 'Auth provided by external oAuth provider' 
                      type: object 
                      properties:
                          issuer:
                              description: 'Identity of the server whose tokens are to be accepted'
                              type: string
                              maxLength: 127
                          jwks_uri:
                              description: 'URL of the endpoint that contains JWKs (Json Web Key) for JWT (Json Web Token) verification'
                              type: string
                              maxLength: 127
                          audience:
                              description: 'Audience for which token sent by Authorization server is applicable'
                              type: array
                              items:
                                type: string
                                maxLength: 127
                          token_in_hdr:
                              description: 'custom header name where token is present, default is Authorization header'
                              type: array
                              items:
                                type: string
                                maxLength: 127
                              maxItems: 2
                          token_in_param:
                              description: 'query parameter name where token is present'
                              type: array
                              items:
                                type: string
                                maxLength: 127
                              maxItems: 2
                          client_credentials:
                              description: 'secrets object that contains Client Id and secret as known to Introspection server'
                              type: string
                              maxLength: 253
                          introspect_url:
                              description: ' URL of the introspection server'
                              type: string
                              maxLength: 127
                          claims_to_save:
                              description: 'list of claims to be saved, used to create authorization policies'
                              type: array
                              items:
                                type: string
                                maxLength: 127
                      anyOf:
                          - required : [jwks_uri]
                          - required : [introspect_url, client_credentials]

                    basic_local_db:
                      description: 'Basic HTTP authentication, user data in local DB'

                  required:
                    - name

            auth_policies:
              description: "Auth policies"
              type: array
              items:
                type: object 
                description: "Auth policy"
                properties:
                  resource:
                      type: object 
                      description: " endpoint/resource selection criteria"
                      properties:
                        path:
                          description: "api resource path e.g. /products. "
                          type: array
                          items:
                            type: string
                            maxLength: 511
                        method:
                          type: array
                          items:
                            type: string
                            enum: ['GET', 'PUT', 'POST','DELETE']
                      required:
                        - path
                  provider:
                    description: "name of the auth provider for the policy, empty if no authentication required"
                    type: array
                    items:
                      type: string
                      maxLength: 127
                    maxItems: 1
                required:
                  - resource
                  - provider

            authorization_policies:
              description: "Authorization policies"
              type: array
              items:
                type: object 
                description: "Authorization policy"
                properties:
                  resource:
                      type: object 
                      description: " endpoint/resource selection criteria"
                      properties:
                        path:
                          description: "api resource path e.g. /products. "
                          type: array
                          items:
                            type: string
                            maxLength: 511
                        method:
                          description: " http method"
                          type: array
                          items:
                            type: string
                            enum: ['GET', 'PUT', 'POST','DELETE']
                        claims:
                          description: " authorization scopes required for selected resource"
                          type: array
                          items:
                              type: object
                              properties:
                                name:
                                  description: " name of the claim/attribute to check"
                                  type: string
                                  maxLength: 127
                                values:
                                  description: " list of claim values required for the request"
                                  type: array
                                  items:
                                    type: string
                                    maxLength: 127
                                  minItems: 1
                              required:
                                - name
                                - values
                      required:
                        - claims

          required:
            - servicenames
```

## Auth CRD attributes

The Auth CRD provides the following attributes that you use to define the authentication policies:

-  `servicenames`
-  `auth_providers`
-  `auth_policies`
-  `authorization_policies`

### servicenames

The name of the services that you want to bind to the authentication policy.

### auth_providers

The **providers** define the authentication mechanism and parameters that are required for the authentication mechanism. The CRD supports both *basic authentication* and *OAuth authentication*.

#### Basic authentication

To use basic authentication, you must create the user accounts on the ingress Citrix ADC. Any new request to the services in your Kubernetes deployment must contain the *Authentication* header with the user name and password. The request is validated with user credentials within the Citrix ADC.

##### Basic authentication attributes

The following are the attributes for basic authentication:

| Attribute | Description |
| --------- | ----------- |
| `name` | The name of the provider. This name is used in the [policies](#authproviders) to refer the provider.|
| `basic_local_db` | Specifies that local authentication is used with the HTTP basic authentication scheme. The requests should contain the authentication header with user name and password.|

#### OAuth authentication

The OAuth authentication mechanism, requires an external identity provider to authenticate the client using oAuth2 and issue an Access token. When the client presents the Access token to Citrix ADC as an access credential, the Citrix ADC validates the token using the configured values. If the token validation is successful then Citrix ADC grants access to the client.

##### OAuth authentication attributes

The following are the attributes for OAuth authentication:

| Attribute | Description |
| --------- | ----------- |
| `Issuer` | The identity (usually a URL) of the server whose tokens need to be accepted for authentication.|
| `jwks_uri` | The URL of the endpoint that contains JWKs (JSON Web Key) for JWT (JSON Web Token) verification.|
| `audience` | The identity of the service or application for which the token is applicable.|
| `token_in_hdr` | The custom header name where the token is present. The default value is `Authorization` header.</br> **Note:** You can specify more than one header.|
| `token_in_param` | The query parameter where the token is present.|
| `introspect_url`| The URL of the introspection endpoint of the authentication server (IdP). If the access token presented is an opaque token, introspection is used for the token verification.|
| `client_credentials`| The name of the Kubernetes secrets object that contains the client id and client secret required to authenticate with the authentication server.|

### auth_policies

The **policies** allow you to define the traffic selection criteria to apply the authentication mechanism and also to specify the provider that you want to use for the selected traffic.

The following are the attributes for policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. </br>**Note:** The traffic is selected if the incoming request URI matches with any of the paths AND any of the listed methods. If the method is not specified then the path alone is used for the traffic selection criteria.|
| `provider` | Specifies the authentication mechanism that needs to be used. If the authentication mechanism is not provided, then authentication is not performed.|

### authorization policies

Authorization policies allow you to define the traffic selection criteria to apply the authorization requirements for the selected traffic.

The following are the attributes for authorization policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. </br>**Note:** The traffic is selected if the incoming request URI matches with any of the paths AND any of the listed methods. If the method is not specified then the path alone is used for the traffic selection criteria.|
| `claims` | Specifies the claims required to access a specific API endpoint. `name` indicates the claim name and `values` indicate the required permissions. You can claim more than one claim. If an empty list is specified, it implies that authorization is not required. |

## Deploy the Auth CRD

Perform the following to deploy the Auth CRD:

1.  Download the CRD ([auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml)).

2.  Deploy the Auth CRD using the following command:

        kubectl create -f auth-crd.yaml

    For example:

        root@master:~# kubectl create -f auth-crd.yaml

        customresourcedefinition.apiextensions.k8s.io/authpolicies.citrix.com created

## How to write the authentication policies

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the authentication policy configuration in a `.yaml` file. In the `.yaml` file, use `authpolicy` in the `kind` field and in the `spec` section add the Auth CRD attributes based on your requirement for the policy configuration.

After you deploy the `.yaml` file, the Citrix ingress controller applies the authentication policy configuration on the Ingress Citrix ADC device.

The following is sample authentication policy definition ([auth_example1.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth_example1.yaml)):

```yml
apiVersion: citrix.com/v1beta1
kind: authpolicy
metadata:
  name: authexample
spec:
    servicenames:
    - frontend

    auth_providers:

        - name: "local-auth-provider"
          basic-local-db:

        - name: "jwt-auth-provider"
          oauth:
            issuer: "https://sts.windows.net/tenant1/"
            jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0/keys"
            audience : ["https://vault.azure.net"]
            claims_to_save : ["scope"]
        
        - name: "introspect-provider"
          oauth:
            issuer: "ns-idp"
            jwks_uri: "https://10.221.35.214/oauth/idp/certs”
            audience : ["https://api.service.net"]
            client_credentials: "oauthsecret"
            introspect_url: https://10.221.35.214/oauth/idp/introspect
            claims_to_save : ["scope"]

    auth_policies:

        - resource:
            path:
              - '/orders/'
              - '/shipping/'
            method: [GET, POST]
          provider: ["local-auth-provider"]

        - resource:
            path:
              - '/products/'
            method: [POST]
          provider: ["local-auth-provider"]

          # no auth for this
        - resource:
            path:
              - '/products/'
            method: [GET]
          provider: []

          # oauth provider for this
        - resource:
            path:
              -  '/reviews/'
          provider: ["jwt-auth-provider"]

          # introspection provider for this
        - resource:
            path:
              -  '/customers/'
          provider: ["introspect-provider"]
    
    authorization_policies:

        - resource:
            path:
              - '/customers/'
            method: [POST]
            claims: 
            - name: "scope"
              values: ["read", "write"]

        - resource:
            path:
              - '/reviews'
            claims: 
            - name: "scope"
              values: ["read"]
        - resource:
            path:
              - '/products/'
            method: [GET]
            claims: []
    
```

The sample authentication policy performs the following:

-  The Citrix ADC performs the authentication mechanism specified in the provider `local-auth-provider` on the requests to the following endpoints:
      -  **orders**, **shipping**, and **GET** or **POST**
      -  **products** and **POST**
  
-  The Citrix ADC does not perform the authentication for the **products** and **GET** endpoints.

-  The Citrix ADC performs the oAuth JWT verification as specified in the provider `jwt-auth-provider` for the requests to the **reviews** endpoint.

-  The Citrix ADC performs the oAuth introspection as specified in the provider `introspect-provider` for the requests to the **customers** endpoint.

-  The Citrix ADC requires the `scope` claim with `read` and `write` permissions to access the **customers** endpoint and **POST**.
  
-  The Citrix ADC does not need any authorization permissions to access the **products** endpoint with GET operation.  

For oAuth, if the token is present in a custom header, it can be specified using the `token_in_hdr` attribute as follows:


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

### Creating a secrets object with client credentials for introspection

A Kubernetes secrets object is needed for configuring the oAuth introspection.
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