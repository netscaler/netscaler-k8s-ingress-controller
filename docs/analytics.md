# Analytics and observability

Analytics from Citrix ADC instances provides you deep-level insights about application performance which helps you to quickly identify issues and take any necessary action.

## Enabling analytics using annotations in the Citrix ingress controller YAML file

You can enable analytics using the analytics profile which is defined as a smart annotation in Ingress or service of type LoadBalancer configuration. You can define the specific parameters you need to monitor by specifying them in the Ingress or service configuration of the application.
The following is a sample Ingress annotation with analytics profile for HTTP records:

`ingress.citrix.com/analyticsprofile: '{"webinsight": {"httpurl":"ENABLED", "httpuseragent":"ENABLED", "httpHost":"ENABLED","httpMethod":"ENABLED","httpContentType":"ENABLED"}}'`

The following is a sample Ingress configuration with the analytics profile for a web application.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/analyticsprofile: '{"webinsight": {"httpurl":"ENABLED", "httpuseragent":"ENABLED",
      "httphost":"ENABLED", "httpmethod":"ENABLED", "httpcontenttype":"ENABLED"}}'
    ingress.citrix.com/insecure-termination: allow
  name: webserver-ingress
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: webserver
            port:
              number: 80
        path: /
        pathType: Prefix
  tls:
  - secretName: name
```

The following is a service annotation:

`service.citrix.com/analyticsprofile: '{"80-tcp":{"webinsight": {"httpurl":"ENABLED", "httpuseragent":"ENABLED"}}}'`

The following is a sample service configuration with the analytics profile which exposes an Apache web application.

```yml
apiVersion: v1
kind: Service
metadata:
  name: apache
  annotations:
    service.citrix.com/csvserver: '{"l2conn":"on"}'
    service.citrix.com/lbvserver: '{"80-tcp":{"lbmethod":"SRCIPDESTIPHASH"}}'
    service.citrix.com/servicegroup: '{"80-tcp":{"usip":"yes"}}'
    service.citrix.com/monitor: '{"80-tcp":{"type":"http"}}'
    service.citrix.com/frontend-ip: "192.0.2.16"
    service.citrix.com/analyticsprofile: '{"80-tcp":{"webinsight": {"httpurl":"ENABLED", "httpuseragent":"ENABLED"}}}'
    NETSCALER_VPORT: "80"
  labels:
    name: apache
spec:
  externalTrafficPolicy: Local
  type: LoadBalancer
  selector:
    name: apache
  ports:
  - name: http
    port: 80
    targetPort: http
  selector:
    app: apache
```
For information about annotations, see the [annotation documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/#smart-annotations-for-services).

## Analytics using Citrix ADM

Citrix ADM provides a comprehensive observability solution including analytics on various events happening in the system and a service graph for monitoring services in an easy to use user interface.

Citrix ADM analytics provide an easy and scalable way to get various insights out of the data from Citrix ADC instances to describe, predict, and improve the application performance. You can use one or more analytics features simultaneously on Citrix ADM. For more information on the service graph, see the [service graph documentation](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/application-analytics-and-management/service-graph.html).

To use the ADM analytics or service graph:

- You must install an ADM agent and ensure the communication between Citrix ADM and Kubernetes cluster or managed instances in your data center or cloud. It makes Citrix ADC instances discoverable by Citrix ADM.
- Ensure that an appropriate license is available and auto licensing is enabled on ADM. 

## Analytics with open source tools

Citrix ADC can be integrated with various open source tools for observability using Citrix observability exporter. Citrix observability exporter is a container which collects metrics and transactions from Citrix ADCs and transforms them to suitable formats (such as JSON, AVRO) for supported endpoints. You can export the collected data to the desired endpoint. By analyzing the data, you can get valuable insights at a microservice level for applications proxied by Citrix ADCs.
For more information on Citrix ADC observability exporter, see the [Citrix ADC observability exporter documentation](https://developer-docs.citrix.com/projects/citrix-observability-exporter/en/latest/).
