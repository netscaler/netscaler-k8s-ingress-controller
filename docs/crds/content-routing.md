## Advanced content routing for Kubernetes with Citrix ADC

Kubernetes native Ingress offers basic host and path based routing. But, other advanced routing techniques like routing based on header values or query strings is not supported in the Ingress structure. You can expose these features on the Kubernetes Ingress through Ingress annotations, but more annotations are complex to manage and validate.

You can expose the advanced content routing abilities provided by Citrix ADC as a custom resource definition (CRD) API for Kubernetes. This API enables you to use the following advanced content routing features on Citrix ADC in a Kubernetes environment:

- HTTP headers
- Cookie
- Query parameters
- HTTP method

## API definition

The advanced Content routing feature is exposed with the following CRDs:

 - Listener
 - HTTPRoute

### Listener CRD

Listener API defines the end-point configuration. Endpoint IP, port, protocol, certificates, routing actions and list of routes linked to the listener are part of the [Listener CRD](../../crd/contentrouting/Listener.yaml).

Following is the Listener CRD definition.

```
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: listeners.citrix.com
status:
spec:
  group: citrix.com
  version: v1alpha1
  names:
    kind: Listener 
    plural: listeners 
    singular: listener
  scope: Namespaced
  validation:
    openAPIV3Schema:
      required: [spec]
      properties:
        spec:
          type: object
          required: [protocol]
          properties:
            protocol:
              type: string
              enum: ["https", "http"]
              description: "Protocol for this listener"
            vip:
              type: string
              description: "Endpoint IP address, Optional for CPX, required for Tier-1 deployments"
            port:
              type: integer
              minimum: 1
              maximum: 65535
            certificates:
              type: array
              description: "certificates attached to the endpoints - Not applicable for HTTP"
              minItems: 1
              items:
                type: object 
                properties:
                  preconfigured:
                    type: string
                    description: "Preconfigured Certificate name on ADC "
                  secret:
                    type: object 
                    description: "Kuberentes secret object"
                    required: [name]
                    properties:
                      name:
                        type: string
                        description: "name of the Kubernetes object where Cert is located"
                        pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                  default:
                    type: boolean
                    description: "Only one of the certificate can be marked as default which will be presented if none of the cert matches with the hostname"
            routes:
              type: array
              description: "List of route objects attached to the listener"
              minItems: 1
              items:
                type: object
                properties:
                  name:
                    type: string
                    description: "Name of the HTTPRoute object"
                    pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                  namespace:
                    type: string
                    description: "Namespace of the HTTPRoute object"
                    pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                  labelSelector:
                    description: "Labels key value pair, if the route carries the same labels, it is automatically attached"
                    type: object
                    additionalProperties:
                      type: string
                oneOf:
                - required: [name, namespace] 
                - required: [labelSelector]
            defaultAction:
              type: object
              description: "Default action for the listener: One of Backend or Redirect"
              properties:
                backend:
                  type: object
                  oneOf:
                  - required: [kube]
                  properties:
                    kube:
                      type: object
                      required: [service, port]
                      properties:
                        service:
                          description: "Name of the backend service"
                          type: string
                          pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                        port:
                          description: "Service port"
                          type: integer
                          minimum: 1
                          maximum: 65535
                        namespace:
                          description: "Service namespace"
                          type: string
                          pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                        backendConfig:
                          description: "General backend service options"
                          properties:
                            secure_backend:
                              description: "Use Secure communications to the backends"
                              type: boolean
                            lbConfig:
                              description: "Citrix ADC LB vserver configurations for the backend. Refer: https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/load-balancing/lbvserver/lbvserver/ for all configurations"
                              type: object
                              additionalProperties:
                                type: string
                            servicegroupConfig:
                              description: "Citrix ADC service group configurations for the backend; Refer: https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/basic/servicegroup/servicegroup/ for all configurations"
                              type: object
                              additionalProperties:
                                type: string
                redirect:
                  type: object
                  oneOf:
                  - required: [targetExpression]
                  - required: [hostRedirect]
                  - required: [httpsRedirect]
                  properties:
                    httpsRedirect:
                      description: "Change the scheme from http to https keeping URL intact"
                      type: boolean
                    hostRedirect:
                      description: "Host name specified is used for redirection with URL intact"
                      type: string
                    targetExpression:
                      description: "A target can be specified using Citrix ADC policy expression"
                      type: string
                    responseCode:
                      description: "Default response code is 302, which can be customised using this attribute"
                      type: integer
                      minimum: 100
                      maximum: 599
              oneOf:
              - required: ["backend"]
              - required: ["redirect"]
  subresources:
    # status enables the status subresource.
    status: {}
```

