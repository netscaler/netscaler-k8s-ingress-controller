# Rate limiting in Kubernetes using Netscaler

In a Kubernetes deployment, you can rate limit the requests to the resources on the back end server or services using [rate limiting](https://docs.citrix.com/en-us/citrix-adc/13/appexpert/rate-limiting.html) feature provided by the ingress Netscaler.

Citrix provides a Kubernetes [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) called the **Rate limit CRD** that you can use with the Netscaler ingress controller to configure the rate limiting configurations on the Netscalers used as Ingress devices.

Apart from rate limiting the requests to the services in a Kubernetes environment, you can use the Rate limit CRD for API security as well. The Rate limit CRD allows you to limit the REST API request to API servers or specific API endpoints on the API servers. It monitors and keeps track of the requests to the API server or endpoints against the allowed limit per time slice and hence protects from attacks such as the DDoS attack.

You can enable logging for observability with the rate limit CRD. Logs are stored on Netscaler which can be viewed by checking the logs using the shell command. The file location is based on the syslog configuration. For example, `/var/logs/ns.log`.

## Rate limit CRD definition

The Rate limit CRD spec is available in the Netscaler ingress controller GitHub repo at: [ratelimit-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/ratelimit/ratelimit-crd.yaml). The **Rate limit CRD provides** [attributes](#ratelimit-crd-attributes) for the various options that are required to define the rate limit policies on the Ingress Netscaler that acts as an API gateway.


## Rate limit CRD attributes

The following table lists the various attributes provided in the Rate limit CRD:

| CRD attribute | Description |
| ---------- | ----------- |
| `servicename` | The list of Kubernetes services to which you want to apply the rate limit policies. |
| `selector_keys` | The traffic selector keys that filter the traffic to identify the API requests against which the throttling is applied and monitored. </br> </br>**Note:** The `selector_keys` is an optional attribute. You can choose to configure zero, one or more of the selector keys. If more than one selector keys are configured then it is considered as a logical AND expression.</br></br> In this version of the Rate limit CRD, `selector_keys` provides the `basic` configuration section that you can use to configure the following commonly used traffic characteristics as the keys against which the configured limits are monitored and throttled:</br></br> - **path:** An array of URL path prefixes that refer to a specific API endpoint. For example, `/api/v1/products/` </br> - **method:** An array of HTTP methods. Allowed values are GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE or CONNECT. </br> - **header_name:** HTTP header that has the unique API client or user identifier. For example, `X-apikey` which comes with a unique API-key that identifies the API client sending the request. </br>- **per_client_ip:** Allows you to monitor and apply the configured threshold to each API request received per unique client IP address. |
| `req_threshold` | The maximum number of requests that are allowed in the given time slice (request rate). |
| `timeslice` | The time interval specified in microseconds (multiple of 10 s), during which the requests are monitored against the configured limits. If not specified it defaults to 1000 milliseconds. |
| `limittype` | It allows you to configure the following type of throttling algorithms that you want to use to apply the limit: </br> - burst </br> - smooth.  The default is the ***burst*** mode.
| `throttle_action` | It allows you to define the throttle action that needs to be taken on the traffic that's throttled for crossing the configured threshold. </br></br> The following are the throttle action that you can define: </br> - **DROP:** Drops the requests above the configured traffic limits. </br>- **RESET:** Resets the connection for the requests crossing the configured limit. </br> - **REDIRECT:** Redirects the traffic to the configured `redirect_url`. </br> - **RESPOND:** Responds with the standard "***429 Too many requests***" response. |
| `redirect_url` | This attribute is an optional attribute that is required only if `throttle_action` is configured with the value `REDIRECT`. |
| `logpackets` | Enables audit logs. |
| `logexpression` | Specifies the default-syntax expression that defines the format and content of the log message. |
| `loglevel` | Specifies the severity level of the log message that is generated. |

## Deploy the Rate limit CRD

Perform the following to deploy the Rate limit CRD:

1.  Download the CRD ([ratelimit-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/ratelimit/ratelimit-crd.yaml)).

1.  Deploy the Rate limit CRD using the following command:

        kubectl create -f ratelimit-crd.yaml

    For example,

        root@master:~# kubectl create -f ratelimit-crd.yaml

        customresourcedefinition.apiextensions.k8s.io/ratelimits.citrix.com created

        root@master:~# kubectl get crd

        NAME CREATED AT
        ratelimits.citrix.com 2019-08-27T01:06:30Z

## How to write a rate-based policy configuration

After you have deployed the CRD provided by Citrix in the Kubernetes cluster, you can define the rate-based policy configuration in a `.yaml` file. In the `.yaml` file, use `ratelimit` in the `kind` field and in the `spec` section add the Rate limit CRD attributes based on your requirement for the policy configuration.

After you deploy the `.yaml` file, the Netscaler ingress controller applies the rate-based policy configuration on the Ingress Netscaler device.

### Examples

#### Limit API requests to configured API endpoint prefixes

Consider a scenario wherein you want to define a rate-based policy in Netscaler to limit the API requests to 15 requests per minute from each unique client IP address to the configured API endpoint prefixes. Create a `.yaml` file called `ratelimit-example1.yaml` and use the appropriate CRD attributes to define the rate-based policy as follows:

```yml
apiVersion: citrix.com/v1beta1
kind: ratelimit
metadata:
  name: throttle-req-per-clientip
spec:
  servicenames:
    - frontend
  selector_keys:
   basic:
    path:
     - "/api/v1/products"
     - "/api/v1/orders/"
    per_client_ip: true
  req_threshold: 15
  timeslice: 60000
  throttle_action: "RESPOND"
  logpackets:
    logexpression: "http.req.url"
    loglevel: "INFORMATIONAL"
```

>**Note:**
>
> You can initiate multiple Kubernetes objects for different paths that require different rate limit configurations.

After you have defined the policy configuration, deploy the `.yaml` file using the following command:

    root@master:~#kubectl create -f ratelimit-example1.yaml
    ratelimit.citrix.com/throttle-req-per-clientip created

The Netscaler ingress controller applies the policy configuration on the Ingress Netscaler device.

#### Limit API requests to calender APIs

Consider a scenario wherein you want to define a rate-based policy in a Netscaler to limit the API requests (GET or POST) to five requests from each API client identified using the HTTP header `X-API-Key` to the calender APIs. Create a `.yaml` file called `ratelimit-example2.yaml` and use the appropriate CRD attributes to define the rate-based policy as follows:

```yml
apiVersion: citrix.com/v1beta1
kind: ratelimit
metadata:
  name: throttle-calendarapi-perapikey
spec:
  servicenames:
    - frontend
  selector_keys:
    basic:
      path:
        - "/api/v1/calender"
      method:
        - "GET"
        - "POST"
      header_name: "X-API-Key"
  req_threshold: 5
  throttle_action: "RESPOND"
  logpackets:
    logexpression: "rate exceeded, you may want to configure higher limit"
    loglevel: "INFORMATIONAL"
```

After you have defined the policy configuration, deploy the `.yaml` file using the following command:

    root@master:~#kubectl create -f ratelimit-example2.yaml
    ratelimit.citrix.com/throttle-req-per-clientip created

The Netscaler ingress controller applies the policy configuration on the Ingress Netscaler device.