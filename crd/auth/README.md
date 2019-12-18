# Define authentication policies on the Ingress Citrix ADC

Authentication policies are used to enforce access restrictions to resources hosted by an application or an API server.

Citrix provides a Kubernetes [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) called the **Auth CRD** that you can use with the Citrix ingress controller to define authentication policies on the ingress Citrix ADC.

## Auth CRD definition

The Auth CRD is available in the Citrix ingress controller GitHub repo at: [auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml). The Auth CRD provides [attributes](#auth-crd-attributes) for various options that are required to define authentication policies on the Ingress Citrix ADC.

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
  validation:
    openAPIV3Schema:
      properties:
        spec:
          properties:
            servicenames:
              description: 'Name of the services that needs to be binded to rewrite policy.'
              type: array
              items:
                type: string
                maxLength: 127
            auth_providers:
              description: 'Auth Config for required auth providers, one or more of these can be created'
              type: array
              items:
                  description: " create config for a single auth provider of a particular type"
                  properties:
                    name:
                      description: 'Name for this provider, has to be unique, referenced by auth policies'
                      type: string

                    oauth:
                      description: 'Auth provided by external oAuth provider' 
                      properties:
                          issuer:
                              description: 'Identity of the server whose tokens are to be accepted'
                              type: string
                          jwks_uri:
                              description: 'URL of the endpoint that contains JWKs (Json Web Key) for JWT (Json Web Token) verification'
                              type: string
                          audience:
                              description: 'Audience for which token sent by Authorization server is applicable'
                              type: array
                              items:
                                type: string
                          token_in_hdr:
                              description: 'custom header name where token is present, default is Authorization header'
                              type: array
                              items:
                                type: string
                          token_in_param:
                              description: 'query parameter name where token is present'
                              type: array
                              items:
                                type: string

                    basic_local_db:
                      description: 'Basic HTTP authentication, user data in local DB'

                  required:
                    - name

            auth_policies:
              description: "Auth policies"
              type: array
              items:
                description: "Auth policy"
                properties:
                  resource:
                      description: " endpoint/resource selection criteria"
                      properties:
                        path:
                          description: "api resource path e.g. /products. "
                          type: array
                          items:
                            type: string
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
                required:
                  - resource
                  - provider

          required:
            - servicenames
```

## Auth CRD attributes

The Auth CRD provides the following attributes that you use to define the authentication policies:

-  `servicenames`
-  `auth_providers`
-  `auth_policies`

### servicenames

The name of the services that you want to bind to the authentication policy.

### auth_providers

The **providers** define the authentication mechanism and parameters that are required for the authentication mechanism. The CRD supports both *basic authentication* and *OAuth authentication*.

#### Basic authentication

To use basic authentication, you must create the user accounts on the ingress Citrix ADC. Any new request to the services in your Kubernetes deployment must contain the *Authentication* header with the user name and password and the request is validated with user credentials within the Citrix ADC.

##### Basic authentication attributes

The following are the attributes for basic authentication:

| Attribute | Description |
| --------- | ----------- |
| `name` | The name of the provider. This name is used in the [policies](#authproviders) to refer the provider. |
| `basic_local_db` | Specifies that local authentication is used with the HTTP basic authentication scheme. The requests should contain the authentication header with user name and password.|

#### OAuth authentication

The OAuth authentication mechanism, requires an external identity provider to authenticate the client using the OAuth 2.0 protocol and issue an access token. When the client presents the access token to the Citrix ADC as an access credential, the Citrix ADC validates the token using the configured values. If the token validation is successful then the Citrix ADC grants access to the client.

##### OAuth authentication attributes

The following are the attributes for OAuth authentication:

| Attribute | Description |
| --------- | ----------- |
| `Issuer` | The identity (usually a URL) of the server whose tokens need to be accepted for authentication.|
| `jwks_uri` | The URL of the endpoint that contains JWKs (JSON Web Key) for JWT (JSON Web Token) verification.|
| `audience` | The identity of the service or application for which the token is applicable. |
| `token_in_hdr` | The custom header name where the token is present. Default is `Authorization` header.</br> **Note:** You can specify more than one header. |
| `token_in_param` | The query parameter where the token is present. |

### auth_policies

The **policies** allow you to define the traffic selection criteria for applying the authentication mechanism. You can also specify the provider that you want to use for the selected traffic.

The following are the attributes for policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. </br>**Note:** The traffic is selected if the incoming request URI matches with any of the paths AND any of the listed methods. If the method is not specified then the path alone is used for the traffic selection criteria.|
| `provider` | Specifies the authentication mechanism that needs to be used. If the value is not provided, then authentication is not performed. |

## Deploy the Auth CRD

Perform the following to deploy the Auth CRD:

1.  Download the CRD ([auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml)).

1.  Deploy the Auth CRD using the following command:

        kubectl create -f auth-crd.yaml

    For example,

        root@master:~# kubectl create -f auth-crd.yaml

        customresourcedefinition.apiextensions.k8s.io/authpolicies.citrix.com created

## How to write authentication policies

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the authentication policy configuration in a `.yaml` file. In the `.yaml` file, use `authpolicy` in the `kind` field and add Auth CRD attributes in the `spec` section based on your policy configuration requirements.

After you deploy the `.yaml` file, the Citrix ingress controller applies the authentication policy configuration on the Ingress Citrix ADC device.

The following is a sample authentication policy definition ([auth_example1.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth_example1.yaml)):

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
```

The sample authentication policy performs the following:

-  The Citrix ADC performs the authentication mechanism specified in the provider `local-auth-provider` on the requests to the following endpoints:
      -  **orders**, **shipping**, and **GET** or **POST**
      -  **products** and **POST**
-  The Citrix ADC does not perform the authentication for the **products** and **GET** endpoints.
-  The Citrix ADC performs the authentication mechanism specified in the provider `jwt-auth-provider` on the requests to the **reviews** endpoint. If the token is present in a custom header, it can be specified using the `token_in_hdr` attribute as follows:

          oauth:
            issuer: "https://sts.windows.net/tenant1/"
            jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0/keys"
            audience : ["https://vault.azure.net"]
            token_in_hdr : [“custom-hdr1”]

    Similarly, if the token is present in a query parameter, it can be specified using the “token_in_param” attribute as follows:

          oauth:
            issuer: "https://sts.windows.net/tenant1/"
            jwks_uri: "https://login.microsoftonline.com/tenant1/discovery/v2.0/keys"
            audience : ["https://vault.azure.net"]
            token_in_param : [“query-param1”]
