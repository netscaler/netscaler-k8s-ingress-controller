# Exporting metrics directly to Prometheus

NetScaler ingress controller now supports exporting metrics directly from NetScaler to Prometheus. 
With NetScaler ingress controller, you can automate the configurations required on NetScaler for exporting metrics directly.

Once you export the metrics, you can visualize the exported NetScaler metrics for easier interpretation and understanding using tools such as Grafana.

## Configuring direct export of metrics from NetScaler CPX to Prometheus

To enable NetScaler ingress controller to configure NetScaler CPX to support direct export of metrics to Prometheus, you need to perform the following steps:

1.  Create a Kubernetes secret to enable read-only access for a user. This step is required for NetScaler CPX to export metrics to Prometheus.

        kubectl create secret generic prom-user --from-literal=username=<prometheus-username> --from-literal=password=<prometheus-password>

2.  Deploy NetScaler CPX with NetScaler ingress controller using the following Helm commands:

        helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

        helm install my-release netscaler/netscaler-cpx-with-ingress-controller --set license.accept=yes,nsic.prometheusCredentialSecret=<Secret-for-read-only-user-creation>,analyticsConfig.required=true,analyticsConfig.timeseries.metrics.enable=true,analyticsConfig.timeseries.port=5563,analyticsConfig.timeseries.metrics.mode=prometheus,analyticsConfig.timeseries.metrics.enableNativeScrape=true

    The new parameters specified in the command are explained as follows:

    -  `nsic.prometheusCredentialSecret`: Specifies the Kubernetes secret name for creating the read only user for native Prometheus support.
    -  `analyticsConfig.timeseries.metrics.enableNativeScrape`: Set this value to `true` for directly exporting metrics to Prometheus

3.  Add a new Prometheus job under `scrape_configs` in the [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) to configure Prometheus for directly exporting from a NetScaler CPX pod. For more information, see [kubernetes_sd_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config). A sample Prometheus job is given as follows:

    ```
            - job_name: 'kubernetes-cpx'
            scheme: http
            metrics_path: /nitro/v1/config/systemfile
            params:
                args: ['filename:metrics_prom_ns_analytics_time_series_profile.log,filelocation:/var/nslog']
                format: ['prometheus']
            basic_auth:
                username:  # Prometheus username set in nsic.prometheusCredentialSecret
                password:  # Prometheus password set in nsic.prometheusCredentialSecret
            scrape_interval: 30s
            kubernetes_sd_configs:
            - role: pod
            relabel_configs:
            - source_labels: [__meta_kubernetes_pod_annotation_netscaler_prometheus_scrape]
                action: keep
                regex: true
            - source_labels: [__address__, __meta_kubernetes_pod_annotation_netscaler_prometheus_port]
                action: replace
                regex: ([^:]+)(?::\d+)?;(\d+)
                replacement: $1:$2
                target_label: __address__
            - source_labels: [__meta_kubernetes_namespace]
                action: replace
                target_label: kubernetes_namespace
            - source_labels: [__meta_kubernetes_pod_name]
                action: replace
                target_label: kubernetes_pod_name
    ```

**Note:**
For more information on Prometheus integration, see the [NetScaler Prometheus integration documentation](https://docs.netscaler.com/en-us/citrix-adc/current-release/observability/prometheus-integration).

## Configuring direct export of metrics from NetScaler VPX or MPX to Prometheus

To enable NetScaler ingress controller to configure NetScaler VPX or MPX to support direct export of metrics to Prometheus, you need to perform the following steps:

1.  Deploy NetScaler ingress controller as a stand-alone pod using the Helm command:

        helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

        helm install my-release netscaler/citrix-cloud-native --set cic.enabled=true,cic.nsIP=<NSIP>,cic.license.accept=yes,cic.adcCredentialSecret=<Secret-for-NetScaler-credentials>,cic.analyticsConfig.required=true,cic.analyticsConfig.timeseries.metrics.enable=true,cic.analyticsConfig.timeseries.port=5563,cic.analyticsConfig.timeseries.metrics.mode=prometheus,cic.analyticsConfig.timeseries.metrics.enableNativeScrape=true

2.  Create a system user with read only access for NetScaler VPX. For more details on the user creation, see the [NetScaler Prometheus integration documentation](https://docs.netscaler.com/en-us/citrix-adc/current-release/observability/prometheus-integration#configure-read-only-prometheus-access-for-a-non-super-user).

3.  Add a scrape job under `scrape_configs` in the prometheus [configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) for enabling Prometheus to scrape from NetScaler VPX. For a sample Prometheus scrape job, see [Prometheus configuration](https://docs.netscaler.com/en-us/citrix-adc/current-release/observability/prometheus-integration#prometheus-configuration).

**Note:**
The scrape configuration section specifies a set of targets and configuration parameters describing how to scrape them. For more information on NetScaler specific parameters used in the configuration, see the [NetScaler documentation](https://docs.netscaler.com/en-us/citrix-adc/current-release/observability/prometheus-integration#install-and-configure-prometheus-for-metrics-export-from-netscaler).