### Listener CRD attributes

Listener CRD attributes are provided as follows:

- `protocol`: Protocol for the listener. Available options are HTTP and HTTPs.

- `vip`: Endpoint IP address. This attribute is optional for Citrix ADC CPX and required for tier-1 deployments.

- `port`: Endpoint port

- `certificates`: Certificates attached to the end point. Only applicable for the HTTPS protocol. Certificates can be configured in two ways:

    - Preconfigured: Preconfigured certificate name which is stored in a Citrix ADC.
    - Secret: Kubernetes secret object name where the certificate is located.

- `routes`: List of route objects attached to the listener. Routes are referenced with following properties:
  
  - `name`: Specifies the name of the HTTPRoute CRD object.
  - `namespace`: Specifies the namespace of the HTTPRoute CRD object.
  - `labelSelector`: Specifies the key-value pair for labels. If an HTTP route carries same labels, it is automatically attached.
  
- `defaultAction`: Specifies the default action for the listener. This could be a default back-end or a redirect destination.
    - `kube`: Default back end details
      -	`service`: Name of the service
      -	`namespace`:  Namespace of the service
      - `port`: Port information
      - `backendConfig`: Back-end service properties
        - `secure_backend`: Use secure communication to the back end service
        - `lbConfig`: Citrix ADC load balancer virtual server configurations for the back-end
        - `servicegroupConfig`: Service group configurations for the back-end
    - `redirect`: Redirect endpoint details
      - `httpsRedirect`: Scheme for the redirect URL
      - `hostRedirect`: Host name to be used for redirect
      - `targetExpression`: Redirect target specified as the Citrix ADC policy expression.
      - `responseCode`: Default value is 302. Customizable with this field.

### Deploy the Listener CRD

1. Download the [Listener CRD](../../crd/contentrouting/Listener_crd.yaml).
2. Deploy the listener CRD with following command.

	    Kubectl create -f  Listener-crd.yaml
        Example:
        root@k8smaster:# kubectl create -f Listener-crd.yaml 
        customresourcedefinition.apiextensions.k8s.io/listeners.citrix.com created

### How to write Listener CRD objects

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the listener configuration in a YAML file. In the YAML file, use `Listener` in the kind field and in the spec section add the listener CRD attributes based on your requirement for the listener configuration.
After you deploy the YAML file, the Citrix ingress controller applies the listener configuration on the Ingress Citrix ADC device.
The [Listener.yaml](../../crd/contentrouting/Listener_crd.yaml) file contains a sample listener definition.  

```yml

apiVersion: citrix.com/v1alpha1
kind: Listener
metadata:
  name: test
  namespace: default
spec:
  certificates:
  - secret:
      name: my-secret
  - secret:
      name: secret2
      namespace: demo
  - default: true
    preconfigured: second-secret
  defaultAction:
    backend:
      kube:
        namespace: default
        port: 80
        service: default-service
        backendConfig:
          lbConfig:
            lbmethod: ROUNDROBIN
          servicegroupConfig:
            clttimeout: 20
  vip: 1.1.1.1
  port: 443
  protocol: https
  routes:
  - labelSelector:
      xyz: abc
  - name: domain-1
    namespace: default
  - name: domain-2
    namespace: default

```

In this example, a listener is exposing an HTTPS endpoint. Under certificates section, SSL certificates for the end are configured as Kubernetes secrets and a default ADC preconfigured certificate. The default action for the listener is configured as a Kubernetes service under defaultAction section.
Routes are attached with the listener using both label selectors and individual route references using name and namespace under routes section.

### HTTPRoute CRD

HTTPRoute API defines the route related configurations, domain names, routing rules, and actions which are part of the [HTTPRoute CRD](../../crd/contentrouting/HTTPRoute.yaml).  

Following is the HTTPRoute CRD definition:

