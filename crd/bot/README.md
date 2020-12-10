# Configure bot management policies with the Citrix ingress controller

A bot is a software application that automates manual tasks. Using bot management policies you can allow useful bots to access your cloud native environment and block the malicious bots.

Custom Resource Definitions (CRDs) are the primary way of configuring policies in cloud native deployments. Using the Bot CRD provided by Citrix, you can configure the bot management policies with the Citrix ingress controller on the Citrix ADC VPX. The Bot CRD enables communication between the Citrix ingress controller and Citrix ADC for enforcing bot management policies.

In a Kubernetes deployment, you can enforce bot management policy on the requests and responses from and to the server using the Bot CRD. For more information on security vulnerabilities, see [Bot Detection](https://docs.citrix.com/en-us/citrix-adc/current-release/bot-management/bot-detection.html).

With the Bot CRD, you can configure the bot management security policy for the following types of security vulnerabilities for the Kubernetes-native applications:

**Protections:**

-  Allow list
-  Block list
-  Device Fingerprint (DFP)
-  Bot TPS
-  Trap insertion
-  IP reputation
-  Rate limit

Based on the type of protections required, you can specify the metadata and use the CRD attributes in the Bot CRD `.yaml` file to define the bot policy.
 
## Bot CRD definition

The Bot CRD is available in the Citrix ingress controller GitHub repo at [bot-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/bot/bot-crd.yaml). The Bot CRD provides attributes for the various options that are required to define the bot management policies on Citrix ADC.

The following is the Bot CRD definition:

```yml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: bots.citrix.com
spec:
  group: citrix.com
  version: v1
  names:
    kind: bot
    plural: bots
    singular: bot
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
              description: 'Name of the services to which the bot policies are applied.'
              type: array
              items:
                type: string
                maxLength: 127
            signatures:
              description: 'Location of external bot signature file'
              type: string
            redirect_url:
              description: 'url to redirect when bot violation is hit'
              type: string
            target:
              description: 'To control what traffic to be inspected by BOT. If you do not provide the target, everything will be inspected by default'
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
                    enum: ['GET', 'PUT', 'POST','DELETE']
                header:
                  type: array
                  description: "List of http headers to inspect"
                  items:
                    type: string
                    description: "header name"
            security_checks:
              description: 'To enable/disable bot ecurity checks'
              type: object
              properties:
                allow_list:
                  type: string
                  enum: ['ON', 'OFF']
                block_list:
                  type: string
                  enum: ['ON', 'OFF']
                device_fingerprint:
                  oneOf:
                    - type: string
                      enum: ['ON', 'OFF']
                    - type: object
                      properties:
                        action:
                          type: array
                          items:
                            type: string
                reputation:
                  type: string
                  enum: ['ON', 'OFF']
                ratelimit:
                  type: string
                  enum: ['ON', 'OFF']
                tps:
                  type: string
                  enum: ['ON', 'OFF']
                trap:
                  oneOf:
                    - type: string
                      enum: ['ON', 'OFF']
                    - type: object
                      properties:
                        action:
                          type: array
                          items:
                            type: string
            relaxations:
              description: 'Section which contains binding rules for bot security checks'
              type: object
              properties:
                allow_list:
                  type: array
                  items:
                    type: object
                    properties:
                      subnet:
                        type: object
                      ip:
                        type: object
                      expression:
                        type: object
 
                block_list:
                  type: array
                  items:
                    type: object
                    properties:
                      subnet:
                        type: object
                      ip:
                        type: object
                      expression:
                        type: object
                ratelimit:
                  type: array
                  items:
                    type: object
                    properties:
                      url:
                        type: object
                      ip:
                        type: object
                      cookie:
                        type: object
                reputation:
                  type: object
                  properties:
                    categories:
                      oneOf:
                        - type: string
                        - type: object
                captcha:
                  type: array
                tps:
                  type: object
                  properties:
                    geolocation:
                      type: object
                    host:
                      type: object
                    ip:
                      type: object
                    host:
                      type: object
                trap:
                  type: object
 
```

## Bot CRD attributes

The following table lists the various attributes provided in the Bot CRD:

| CRD attribute | Description |
| ---------- | ----------- |
| `security_checks` | List of security checks to be applied for incoming traffic. |
| `allow_list` | List of allowed IP, subnet, and policy expressions. |
| `block_list` | List of disallowed IP, subnet, and policy expressions. |
| `device_fingerprint` | Inserts javascript and collects the client browser and device parameters. |
| `trap` | Inserts hidden URLs in the response. |
| `tps` | Prevents bots which cause unusual spike in requests based on configured percentage change in transactions.  |
| `reputation` | Prevents access to bad IPs based on configured reputation categories. |
| `ratelimit` | Prevents bots based on rate limit. |
| `redirect_url` | Redirect URL when block is enabled on protection. |
| `servicenames` | Name of the services to which the bot policies are applied. |
| `signatures` | Location of external bot signature file. |
| `target` | Determines which traffic to be inspected by the bot. If you do not specify the traffic targeted, every traffic is inspected by default. |
| `paths` | List of HTTP URLs to be inspected. |
| `method` | List of HTTP methods to be inspected. |
| `header` | List of HTTP headers to be inspected. |

## Deploy the Bot CRD

Perform the following steps to deploy the Bot CRD:

1. Download the CRD (bot-crd.yaml).
2. Deploy the Bot CRD using the following command:

`kubectl create -f bot-crd.yaml`

For example,

```
root@master:~# kubectl create -f bot-crd.yaml
customresourcedefinition.apiextensions.k8s.io/bots.citrix.com created
```
## How to write a Bot configuration

After you have deployed the Bot CRD provided by Citrix in the Kubernetes cluster, you can define the bot management policy configuration in a YAML file. In the YAML file, specify bot in the kind field. In the spec section, add the Bot CRD attributes based on your requirements for the policy configuration.

After you deploy the YAML file, the Citrix ingress controller applies the bot configuration on the Ingress Citrix ADC device.

**Examples**

**Block malicious traffic using known IP, subnet, or ADC policy expressions**

When you want to define and employ a web bot management policy in Citrix ADC to enable bot for blocking malicious traffic, you can create a YAML file called `botblocklist.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: botblocklist
spec:
    servicenames:
        - frontend
    security_checks:
        block_list: "ON"
    bindings:
        block_list:
            - subnet:
                value:
                    - 172.16.1.0/12
                    - 172.16.2.0/12
                    - 172.16.3.0/12
                    - 172.16.4.0/12
                action:
                    - "drop"
            - ip:
                value: 10.102.30.40
            - expression:
                value:  http.req.url.contains("/robots.txt")
                action:
                    - "reset"
                    - "log"
```

**Allow known traffic without bot security checks**

When you want to avoid security checks for certain traffic such as staging or trusted traffic, you can avoid such traffic from security checks. You can create a YAML file called `botallowlist.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: botallowlist
spec:
    servicenames:
        - frontend
    security_checks:
        allow_list: "ON"
    bindings:
        allow_list:
            - subnet:
                value:
                    - 172.16.1.0/12
                    - 172.16.2.0/12
                    - 172.16.3.0/12
                    - 172.16.4.0/12
                action:
                    - "log"
            - ip:
                value: 10.102.30.40
            - expression:
                value:  http.req.url.contains("index.html")
                action:
                    - "log"
```

**Enable bot signatures to detect bots**

Citrix provides thousands of inbuilt signatures to detect bots based on user agents. Citrix threat intelligence team keeps on updating and releasing new bot signatures in every two weeks. The latest bot signature file is available at: [Bot signatures](https://nsbotsignatures.s3.amazonaws.com/BotSignatureMapping.json). You can create a YAML file called `botsignatures.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: botsignatures
spec:
    servicenames:
        - frontend
    redirect_url: "/error_page.html"
    signatures: "http://10.106.102.242/ganeshka/bot_sig.json"
```

**Enable the bot device fingerprint and customize the action**

Device fingerprinting involves inserting a JavaScript snippet in the HTML response to the client. This JavaScript snippet, when invoked by the browser on the client, collects the attributes of the browser and client. And sends a POST request to Citrix ADC with that information. These attributes are examined to determine whether the connection is requested from a bot or a human being. You can create a YAML file called `botdfp.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: botdfp
spec:
    servicenames:
        - frontend
    redirect_url: "/error_page.html"
    security_checks:
       device_fingerprint:
           action:
               - "log"
               - "drop"
```

**Enable the bot TPS and customize the action**

If the bot TPS is configured, it detects incoming traffic as bots if the maximum number of requests or increase in requests exceeds the configured time interval. You can configure the TPS limits as per *geolocation*, *host*, *source IP*, and *URL* in the *bindings* section. You can create a YAML file called `bottps.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: bottps
spec:
    servicenames:
        - frontend
    redirect_url: "/error_page.html"
    security_checks:
        tps: "ON"
    bindings:
        tps:
            geolocation:
                threshold: 101
                percentage: 100
            host:
                threshold: 10
                percentage: 100
                action:
                    - "log"
                    - "mitigation"
```

**Enable the trap insertion protection and customize the action**

Detects and blocks automated bots by advertising a trap URL in the client response. The URL is invisible and not accessible to the client, if it is human. The detection method is effective in blocking attacks from automated bots. Insertion of the trap URL in the URL responses is random. You can enforce the trap URL insertion to a particular URL response by configuring the trap bindings. You can create a YAML file called `trapinsertion.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: trapinsertion
spec:
    servicenames:
        - frontend
    redirect_url: "/error_page.html"
    security_checks:
       trap: ["log","drop"]
         bindings:
      trap:
      urls:
          - "/index.html"
        - "/submit.php"
        - "/login.html"

```

**Enable IP reputation to reject requests of a particular category**

The following is an example of a Bot CRD configuration for enabling only specific threat categories of IP reputation that are suitable for the user environment. You can create a YAML file called `botiprepcategory.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
    name: botiprepcategory
spec:
    servicenames:
        - frontend
    redirect_url: "/error_page.html"
    security_checks:
       reputation: "ON"
    bindings:
      reputation:
        categories: 
            - SPAM_SOURCES:
                action:
                    - "log"
                    - "redirect"
            - MOBILE_THREATS
            - SPAM_SOURCES
```
**Enable rate limit to control request rate**

The following is an example of a Bot CRD configuration for enforcing the request rate limit using the parameters: URL, cookies, and IP. You can create a YAML file called `botratelimit.yaml` and use the appropriate CRD attributes to define the bot policy as follows:

```yml
apiVersion: citrix.com/v1
kind: bot
metadata:
  name: botratelimit
spec:
  servicenames:
    - frontend
  redirect_url: "/error_page.html"
  security_checks:
    ratelimit: "ON"
  bindings:
    ratelimit:
      - url:
          value: index.html
          rate: 2000
          timeslice: 1000
      - cookie:
          value: citrix_bot_id
          rate: 2000
          timeslice: 1000
      - ip:
          rate: 2000
          timeslice: 1000
          action:
              - "log"
              - "reset"
```