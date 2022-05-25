# Enable request retry feature using AppQoE for Citrix ingress controller

When a Citrix ADC appliance receives an HTTP request and forwards it to a back-end server, sometimes there may be connection failures with the back-end server. You can configure the request-retry feature on Citrix ADC to forward the request to the next available server, instead of sending the reset to the client. Hence, the client saves round trip time when Citrix ADC initiates the same request to the next available service. For more information request retry feature, see the [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/system/request-retry/request_retry_if_back-end_server_resets_tcp_connection.html)

Now, you can configure request retry on Citrix ADC with Citrix ingress controller.
Custom Resource Definitions (CRDs) are the primary way of configuring policies in cloud native deployments. Using the AppQoE CRD provided by Citrix, you can configure request-retry policies on Citrix ADC with the Citrix ingress controller. The AppQoE CRD enables communication between the Citrix ingress controller and Citrix ADC for enforcing AppQoE policies.

## AppQoE CRD definition

The AppQoE CRD is available in the Citrix ingress controller GitHub repo at: [appqoe-crd.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/appqoe/appqoe-crd.yaml). The AppQoE CRD provides attributes for the various options that are required to define the AppQoE policy on Citrix ADC.

The following are the attributes provided in the AppQoE CRD:

| Attribute | Description |
| --------- | ----------- |
| `servicenames` | Specifies the list of Kubernetes services to which you want to apply the AppQoE policies.|
| `on-reset`|  Specifies whether to set retry on connection Reset or Not|
| `on-timeout` | Specifies the time in milliseconds for retry |
| `number-of-retries`| Specifies the number of retries |
| `appqoe-criteria`|Specifies the expression for evaluating traffic. |
| `direction`| Specifies the bind point for binding the AppQoE policy. |

## Deploy the AppQoE CRD

Perform the following to deploy the AppQoE CRD:

1.  Download the [AppQoE CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/appqoe/appqoe-crd.yaml).

2.  Deploy the AppQoE CRD using the following command:

        kubectl create -f appqoe-crd.yaml

### How to write a AppQoE policy configuration

After you have deployed the AppQoE CRD provided by Citrix in the Kubernetes cluster, you can define the AppQoE policy configuration in a `.yaml` file. In the `.yaml` file, use `appqoepolicy` in the kind field and in the `spec` section add the AppQoE CRD attributes based on your requirement for the policy configuration.

The following YAML file applies the AppQoE policy to the services listed in the servicenames field. You must configure the AppQoE action to retry on timeout and define the number of retry attempts.

```yml
apiVersion: citrix.com/v1
kind: appqoepolicy
metadata:
  name: targeturlappqoe
spec:
  appqoe-policies:
    - servicenames:
        - apache
      appqoe-policy:
        operation-retry:
          onReset: 'YES'
          onTimeout: 33
        number-of-retries: 2
        appqoe-criteria: 'HTTP.REQ.HEADER("User-Agent").CONTAINS("Android")'
        direction: REQUEST
```

After you have defined the policy configuration, deploy the `.yaml` file using the following commands:

   $ kubectl create -f appqoe-example.yaml
