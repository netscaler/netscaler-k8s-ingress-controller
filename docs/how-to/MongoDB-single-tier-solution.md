# Single tier Citrix Ingress solution for MongoDB

MongoDB is one of the most popular NoSQL databases which is designed to process and store massive amounts of unstructured data. Cloud-native applications widely use MongoDB as a NoSQL database in the Kubernetes platform.

To identify and troubleshoot performance issues are a challenge in a Kubernetes environment due to the massive scale of application deployments. For database deployments like MongoDB, monitoring is a critical component of database administration to ensure that high availability and high performance requirements are met.

Citrix provides an ingress solution for load balancing and monitoring MongoDB databases on a Kubernetes platform using the advanced load balancing and performance monitoring capabilities of Citrix ADCs. Citrix Ingress solution for MongoDB provides you deeper visibility into MongoDB transactions and helps you to quickly identify and address performance issues whenever they occur. Using [Citrix ADC observability exporter](https://github.com/citrix/citrix-observability-exporter), you can export the MongoDB transactions to [Elasticsearch](https://www.elastic.co/products/elasticsearch) and visualize them using [Kibana](https://www.elastic.co/kibana) dashboards to get deeper insights.

The following diagram explains Citrix Ingress solution for MongoDB using a single-tier deployment of Citrix ADC.

![Citrix Ingress solution for MongoDB](../media/mongodb-vpx-deployment.png)

In this solution, a Citrix ADC VPX is deployed outside the Kubernetes cluster (Tier-1) and Citrix ADC observability exporter is deployed inside the Kubernetes cluster.

The Tier-1 Citrix ADC VPX routes the traffic (North-South) from MongoDB clients to Mongo DB query routers (Mongos) in the Kubernetes cluster. Citrix observability exporter is deployed inside the Kubernetes cluster.


As part of this deployment, an Ingress resource is created for Citrix ADC VPX (Tier-1 Ingress). The Tier-1 Ingress resource defines rules to enable load balancing for MongoDB traffic on Citrix ADC VPX and specifies the port for Mongo. Whenever MongoDB traffic arrives on the specified port on a Citrix ADC VPX, it routes this traffic to one of the Mongo service instances mentioned in the Ingress rule. Mongo service is exposed by the MongoDB administrator, and the same service instance is specified in the Ingress.

The Citrix observability exporter instance aggregates transactions from Citrix ADC VPX and uploads them to the Elasticsearch server. You can set up Kibana dashboards to visualize the required data (for example, query response time, most queried collection names) and analyze them to get meaningful insights. Only insert, update, delete, find, and reply operations are parsed and metrics are sent to the Citrix Observability Exporter.

For more information, see [Single tier Citrix Ingress solution for MongoDB](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/how-to/mongodb-solution.html).