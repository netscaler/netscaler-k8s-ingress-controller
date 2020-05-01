# Troubleshooting

The following table describes some of the common issues and workarounds.

|**Problem**|**Log**|**Workaround**|
|------|-----|-----|
|Citrix ADC instance is not reachable|**2019-01-10 05:05:27,250 - ERROR - [nitrointerface.py:login_logout:94] (MainThread) Exception: HTTPConnectionPool(host='10.106.76.200', port=80): Max retries exceeded with url: /nitro/v1/config/login (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4d45bd63d0>: Failed to establish a new connection: [Errno 113] No route to host',))**|Ensure that Citrix ADC is up and running, and you can ping the NSIP address.|
|Wrong user name password|**2019-01-10 05:03:05,958  - ERROR - [nitrointerface.py:login_logout:90] (MainThread) Nitro Exception::login_logout::errorcode=354,message=Invalid username or password**| |
|SNIP is not enabled with management access|**2019-01-10 05:43:03,418  - ERROR - [nitrointerface.py:login_logout:94] (MainThread) Exception: HTTPConnectionPool(host='10.106.76.242', port=80): Max retries exceeded with url: /nitro/v1/config/login (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f302a8cfad0>: Failed to establish a new connection: [Errno 110] Connection timed out',))**|Ensure that you have enabled the management access in Citrix ADC (for Citrix ADC VPX high availability) and set the IP address, **NSIP**, with management access enabled.|
|Error while parsing annotations|**2019-01-10 05:16:10,611 - ERROR - [kubernetes.py:set_annotations_to_csapp:1040] (MainThread) set_annotations_to_csapp: Error message=No JSON object could be decodedInvalid Annotation $service_weights please fix and apply ${"frontend":, "catalog":95}**| |
|Wrong port for NITRO access|**2019-01-10 05:18:53,964 - ERROR - [nitrointerface.py:login_logout:94] (MainThread) Exception: HTTPConnectionPool(host='10.106.76.242', port=34438): Max retries exceeded with url: /nitro/v1/config/login (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fc592cb8b10>: Failed to establish a new connection: [Errno 111] Connection refused',))**|Verify if the correct port is specified for NITRO access. By default, Citrix ingress controller uses port **80** for communcation.|
| Ingress class is wrong|**2019-01-10 05:27:27,149  - INFO - [kubernetes.py:get_all_ingresses:1329] (MainThread) Unsupported Ingress class for ingress object web-ingress.default**|Verify that the ingress file belongs to the ingress class that Citrix ingress controller monitors.|
| | | See the following log for information about the ingress classes listened by Citrix ingress controller:|
| | |Log: 2019-01-10 05:27:27,120 - DEBUG - [kubernetes.py:__init__:63] (MainThread) Ingress classes allowed:|
| | |2019-01-10 05:27:27,120 - DEBUG - [kubernetes.py:__init__:64] (MainThread) ['vpxclass']|
|Kubernetes API is not reachable|**2019-01-10 05:32:09,729  - ERROR - [kubernetes.py:_get:222] (Thread-1) Error while calling /services:HTTPSConnectionPool(host='10.106.76.237', port=6443): Max retries exceeded with url: /api/v1/services (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7fb3013e7dd0>: Failed to establish a new connection: [Errno 111] Connection refused',))**| Check if the kubernetes_url is correct. Use the command, `kubectl cluster-info` to get the URL information. Ensure that the Kubernetes master is running at `https://kubernetes_master_address:6443` and also the Kubernetes API server pod is up and running. |
| Incorrect service port specified in the YAML file| |Provide the correct port details in the ingress YAML file and reapply to solve the issue. |
|Load balancing virtual server and service group are created but they are down| |Check for the service name and port used in the YAML file. For Citrix ADC VPX, ensure that `--feature-node-watch` is set to `true`, when bringing up the Citrix ingress controller.|
|CS virtual server is not getting created for Citrix ADC VPX.| |Use the annotation, `ingress.citrix.com/frontend-ip`, in the ingress YAML file for Citrix ADC VPX.|
|Incorrect secret provided in TLS section in the ingress YAML file|**2019-01-10 09:30:50,673 - INFO - [kubernetes.py:_get:231] (MainThread) Resource not found: /secrets/default-secret12345 namespace default**| |
| |**2019-01-10 09:30:50,673 - INFO - [kubernetes.py:get_secret:1712] (MainThread) Failed to get secret for the app default-secret12345.default**|Correct the values in the YAML file and reapply to solve the issue.|

## Troubleshooting - Prometheus and Grafana Integration

|**Problem**|**Description**|**Workaround**|
|------|-----|-----|
|Grafana dashboard has no plots|If the graphs on the Grafana dashboards do not have any values plotted, then Grafana is unable to obtain statistics from its datasource.| Check if the Prometheus datasource is saved and working properly. On saving the datasource after providing the Name and IP, a "Data source is working" message appears in green indicating the datasource is reachable and detected.
| | |If the dashboard is created using `sample_grafana_dashboard.json`, ensure that the name given to the Prometheus datasource begins with the word "prometheus" in lowercase.|
| | | Check the Targets page of Prometheus to see if the required target exporter is in `DOWN` state.|
| DOWN: Context deadline exceeded| If the message appears against any of the exporter targets of Prometheus, then Prometheus is either unable to connect to the exporter or unable to fetch all the metrics within the given `scrape_timeout`.|If you are using Prometheus Operator, `scrape_timeout` is adjusted automatically and the error means that the exporter itself is not reachable.|
| | |If a standalone Prometheus container or pod is used, try increasing the `scrape_interval` and `scrape_timeout` values in the `/etc/prometheus/prometheus.cfg` file to increase the time interval for collecting the metrics.|