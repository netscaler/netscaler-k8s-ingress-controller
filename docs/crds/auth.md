# Define authentication policies on the Ingress Citrix ADC

Authentication policies are used to enforce access restrictions to the resources hosted by an application or API server.

Citrix provides a Kubernetes [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) called the **Auth CRD**that you can use with the Citrix ingress controller to define authentication policies on the ingress Citrix ADC.

## Auth CRD definition

The Auth CRD is available in the Citrix ingress controller GitHub repo at: ***link to the CRD YAML***. The Auth CRD provides [attributes](#auth-crd-attributes) for various options that are required to define the authentication policies on the Ingress Citrix ADC.

The following is the Auth CRD definition:

```yml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: authpolicies.citrix.com
spec:
  group: citrix.com
  version: v1
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
              description: 'Name of the services that needs to be binded to auth policy.'
              type: array
              items:
                type: string
            auth_providers:
              description: 'Auth Config for required auth providers, one or more of these can be created'
              type: array
              items:
                  description: " create config for a single auth provider of a particular type"
                  properties:
                    name:
                      description: 'Name for this provider, has to be unique, referenced by auth policies'
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

The **providers** define the authentication mechanism and parameters that are required for the authentication mechanism. The current version of the CRD supports only *basic authentication* and hence you should create the user accounts on the ingress Citrix ADC.

Any new request to the services in your Kubernetes deployment must contain the *Authentication* header with the user name and password and the request is validated with user credentials within the Citrix ADC.

The following are the attributes for local authentication:

| Attribute | Description |
| --------- | ----------- |
| `name` | The name of the provider. This name is used in the [policies](#authproviders) to refer the provider. |
| `basic_local_db` | Specifies that local authentication is used with the HTTP basic authentication scheme. The requests should contain the Authentication header with user name and password.|

### auth_policies

The **policies** allow you to define the traffic selection criteria to apply the authentication mechanism and also to specify the provider that you want to use for the selected traffic.

The following are the attributes for policies:

| Attribute | Description |
| --------- | ----------- |
| `path` | An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/`.  |
| `method` | An array of HTTP methods. Allowed values are GET, PUT, POST, or DELETE. </br>**Note:** The traffic is selected if the incoming request URI matches with any of the paths AND any of the listed methods. If the method is not specified then the path alone is used for the traffic selection criteria.|
| `provider` | Specifies the authentication mechanism that needs to be used. If no value is provided then authentication is not performed. |

## Deploy the Auth CRD

Perform the following to deploy the Auth CRD:

1.  Download the CRD ([auth-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth-crd.yaml)).

1.  Deploy the Auth CRD using the following command:

        kubectl create -f auth-crd.yaml

    For example,

        root@master:~# kubectl create -f auth-crd.yaml

        customresourcedefinition.apiextensions.k8s.io/authpolicies.citrix.com created

## How to write the authentication policies

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the authentication policy configuration in a `.yaml` file. In the `.yaml` file, use `authpolicy` in the `kind` field and in the `spec` section add the Auth CRD attributes based on your requirement for the policy configuration.

After you deploy the `.yaml` file, the Citrix ingress controller applies the authentication policy configuration on the Ingress Citrix ADC device.

The following is sample authentication policy definition ([auth_example1.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/auth/auth_example1.yaml)):

```yml
apiVersion: citrix.com/v1
kind: authpolicy
metadata:
  name: authexample
spec:
    servicenames:
    - frontend

    auth_providers:

        - name: "local-auth-provider"
          basic-local-db:

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

          # no auth for these
        - resource:
            path:
              - '/products/'
            method: [GET]
          provider: []

        - resource:
            path:
              -  '/reviews/'
          provider: []
```

The sample authentication policy performs the following:

-  The Citrix ADC performs the authentication mechanism specified in the provider `local-auth-provider` on the requests to the following endpoints:
   -  **orders**, **shipping**, and **GET** or **POST**
   -  **products** and **POST**
-  The Citrix ADC does not perform the authentication mechanism for the following endpoints:
   -  **products** and **POST**
   -  **reviews**
