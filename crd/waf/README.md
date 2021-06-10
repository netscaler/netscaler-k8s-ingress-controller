# Configure web application firewall policies with the Citrix ingress controller

Citrix provides a Custom Resource Definition (CRD) called the WAF CRD for Kubernetes. You can use the WAF CRD to configure the web application firewall policies with the Citrix ingress controller on the Citrix ADC VPX, MPX, SDX, and CPX. The WAF CRD enables communication between the Citrix ingress controller and Citrix ADC for enforcing web application firewall policies.

In a Kubernetes deployment, you can enforce a web application firewall policy to protect the server using the WAF CRD. For more information about web application firewall, see [Web application security](https://docs.citrix.com/en-us/citrix-adc/13/application-firewall/introduction/web-application-security.html).

With the WAF CRD, you can configure the firewall security policy to enforce the following types of security checks for Kubernetes native applications.

**Common protections:**

- Buffer overflow
- Content type
- Allow URL
- Block URL
- Cookie consistency
- Credit card

**HTML protections:**

- CSRF (cross side request forgery) form tagging
- Field formats
- Form field consistency
- File upload types
- HTML cross-site scripting
- HTML SQL injection

**JSON protections:**

- JSON denial of service
- JSON SQL injection
- JSON cross-site scripting

**XML protections:**

- XML web services interoperability
- XML attachment
- XML cross-site scripting
- XML denial of service
- XML format
- XML message validation
- XML SOAP fault filtering
- XML SQL injection

Based on the type of security checks, you can specify the metadata and use the CRD attributes in the WAF CRD .yaml file to define the WAF policy.
 
## WAF CRD definition

The WAF CRD is available in the Citrix ingress controller GitHub repository at [waf-crd.yaml](./waf-crd.yaml). The WAF CRD provides attributes for the various options that are required to define the web application firewall policies on Citrix ADC.

The following is the WAF CRD definition:

```yml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
    name: wafs.citrix.com
spec:
    group: citrix.com
    version: v1
    names:
        kind: waf
        plural: wafs 
        singular: waf
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
            required: [spec]
            properties:
                spec:
                    type: object
                    properties:
                        servicenames:
                            description: "Name of the services to which the waf policies are applied."
                            type: array
                            items:
                                type: string
                                maxLength: 127
                        application_type:
                            description: "Type of applications to protect"
                            type: array
                            items
                                type: string
                                enum: ["HTML", "JSON", "XML"]
                        signatures:
                            description: "Location of external signature file"
                            type: string
                        redirect_url:
                            description: ""
                            type: string
                        html_error_object:
                            description: "Location of customized error page to respond when html or common violation are hit"
                            type: string
                        xml_error_object:
                            description: "Location of customized error page to respond when xml violations are hit"
                            type: string
                        json_error_object:
                            description: "Location of customized error page to respond when json violations are hit"
                            type: string
                        ip_reputation:
                            description: "Enabling IP reputation feature"
                            oneOf:
                                - type: string
                                - type: object
                        target:
                            description: "To control what traffic to be inspected by Web Application Firewall. If you do not provide the target, everything will be inspected by default"
                            type: object
                            properties:
                                paths:
                                    type: array
                                    description: "List of http urls to inspect"
                                    items:
                                        type: string
                                        description: "URL path"
                                method:
                                    type: array
                                    description: "List of http methods to inspect"
                                    items:
                                        type: string
                                        enum: ["GET", "PUT", "POST","DELETE"]
                                header:
                                    type: array
                                    description: "List of http headers to inspect"
                                    items:
                                        type: string
                                        description: "header name"
                        security_checks:
                            description: "To enable/disable application firewall security checks"
                            type: object
                            properties:
                                common:
                                    type: object
                                html:
                                    type: object
                                json:
                                    type: object
                                xml:
                                    type: object
                        settings:
                            description: "To fine tune application firewall security checks default settings"
                            type: object
                            properties:
                                common:
                                    type: object
                                html:
                                    type: object
                                json:
                                    type: object
                                xml:
                                    type: object
                        relaxations:
                            description: "Section which contains relaxation rules for known traffic and false positives"
                            type: object
                            properties:
                                common:
                                    type: object
                                html:
                                    type: object
                                json:
                                    type: object
                                xml:
                                    type: object
                        enforcements:
                            description: "Section which contains enforcement or restriction rules"
                            type: object
                            properties:
                                common:
                                    type: object
                                html:
                                    type: object
                                json:
                                    type: object
                                xml:
                                    type: object                                 
```

## WAF CRD attributes

The following table lists the various attributes provided in the WAF CRD:


| CRD attribute | Description |
| ---------- | ----------- |
| `commonchecks` | Specifies a list of common security checks, which are applied irrespective of the content type. |
| `block_urls` | Protects URLs. |
| `buffer_overflow` | Protects buffer overflow. |
| `content_type` | Protects content type. |
| `htmlchecks` | Specifies a list of security checks to be applied for HTML content types. |
| `cross_site_scripting` | Prevents cross site scripting attacks. |
| `sql_injection` | Prevents SQL injection attacks. |
| `form_field_consistency` | Prevents form tampering. |
| `csrf` | Prevents cross side request forgery (CSRF) attacks. |
| `cookie_consistency` | Prevents cookie tampering or session takeover. |
| `field_format` | Validates the form submission. |
| `fileupload_type` | Prevents malicious file uploads. |
| `jsonchecks` | Specifies security checks for JSON content types. |
| `xmlchecks` | Specifies security checks for XML content types. |
| `wsi` | Protects web services interoperability. |
| `redirect_url` | Redirects URL when block is enabled on protection. |
| `servicenames` |Specifies the services to which the WAF policies are applied. |
| `application_type` | Protects application types. |
| `signatures` | Specifies the location of the external signature file. |
| `html_error_object` | Specifies the location of the customized error page to respond when HTML or common violations are attempted. |
| `xml_error_object` | Specifies the location of the customized error page to respond when XML violations are attempted. |
| `json_error_object` | Specifies the location of the customized error page to respond when JSON violations are attempted. |
| `ip_reputation` | Enables the IP reputation feature. |
| `target` | Determines the traffic to be inspected by the WAF. If you do not specify the traffic targeted, all traffic is inspected by default. |
| `paths` | Specifies the list of HTTP URLs to be inspected. |
| `method` | Specifies the list of HTTP methods to be inspected. |
| `header` | Specifies the list of HTTP headers to be inspected. |


## Deploy WAF CRD

Perform the following steps to deploy the WAF CRD:

1. Download the CRD ([waf-crd.yaml](waf-crd.yaml)).
2. Deploy the WAF CRD using the following command:

        kubectl create -f waf-crd.yaml  

   For example,

    ```
    root@master:~# kubectl create -f waf-crd.yaml
    customresourcedefinition.apiextensions.k8s.io/wafpolicies.citrix.com created
    ```

## How to write a WAF configuration

After you have deployed the WAF CRD provided by Citrix in the Kubernetes cluster, you can define the web application firewall policy configuration in a .yaml file. In the .yaml file, use waf in the kind field. In the spec section add the WAF CRD attributes based on your requirements for the policy configuration.

After you deploy the .yaml file, the Citrix ingress controller applies the WAF configuration on the Ingress Citrix ADC device.

### Examples

**Enable protection for cross-site scripting and SQL injection attacks**

Consider a scenario in which you want to define and specify a web application firewall policy in the Citrix ADC to enable protection for the cross-site scripting and SQL injection attacks. You can create a .yaml file called `wafhtmlxsssql.yaml` and use the appropriate CRD attributes to define the WAF policy as follows:

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafhtmlxsssql
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_page_url: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        html:
          cross_site_scripting: "on"
          sql_injection: "on"
```

**Apply rules to allow only known content types**

Consider a scenario in which you want to define a web application firewall policy that specifies rules to allow only known content types and block unknown content types. Create a `.yaml` file called `waf-contenttype.yaml` and use the appropriate CRD attributes to define the WAF policy as follows:


```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafcontenttype
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        common:
          content_type: "on"
    relaxations:
        common:
          content_type:
            types:
                - custom_cnt_type
                - image/crd

```

**Protect against known attacks**

The following is an example of a WAF CRD configuration for applying external signatures. You can copy the latest WAF signatures from [Signature Location](https://s3.amazonaws.com/NSAppFwSignatures/SignaturesMapping.xml) to the local web server and provide the location of the copied file as *signature_url*.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafhtmlsigxsssql
spec:
    servicenames:
        - frontend
    application_type: HTML
    signatures: "http://x.x.x.x/crd/sig.xml"
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        html:
          cross_site_scripting: "on"
          sql_injection: "on"

```

**Protect from header buffer overflow attacks and block multiple headers**

The following is an example of a WAF CRD configuration for protecting buffer overflow.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafhdrbufferoverflow
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        common:
          buffer_overflow: "on"
          multiple_headers:
            action: ["block", "log"]
    settings:
        common:
          buffer_overflow:
            max_cookie_len: 409
            max_header_len: 4096
            max_url_len: 1024

```

**Prevent repeated attempts to access random URLs on a web site**

The following is an example of a WAF CRD configuration for providing URL filter rules. You can add URLs to permit under *allow_url* and URLs to deny under *block_url*. The URL can be a regular expression also.

```yml

apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafurlchecks
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    target:
        path:
            - /
    security_checks:
        common:
          allow_url: "on"
          block_url: "on"
    relaxations:
        common:
          allow_url:
            urls:
                - payment.php
                - cover.php
    enforcements:
        common:
          block_url:
            urls:
                - "^[^?]*(passwd|passwords?)([.][^/?]*)?([?].*)?$"
                - "^[^?]*(htaccess|access_log)([.][^/?]*)?([~])?([?].*)?$"
```

**Prevent leakage of sensitive data**

Data breaches involve leakage of sensitive data such as credit card and social security number (SSN). You can add custom regexes for the sensitive data in the *Enforcements safe objects* section.

The following is an example of a WAF CRD configuration for preventing leakage of sensitive data.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafdataleak
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        common:
          credit_card: "on"
    settings:
        common:
          credit_card:
            card_type: ["visa","amex"]
            max_allowed: 1
            card_xout: "on"
            secure_logging: "on"
    enforcements:
        common:
          safe_object:
            - rule:
                name: aadhar
                expression: "[1-9]{4,4}\s[1-9]{4,4}\s[1-9]{4,4}"
                max_match_len: 19
                action: ["log","block"]
```

**Protect HTML forms from CSRF and form attacks**

The following is an example of a WAF CRD configuration for protecting HTML forms from CSRF and form attacks.


```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafforms
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_error_object: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        html:
          cross_site_scripting: "on"
          sql_injection: "on"
          form_field_consistency:
            action: ["log","block"]
          csrf: "on"

```

**Protect forms and headers**

The following is an example of a WAF CRD configuration for protecting both forms and headers.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafhdrforms
spec:
    servicenames:
        - frontend
    application_type: HTML
    html_page_url: "http://x.x.x.x/crd/error_page.html"
    security_checks:
        common:
          buffer_overflow: "on"
          multiple_headers:
            action: ["block", "log"]
        html:
          cross_site_scripting: "on"
          sql_injection: "on"
          form_field_consistency:
            action: ["log","block"]
          csrf: "on"
    settings:
        common:
          buffer_overflow:
            max_cookie_len: 409
            max_header_len: 4096
            max_url_len: 1024
    ip_reputation: on


```
**Enable basic WAF security checks**

The basic security checks are required to protect any application with minimal effect on performance. It does not require any sessionization. The following is an example of a WAF CRD configuration for enabling basic WAF security checks.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafbasic
spec:
    servicenames:
        - frontend
    security_checks:
        common:
          allow_url: "on"
          block_url: "on
          buffer_overflow: "on"
          multiple_headers:
            action: ["block", "log"]
        html:
          cross_site_scripting: "on"
          field_format: "on"
          sql_injection: "on"
          fileupload_type: "on"
        json:
          dos: "on"
          sql_injection: "on"
          cross_site_scripting: "on"
        xml:
          dos: "on"
          wsi: "on"
          attachment: "on"
          format: "on"
    relaxations:
        common:
          allow_url:
            urls:
                - "^[^?]+[.](html?|shtml|js|gif|jpg|jpeg|png|swf|pif|pdf|css|csv)$"
                - "^[^?]+[.](cgi|aspx?|jsp|php|pl)([?].*)?$"

```

**Enable advanced WAF security checks**

Advanced security checks such as cookie consistency, allow URL closure, field consistency, and CSRF are resource-intensive (CPU and memory) as they require WAF sessionization. For example, when a form is protected by the WAF, form field information in the response is retained in the system memory. When the client submits the form in the next request, it is checked for inconsistencies before the information is sent to the web server. This process is known as sessionization. The following is an example of a WAF CRD configuration for enabling WAF advanced security checks.


```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafadvanced
spec:
    servicenames:
        - frontend
    security_checks:
        common:
          allow_url: "on"
          block_url: "on"
          buffer_overflow: "on"
          content_type: "on"
          cookie_consistency: "on"
          multiple_headers:
            action: ["log"]
        html:
          cross_site_scripting: "on"
          field_format: "on"
          sql_injection: "on"
          form_field_consistency: "on"
          csrf: "on"
          fileupload_type: "on"
        json:
          dos: "on"
          sql_injection: "on"
          cross_site_scripting: "on"
        xml:
          dos: "on"
          wsi: "on"
          validation: "on"
          attachment: "on"
          format: "on"
    settings:
        common:
          allow_url: 
            closure: "on"
```
**Enable IP reputation**

The following is an example of a WAF CRD configuration for enabling IP reputation to reject requests that come from IP addresses with bad reputation.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafiprep
spec:
    application_type: html
    servicenames:
        - frontend
    ip_reputation: "on"

```
**Enable IP reputation to reject requests of a particular category**

The following is an example of a WAF CRD configuration for enabling IP reputation to reject requests from particular threat categories.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafiprepcategory
spec:
    application_type: html
    servicenames:
        - frontend
    ip_reputation:
        action: block
        threat-categories:
            - SPAM_SOURCES
            - WINDOWS_EXPLOITS
            - WEB_ATTACKS
            - BOTNETS
            - SCANNERS
            - DOS
            - REPUTATION
            - PHISHING
            - PROXY
            - NETWORK
            - CLOUD_PROVIDERS
            - MOBILE_THREATS

```

**Protect JSON applications from denial of service attacks**

The following is an example of a WAF CRD configuration for protecting the JSON applications from denial of service attacks.

```yml
metadata:
    name: wafjsondos
spec:
    servicenames:
        - frontend
    application_type: JSON
    json_error_object: "http://x.x.x.x/crd/error_page.json"
    security_checks:
        json:
          dos: "on"
    settings:
        json:
          dos:
            container:
              max_depth: 2
            document:
              max_len: 20000000
            array:
              max_len: 5
            key:
              max_count: 10000
              max_len: 12
            string:
              max_len: 1000000


```
**Protect RESTful APIs**

The following is an example of a WAF CRD configuration for protecting RESTful APIs from SQL injection, cross-site scripting, and denial of service attacks.
Here, the back-end application or service is purely based on RESTful APIs.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafjson
spec:
    servicenames:
        - frontend
    application_type: JSON
    json_error_object: "http://x.x.x.x/crd/error_page.json"
    security_checks:
        json:
          dos: "on"
          sql_injection:
            action: ["block"]
          cross_site_scripting: "on"
    settings:
        json:
          dos:
            container:
              max_depth: 5
            document:
              max_len: 20000000
            array:
              max_len: 10000
            key:
              max_count: 10000
              max_len: 128
            string:
              max_len: 1000000

```
**Protect XML applications from denial of service attacks**

The following is an example of a WAF CRD configuration for protecting the XML applications from denial of service attacks.

```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafxmldos
spec:
    servicenames:
        - frontend
    application_type: XML
    xml_error_object: "http://x.x.x.x/crd/error_page.xml"
    security_checks:
        xml:
          dos: "on"
    settings:
        xml:
          dos:
            attribute:
                max_attributes: 1024
                max_name_len: 128
                max_value_len: 128
            element:
                max_elements: 1024
                max_children: 128
                max_depth: 128
            file:
                max_size: 2123
                min_size: 9
            entity:
                max_expansions: 512
                max_expansions_depth: 9
            namespace:
                max_namespaces: 16
                max_uri_len: 256
            soaparray:
                max_size: 1111
            cdata:
                max_size: 65

```
**Protect XML applications from security attacks**

This example provides a WAF CRD configuration for protecting XML applications from the following security attacks:

 - SQL injection
 - Cross-site scripting
 - Validation (schema or message)
 - Format
 - Denial of service
 - Web service interoperability (WSI)


```yml
apiVersion: citrix.com/v1
kind: waf
metadata:
    name: wafxml
spec:
    servicenames:
        - frontend
    application_type: XML
    xml_error_object: "http://x.x.x.x/crd/error_page.json"
    security_checks:
        xml:
          dos: "on"
          sql_injection: "on"
          cross_site_scripting: "off"
          wsi:
            action: ["block"]
          validation: "on"
          attachment: "on"
          format:
            action: ["block"]
    settings:
        xml:
          dos:
            attribute:
                max_attributes: 1024
                max_name_len: 128
                max_value_len: 128
            element:
                max_elements: 1024
                max_children: 128
                max_depth: 128
            file:
                max_size: 2123
                min_size: 9
            entity:
                max_expansions: 512
                max_expansions_depth: 9
            namespace:
                max_namespaces: 16
                max_uri_len: 256
            soaparray:
                max_size: 1111
            cdata:
                max_size: 65
          wsi:
            checks: ["R1000","R1003"]
          validation:
            soap_envelope: "on"
            validate_response: "on"
          attachment:
            url:
                max_size: 1111
            content_type:
                value: "crd_test"

```