```yml

apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: httproutes.citrix.com
spec:
  group: citrix.com
  version: v1alpha1
  names:
    kind: HTTPRoute
    plural: httproutes
    singular: httproute
  scope: Namespaced
  validation:
    openAPIV3Schema:
      required: [spec] 
      properties:
        spec:
          type: object
          required: [rules]
          properties:
            hostname:
              type: array
              description: "List of domain names that share the same route, default is '*'"
              minItems: 1
              items:
                type: string
                description: "Domain name"
            rules:
              type: array
              description: "List Content routing rules with an action defined"
              minItems: 1
              items:
                type: object
                required: [name, action]
                properties:
                  name:
                    type: string
                    description: "A name to represent the rule, this is used as an identifier in content routing policy name in ADC"
                    minLength: 1
                    maxLength: 20
                    pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                  match:
                    type: array
                    description: "List of rules with same action"
                    minItems: 1
                    items:
                      type: object
                      anyof:
                      - required: [path]
                      - required: [headers]
                      - required: [cookies]
                      - required: [queryParams]
                      - required: [method]
                      - required: [policyExpression]
                      properties:
                        path:
                          type: object
                          description: "URL Path based content routing"
                          properties:
                            prefix:
                              type: string
                              description: "URL path matches the prefix expression"
                            exact:
                              type: string
                              description: "URL Path must match exact path"
                            regex:
                              type: string
                              description: "PCRE based regex expression for path matching"
                        headers:
                          type: array
                          description: "List of header for content routing - Must match all the rules- Treated as AND condition if more than 1 rule"
                          minItems: 1
                          items:
                            type: object
                            description: "Header details for content routing, Check for existence of a header or header name-value match"
                            properties:
                              headerName:
                                type: object
                                description: "Header name based content routing, Here existence of header is used for routing"
                                properties:
                                  exact:
                                    type: string
                                    description: "Header Name - treated as exact must exist"
                                  contains:
                                    type: string
                                    description: "Header Name - A header must exist that contain the string the name"
                                  regex:
                                    type: string
                                    description: "header Name - treated as PCRE regex expression"
                                  not:
                                    type: boolean
                                    description: "Default False, if present, rules are inverted. I.e header name must not exist"
                                oneOf:
                                - required: [exact]
                                - required: [contains]
                                - required: [regex]
                              headerValue:
                                type: object
                                description: "Header Name and Value based match"
                                properties:
                                  name:
                                    type: string
                                    description: "Header name that must match the value"
                                  exact:
                                    type: string
                                    description: "Header value - treated as exact"
                                  contains:
                                    type: string
                                    description: "Header value - treated as contains"
                                  regex:
                                    type: string
                                    description: "header value - treated as PCRE regex expression"
                                  not:
                                    type: boolean
                                    description: "Default False, if present, rules are inverted. I.e header if present must not match the value"
                                oneOf:
                                - required: [name, exact]
                                - required: [name, contains]
                                - required: [name, regex]
                        queryParams:
                          type: array
                          description: "List of Query parameters  for content routing - Must match all the rules- Treated as AND condition if more than 1 rule"
                          minItems: 1
                          items:
                            type: object
                            description: "Query parameters Name and Value based match"
                            properties:
                              name:
                                type: string
                                description: "Query name that must match the value. If no value is specified, matches with any value"
                              exact:
                                type: string
                                description: "Query value - Exact match"
                              contains:
                                type: string
                                description: "Query value - value must have the string(substring)"
                              regex:
                                type: string
                                description: "Query value - Value must match this regex patterm"
                              not:
                                type: boolean
                                description: "Default False, if present, rules are inverted. I.e query if present must not match the value"
                            oneOf:
                            - required: [name]
                            - required: [name, exact]
                            - required: [name, contains]
                            - required: [name, regex]
                        cookies:
                          type: array
                          description: "List of Cookie params for content routing - Must match all the rules- Treated as AND condition if more than 1 rule"
                          minItems: 1
                          items:
                            type: object
                            description: "Cookie based routing"
                            properties:
                              name:
                                type: string
                                description: "cookie name that must match the value. If no value specified, it matches with any value"
                              exact:
                                type: string
                                description: "cookie value - treated as exact"
                              contains:
                                type: string
                                description: "cookie value - treated as substring"
                              regex:
                                type: string
                                description: "cookie value - treated as PCRE regex expression"
                              not:
                                type: boolean
                                description: "Default False, if present, rules are inverted. I.e cookie if present must not match the value"
                            oneOf:
                            - required: [name]
                            - required: [name, exact]
                            - required: [name, contains]
                            - required: [name, regex]
                            method:
                              type: string
                              description: "HTTP method for content routing eg: POST, PUT, DELETE etc"
                            policyExpression:
                              type: string
                              description: "Citrix ADC policy expressions; refer: https://docs.citrix.com/en-us/netscaler/media/expression-prefix.pdf"
                  action:
                    type: object
                    description: "Action for the matched rule"
                    properties:
                      backend:
                        type: object
                        oneOf:
                        - required: [kube]
                        properties:
                          kube:
                            type: object
                            required: [service, port]
                            properties:
                              service:
                                description: "Name of the backend service"
                                type: string
                                pattern: '^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
                              port:
                                description: "Service port" 
                                type: integer 
                                minimum: 1
                                maximum: 65535
                              backendConfig:
                                description: "General backend service options"
                                properties:
                                  secure_backend:
                                    description: "Use Secure communications to the backends"
                                    type: boolean
                                  lbConfig:
                                    description: "Citrix ADC LB vserver configurations for the backend. Refer: https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/load-balancing/lbvserver/lbvserver/ for all configurations"
                                    type: object
                                    additionalProperties:
                                      type: string
                                  servicegroupConfig:
                                    description: "Citrix ADC service group configurations for the backend; Refer: https://developer-docs.citrix.com/projects/netscaler-nitro-api/en/12.0/configuration/basic/servicegroup/servicegroup/ for all configurations"
                                    type: object
                                    additionalProperties:
                                      type: string
                      redirect:
                        type: object
                        oneOf:
                        - required: [targetExpression]
                        - required: [hostRedirect]
                        - required: [httpsRedirect]
                        properties:
                          httpsRedirect:
                            description: "Change the scheme from http to https keeping URL intact"
                            type: boolean
                          hostRedirect:
                            description: "Host name specified is used for redirection with URL intact"
                            type: string
                          targetExpression:
                            description: "A target can be specified using Citrix ADC policy expression"
                            type: string
                          responseCode:
                            description: "Default response code is 302, which can be customised using this attribute"
                            type: integer
                            minimum: 100
                            maximum: 599
                    oneOf:
                    - required: ["backend"]
                    - required: ["redirect"]
  subresources:
    # status enables the status subresource.
    status: {}

```

