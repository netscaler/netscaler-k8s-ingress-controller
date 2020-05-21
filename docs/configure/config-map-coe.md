# Analytics configuration support using ConfigMap

You can use [Citrix Observability Exporter](https://github.com/citrix/citrix-observability-exporter) to export metrics and transactions from Citrix ADC CPX, MPX, or VPX and analyze the exported data to get meaningful insights. The Citrix Observability Exporter support is enabled with in the Citrix ingress controller configuration. You can now enable the Citrix Observability Exporter configuration with in the Citrix ingress controller using a [ConfigMap](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map/).

## Supported environment variables for analytics configuration using ConfigMap

You can configure the following parameters under `NS_ANALYTICS_CONFIG` using a ConfigMap:

- `distributed_tracing`: This variable enables or disables OpenTracing in Citrix ADC and has the following attributes:

  - `enable`:  Set this value to `true` to enable OpenTracing. The default value is `false`.
  - `samplingrate`: Specifies the OpenTracing sampling rate in percentage. The default value is 100.

- `endpoint`: Specifies the IP address or DNS address of the analytics server.
   
    - `server`: Set this value as the IP address or DNS address of the server.
  
- `timeseries`: Enables exporting time series data from Citrix ADC. You can specify the following attributes for time series configuration.
    
    - `port`: Specifies the port number of time series end point of the analytics server. The default value is 5563.
    - `metrics`: Enables exporting metrics from Citrix ADC.
  
       - `enable`: Set this value to `true` to enable sending metrics. The default value is `false`.
       - `mode`: Specifies the mode of metric endpoint. The default value is  `avro`.
    - `auditlogs`: Enables exporting audit log data from Citrix ADC.
       - `enable`: Set this value to `true` to enable audit log data. The default value is `false`.
  
    - `events`: Enables exporting events from the Citrix ADC.
       - `enable`: Set this value to `true` to enable exporting events. The default value is `false`.

- `transactions`: Enables exporting transactions from Citrix ADC.
  
    - `enable`: Set this value to `true` to enable sending transactions. The default value is `false`.
    - `port`: Specifies the port number of transactional endpoint of analytics server. The default value is 5557.

The following configurations cannot be changed while the Citrix ingress controller is running and you need to reboot the Citrix ingress controller to apply these settings.

- server configuration (endpoint)
- port configuration (time series)
- port configuration (transactions)

 You can change other ConfigMap settings at runtime while the Citrix ingress controller is running.

The attributes of `NS_ANALYTICS_CONFIG` should follow a well-defined schema. If any value provided does not confirm with the schema, then the entire configuration is rejected. For reference, see the schema file [ns_analytics_config_schema.yaml](#Schema-for-NSANALYTICSCONFIG).

## Creating a ConfigMap for analytics configuration

This topic provides information on how to create a ConfigMap for analytics configuration.

Create a YAML file `cic-configmap.yaml` with the required key-value pairs in the ConfigMap.

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cic-configmap
  labels:
    app: citrix-ingress-controller
data:
  LOGLEVEL: 'info'
  NS_PROTOCOL: 'http'
  NS_PORT: '80'
  NS_HTTP2_SERVER_SIDE: 'ON'
  NS_ANALYTICS_CONFIG: |
    distributed_tracing:
      enable: 'false'
      samplingrate: 100
    endpoint:
      server: '1.1.1.1'
    timeseries:
      port: 5563
      metrics:
        enable: 'false'
        mode: 'avro'
      auditlogs:
        enable: 'false'
      events:
        enable: 'false'
    transactions:
      enable: 'true'
      port: 5557
```

For more information on how to configure ConfigMap support on the Citrix ingress controller, [see configuring ConfigMap support for the Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map/#configuring-configmap-support-for-the-citrix-ingress-controller).

### Schema for NS_ANALYTICS_CONFIG

Following is the schema for `NS_ANALYTICS_CONFIG`. The attributes should confirm with this schema.

```yml

type: map
mapping:
  NS_ANALYTICS_CONFIG:
    required: no
    type: map
    mapping:
      endpoint:
        required: yes
        type: map
        mapping:
          server:
            required: yes
            type: str
      distributed_tracing:
        required: no
        type: map
        mapping:
          enable:
            required: yes
            type: str
            enum:
              - 'true'
              - 'false'
          samplingrate:
            required: no
            type: int
            range:
              max: 100
              min: 0
      timeseries:
        required: no
        type: map
        mapping:
          port:
            required: no
            type: int
          metrics:
            required: no
            type: map
            mapping:
              enable:
                required: yes
                type: str
                enum:
                  - 'true'
                  - 'false'
              mode:
                required: yes
                type: str
                enum:
                  - prometheus
                  - avro
                  - influx
          auditlogs:
            required: no
            type: map
            mapping:
              enable:
                required: yes
                type: str
                enum:
                  - 'true'
                  - 'false'
          events:
            required: no
            type: map
            mapping:
              enable:
                required: yes
                type: str
                enum:
                  - 'true'
                  - 'false'
      transactions:
        required: no
        type: map
        mapping:
          enable:
            required: yes
            type: str
            enum:
              - 'true'
              - 'false'
          port:
            required: no
            type: int
```