### HTTPRoute CRD attributes

Following are the attributes for the HTTPRoute CRD.

- `hostname` : Specifies the list of domain names that share route, default is *.

- `rules`: List of content routing rules with defined actions:
   - `name`: Name of the rule
   - `match`: List of rules with same action
     - `path`: URL Path based routing
     - `headers`: List of headers for content routing
     - `queryparams`: List of query parameters for content routing
     - `cookies`: List of cookie parameters for content routing

- `actions`: Specifies actions for matched rule. This could be a default back-end or a redirect destination.

    - `kube`: Default back end details
      -	`service`: Name of the service
      -	`namespace`:  Namespace of the service
      - `port`: Port information
      - `backendConfig`: Back-end service properties
        - `secure_backend`: Use secure communication to the back end service
        - `lbConfig`: Citrix ADC load balancer virtual server configurations for the back end
        - `servicegroupConfig`: Service group configurations for the back-end
    - `redirect`: Redirect endpoint details
      - `httpsRedirect`: Scheme for the redirect URL
      - `hostRedirect`: Host name to be used for redirect
      - `targetExpression`: Redirect target specified as the Citrix ADC policy expression.
      - `responseCode`: Default value is 302. Customizable with this field.

### Deploy the HTTPRoute CRD

Perform the following to deploy the HTTPRoute CRD:

1. Download the [HTTPRoute CRD](../../crd/contentrouting/HTTPRoute.yaml).
2. Deploy the HTTPRoute CRD using the following command.

	    Kubectl create -f  Route-crd.yaml 
    
        Example:
        root@k8smaster:# kubectl create -f Route-crd.yaml
        customresourcedefinition.apiextensions.k8s.io/httproutes.citrix.com created

### How to write HTTPRoute CRD objects

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the HTTP route configuration in a YAML file. In the YAML file, use `HTTPRoute` in the kind field and in the spec section add the HTTPRoute CRD attributes based on your requirement for the HTTP route configuration.
After you deploy the YAML file, the Citrix ingress controller applies the HTTP route configuration on the Ingress Citrix ADC device.

The [HTTPRoute.yaml](../../crd/contentrouting/HTTPRoute_crd.yaml) file contains a sample HTTPRoute definition:

```yml
apiVersion: citrix.com/v1alpha1
kind: HTTPRoute
metadata:
   name: header-routing 
spec:
  hostname:
  - host1.com
  rules:       
  - name: rulename 
    match:
    - headers:
      - headerName:
          contains: mobile 
    action:
      backend:
        kube:
          service: mobile_svc
          port: 80
```

In this example, HTTPRoute CRD is configuring routing rules for content routing. Routing is configured as a header name matching rule under rules section. A match is considered if the header name contains the string `mobile`.

Action for the routing rule match is configured as a Kubernetes service under the action section using a Kubernetes service name and port details.
