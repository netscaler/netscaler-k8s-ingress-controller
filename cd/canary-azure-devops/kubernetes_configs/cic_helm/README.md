# Citrix Ingress Controller

[Citrix](https://www.citrix.com/en-in/) provides an Ingress Controller for Citrix ADC MPX (hardware), Citrix ADC VPX (virtualized), and [Citrix ADC CPX](https://docs.citrix.com/en-us/citrix-adc-cpx/13/about.html) (containerized) for [bare metal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments. It configures one or more Citrix ADC based on the Ingress resource configuration in [Kubernetes](https://kubernetes.io/) or in [OpenShift](https://www.openshift.com) cluster.

## TL;DR;

### For Kubernetes
   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>
   ```

   To install Citrix Provided Custom Resource Definition(CRDs) along with Citrix Ingress Controller
   ```
   helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,crds.install=true
   ``` 

### For OpenShift

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,openshift=true
   ```

   To install Citrix Provided Custom Resource Definition(CRDs) along with Citrix Ingress Controller
   ```
   helm install cic citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,openshift=true,crds.install=true
   ``` 

> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the Citrix license.

## Introduction
This Helm chart deploys Citrix ingress controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 3.11.x or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You determine the NS_IP IP address needed by the controller to communicate with Citrix ADC. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).

-  You have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator), if you want to view the metrics of the Citrix ADC CPX collected by the [metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics).

-  The user name and password of the Citrix ADC VPX or MPX appliance used as the ingress device. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

    You can pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'
    ```

#### Create system User account for Citrix ingress controller in Citrix ADC

Citrix ingress controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission configure the following on the Citrix ADC:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Cofigure SSl certkeys
-  Configure routes
-  Configure user monitors
-  Add system file (for uploading SSL certkeys from Kubernetes)
-  Configure Virtual IP address (VIP)
-  Check the status of the Citrix ADC appliance

> **Note:**
>
> The system user account would have privileges based on the command policy that you define.

To create the system user account, do the following:

1.  Log on to the Citrix ADC appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.

    2.  Log on to the appliance by using the administrator credentials.

2.  Create the system user account using the following command:

    ```
       add system user <username> <password>
    ```

    For example:

    ```
       add system user cic mypassword
    ```

3.  Create a policy to provide required permissions to the system user account. Use the following command:

        add cmdpolicy cic-policy ALLOW '^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)'

    **Note**: The system user account would have privileges based on the command policy that you define.
    The command policy mentioned in ***step 3*** is similar to the built-in `sysAdmin` command policy with additional permission to upload files.
    For more information on command policy, see the [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/system/authentication-and-authorization-for-system-user/user-usergroups-command-policies.html#configure-command-policies).

    In the command policy specification provided, special characters which need to be escaped are already omitted to easily copy-paste into the Citrix ADC command line.

    For configuring the command policy from Citrix ADC configuration wizard (GUI), use the following command policy specification.

        ^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)

4.  Bind the policy to the system user account using the following command:

    ```
       bind system user cic cic-policy 0
    ```

## Installing the Chart
Add the Citrix Ingress Controller helm chart repository using command:

```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
```

### For Kubernetes:
#### 1. Citrix Ingress Controller
To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,ingressClass[0]=<ingressClassName>
   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix ingress controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

#### 2. Citrix Ingress Controller with Exporter
[Metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics) can be deployed along with Citrix ingress controller and collects metrics from the Citrix ADC instances. You can then [visualize these metrics](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/metrics/promotheus-grafana/) using Prometheus Operator and Grafana.

> **Note:**
> Ensure that you have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator).

Use the following command for this:
   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,ingressClass[0]=<ingressClassName>,exporter.required=true
   ```

### For Openshift:
Add the name of the service account created when the chart is deployed to the privileged Security Context Constraints of OpenShift:

   ```
   oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:<service-account-name>
   ```

#### 1. Citrix Ingress Controller
To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,openshift=true
   ```

The command deploys Citrix ingress controller on your Openshift cluster in the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

#### 2. Citrix Ingress Controller with Exporter
[Metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics) can be deployed along with Citrix ingress controller and collects metrics from the Citrix ADC instances. You can then [visualize these metrics](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/metrics/promotheus-grafana/) using Prometheus Operator and Grafana.

> **Note:**
> Ensure that you have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator)

Use the following command for this:
   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,openshift=true,exporter.required=true
   ```

### Installed components

The following components are installed:

-  [Citrix ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller)
-  [Exporter](https://github.com/citrix/citrix-adc-metrics-exporter) (if enabled)

## Configuration for ServiceGraph:
   If Citrix ADC VPX/MPX need to send data to the Citrix ADM to bring up the servicegraph, then the below steps can be followed to install Citrix ingress controller for Citrix ADC VPX/MPX. Citrix ingress controller configures Citrix ADC VPX/MPX with the configuration required for servicegraph.

   1. Create secret using Citrix ADC VPX credentials, which will be used by Citrix ingress controller for configuring Citrix ADC VPX/MPX:

	kubectl create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'

   2. Deploy Citrix ingress controller using helm command:

	helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,nsVIP=<NSVIP>,license.accept=yes,adcCredentialSecret=<Secret-of-Citrix-ADC-credentials>,coeConfig.required=true,coeConfig.timeseries.metrics.enable=true,coeConfig.timeseries.port=5563,coeConfig.distributedTracing.enable=true,coeConfig.transactions.enable=true,coeConfig.transactions.port=5557,coeConfig.endpoint.server=<ADM-Agent-IP>

> **Note:**
> If container agent is being used here for Citrix ADM, please provide `podIP` of container agent in the `coeConfig.endpoint.server` parameter.

## CRDs configuration

CRDs can be installed/upgraded when we install/upgrade Citrix ingress controller using `crds.install=true` parameter in Helm. If you do not want to install CRDs, then set the option `crds.install` to `false`. By default, CRDs too get deleted if you uninstall through Helm. This means, even the CustomResource objects created by the customer will get deleted. If you want to avoid this data loss set `crds.retainOnDelete` to `true`.

> **Note:**
> Installing again may fail due to the presence of CRDs. Make sure that you back up all CustomResource objects and clean up CRDs before re-installing Citrix Ingress Controller.

There are a few examples of how to use these CRDs, which are placed in the folder: [Example-CRDs](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds). Refer to them and install as needed, using the following command:
```kubectl create -f <crd-example.yaml>```

### Details of the supported CRDs:

#### authpolicies CRD:

Authentication policies are used to enforce access restrictions to resources hosted by an application or an API server.

Citrix provides a Kubernetes CustomResourceDefinitions (CRDs) called the [Auth CRD](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/auth) that you can use with the Citrix ingress controller to define authentication policies on the ingress Citrix ADC.

Example file: [auth_example.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/auth_example.yaml)

#### continuousdeployments CRD  for canary:

Canary release is a technique to reduce the risk of introducing a new software version in production by first rolling out the change to a small subset of users. After user validation, the application is rolled out to the larger set of users. Citrix ADC-Integrated [Canary Deployment solution](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/canary) stitches together all components of continuous delivery (CD) and makes canary deployment easier for the application developers.

#### httproutes and listeners CRDs for contentrouting:

[Content Routing (CR)](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/contentrouting) is the execution of defined rules that determine the placement and configuration of network traffic between users and web applications, based on the content being sent. For example, a pattern in the URL or header fields of the request.

Example files: [HTTPRoute_crd.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/HTTPRoute_crd.yaml), [Listener_crd.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/Listener_crd.yaml)

#### ratelimits CRD:

In a Kubernetes deployment, you can [rate limit the requests](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/ratelimit) to the resources on the back end server or services using rate limiting feature provided by the ingress Citrix ADC.

Example files: [ratelimit-example1.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/ratelimit-example1.yaml), [ratelimit-example2.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/ratelimit-example2.yaml)

#### vips CRD:

Citrix provides a CustomResourceDefinitions (CRD) called [VIP](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd/vip) for asynchronous communication between the IPAM controller and Citrix ingress controller.

The IPAM controller is provided by Citrix for IP address management. It allocates IP address to the service from a defined IP address range. The Citrix ingress controller configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADX VPX. And, the service is exposed using the IP address.

When a new service is created, the Citrix ingress controller creates a CRD object for the service with an empty IP address field. The IPAM Controller listens to addition, deletion, or modification of the CRD and updates it with an IP address to the CRD. Once the CRD object is updated, the Citrix ingress controller automatically configures Citrix ADC-specfic configuration in the tier-1 Citrix ADC VPX.

#### rewritepolicies CRD:

In kubernetes environment, to deploy specific layer 7 policies to handle scenarios such as, redirecting HTTP traffic to a specific URL, blocking a set of IP addresses to mitigate DDoS attacks, imposing HTTP to HTTPS and so on, requires you to add appropriate libraries within the microservices and manually configure the policies. Instead, you can use the [Rewrite and Responder features](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/rewrite-responder-policies-deployment.yaml) provided by the Ingress Citrix ADC device to deploy these policies.

Example files: [target-url-rewrite.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/target-url-rewrite.yaml)

#### wafs CRD:

[WAF CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/crds/waf.md) can be used to configure the web application firewall policies with the Citrix ingress controller on the Citrix ADC VPX, MPX, SDX, and CPX. The WAF CRD enables communication between the Citrix ingress controller and Citrix ADC for enforcing web application firewall policies.

In a Kubernetes deployment, you can enforce a web application firewall policy to protect the server using the WAF CRD. For more information about web application firewall, see [Web application security](https://docs.citrix.com/en-us/citrix-adc/13/application-firewall/introduction/web-application-security.html).

Example files: [wafhtmlxsssql.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/wafhtmlxsssql.yaml)

#### apigateway CRD:

API Gateway CRD is used to configure gitops framework on citrix API gateway. This solution enables citrix ingress controller to generate API gateway configurations out of Open API Specification documents checked in to git repository by API developers and designers.

Example files: [api-gateway-crd-instance.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/api-gateway-crd-instance.yaml)
#### bots CRD:

[BOT CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/crds/bot.md) You can use Bot CRDs to configure the bot management policies with the Citrix ingress controller on the Citrix ADC VPX. The Bot custom resource definition enables communication between the Citrix ingress controller and Citrix ADC for enforcing bot management policies.

In a Kubernetes deployment, you can enforce bot management policy on therequests and responses from and to the server using the Bot CRDs. For more information on security vulnerabilities, see [Bot Detection](https://docs.citrix.com/en-us/citrix-adc/current-release/bot-management/bot-detection.html).

Example files: [botallowlist.yaml](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds/botallowlist.yaml)

### Tolerations

Taints are applied on cluster nodes whereas tolerations are applied on pods. Tolerations enable pods to be scheduled on node with matching taints. For more information see [Taints and Tolerations in Kubernetes](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).

Toleration can be applied to Citrix ingress controller pod using `tolerations` argument while deploying CIC using helm chart. This argument takes list of tolerations that user need to apply on the CIC pods.

For example, following command can be used to apply toleration on the CIC pod:

```
helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,tolerations[0].key=<toleration-key>,tolerations[0].value=<toleration-value>,tolerations[0].operator=<toleration-operator>,tolerations[0].effect=<toleration-effect>
```

Here tolerations[0].key, tolerations[0].value and tolerations[0].effect are the key, value and effect that was used while tainting the node.
Effect represents what should happen to the pod if the pod don't have any matching toleration. It can have values `NoSchedule`, `NoExecute` and `PreferNoSchedule`.
Operator represents the operation to be used for key and value comparison between taint and tolerations. It can have values `Exists` and `Equal`. The default value for operator is `Equal`.



### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the CIC end user license agreement. |
| image | Mandatory | `quay.io/citrix/citrix-k8s-ingress-controller:1.25.6` | The CIC image. |
| pullPolicy | Mandatory | IfNotPresent | The CIC image pull policy. |
| adcCredentialSecret | Mandatory | N/A | The secret key to log on to the Citrix ADC VPX or MPX. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| nsIP | Mandatory | N/A | The IP address of the Citrix ADC device. For details, see [Prerequisites](#prerequistes). |
| nsVIP | Optional | N/A | The Virtual IP address on the Citrix ADC device. |
| nsSNIPS | Optional | N/A | The list of subnet IPAddresses on the Citrix ADC device, which will be used to create PBR Routes instead of Static Routes [PBR support](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/docs/how-to/pbr.md) |
| nsPort | Optional | 443 | The port used by CIC to communicate with Citrix ADC. You can use port 80 for HTTP. |
| nsProtocol | Optional | HTTPS | The protocol used by CIC to communicate with Citrix ADC. You can also use HTTP on port 80. |
| logLevel | Optional | DEBUG | The loglevel to control the logs generated by CIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, DEBUG and TRACE. For more information, see [Logging](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/log-levels.md).|
| kubernetesURL | Optional | N/A | The kube-apiserver url that CIC uses to register the events. If the value is not specified, CIC uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
| clusterName | Optional | N/A | The unique identifier of the kubernetes cluster on which the CIC is deployed. Used in multi-cluster deployments. |
| ingressClass | Optional | N/A | If multiple ingress load balancers are used to load balance different ingress resources. You can use this parameter to specify CIC to configure Citrix ADC associated with specific ingress class. For more information on Ingress class, see [Ingress class support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/ingress-classes/). For Kubernetes version >= 1.19, this will create an IngressClass object with the name specified here |
| setAsDefaultIngressClass | Optional | False | Set the IngressClass object as default ingress class. New Ingresses without an "ingressClassName" field specified will be assigned the class specified in ingressClass. Applicable only for kubernetes versions >= 1.19 |
| serviceClass | Optional | N/A | By Default ingress controller configures all TypeLB Service on the ADC. You can use this parameter to finetune this behavior by specifing CIC to only configure TypeLB Service with specific service class. For more information on Service class, see [Service class support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/service-classes/). |
| nodeWatch | Optional | false | Use the argument if you want to automatically configure network route from the Ingress Citrix ADC VPX or MPX to the pods in the Kubernetes cluster. For more information, see [Automatically configure route on the Citrix ADC instance](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/staticrouting/#automatically-configure-route-on-the-citrix-adc-instance). |
| cncPbr | Optional | False | Use this argument to inform CIC that Citrix Node Controller(CNC) is configuring Policy Based Routes(PBR) on the Citrix ADC. For more information, see [CNC-PBR-SUPPORT](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/docs/how-to/pbr.md#configure-pbr-using-the-citrix-node-controller) |
| defaultSSLCertSecret | Optional | N/A | Provide Kubernetes secret name that needs to be used as a default non-SNI certificate in Citrix ADC. |
| podIPsforServiceGroupMembers | Optional | False |  By default Citrix Ingress Controller will add NodeIP and NodePort as service group members while configuring type LoadBalancer Services and NodePort services. This variable if set to `True` will change the behaviour to add pod IP and Pod port instead of nodeIP and nodePort. Users can set this to `True` if there is a route between ADC and K8s clusters internal pods either using feature-node-watch argument or using Citrix Node Controller. |
| ignoreNodeExternalIP | Optional | False | While adding NodeIP, as Service group members for type LoadBalancer services or NodePort services, Citrix Ingress Controller has a selection criteria whereas it choose Node ExternalIP if available and Node InternalIP, if Node ExternalIP is not present. But some users may want to use Node InternalIP over Node ExternalIP even if Node ExternalIP is present. If this variable is set to `True`, then it prioritises the Node Internal IP to be used for service group members even if node ExternalIP is present |
| nsHTTP2ServerSide | Optional | OFF | Set this argument to `ON` for enabling HTTP2 for Citrix ADC service group configurations. |
| nsCookieVersion | Optional | 0 | Specify the persistence cookie version (0 or 1). |
| ipam | Optional | False | Set this argument if you want to use the IPAM controller to automatically allocate an IP address to the service of type LoadBalancer. |
| logProxy | Optional | N/A | Provide Elasticsearch or Kafka or Zipkin endpoint for Citrix observability exporter. |
| entityPrefix | Optional | k8s | The prefix for the resources on the Citrix ADC VPX/MPX. |
| updateIngressStatus | Optional | False | Set this argurment if `Status.LoadBalancer.Ingress` field of the Ingress resources managed by the Citrix ingress controller needs to be updated with allocated IP addresses. For more information see [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/ingress-classes.md#updating-the-ingress-status-for-the-ingress-resources-with-the-specified-ip-address). |
| routeLabels | Optional | N/A | You can use this parameter to provide the route labels selectors to be used by Citrix Ingress Controller for routeSharding in OpenShift cluster. |
| namespaceLabels | Optional | N/A | You can use this parameter to provide the namespace labels selectors to be used by Citrix Ingress Controller for routeSharding in OpenShift cluster. |
| exporter.required | Optional | false | Use the argument, if you want to run the [Exporter for Citrix ADC Stats](https://github.com/citrix/citrix-adc-metrics-exporter) along with CIC to pull metrics for the Citrix ADC VPX or MPX|
| exporter.image    | Optional | `quay.io/citrix/citrix-adc-metrics-exporter:1.4.7` | The Exporter image. |
| exporter.pullPolicy | Optional | IfNotPresent | The Exporter image pull policy. |
| exporter.ports.containerPort | Optional | 8888 | The Exporter container port. |
| openshift | Optional | false | Set this argument if OpenShift environment is being used. |
| nodeSelector.key | Optional | N/A | Node label key to be used for nodeSelector option in CIC deployment. |
| nodeSelector.value | Optional | N/A | Node label value to be used for nodeSelector option in CIC deployment. |
| tolerations | Optional | N/A | Specify the tolerations for the CIC deployment. |
| crds.install | Optional | False | Unset this argument if you don't want to install CustomResourceDefinitions which are consumed by CIC. |
| crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling CIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |
| coeConfig.required | Mandatory | false | Set this to true if you want to configure Citrix ADC to send metrics and transaction records to COE. |
| coeConfig.distributedTracing.enable | Optional | false | Set this value to true to enable OpenTracing in Citrix ADC. |
| coeConfig.distributedTracing.samplingrate | Optional | 100 | Specifies the OpenTracing sampling rate in percentage. |
| coeConfig.endpoint.server | Optional | N/A | Set this value as the IP address or DNS address of the  analytics server. |
| coeConfig.timeseries.port | Optional | 30002 | Specify the port used to expose COE service outside cluster for timeseries endpoint. |
| coeConfig.timeseries.metrics.enable | Optional | False | Set this value to true to enable sending metrics from Citrix ADC. |
| coeConfig.timeseries.metrics.mode | Optional | avro |  Specifies the mode of metric endpoint. |
| coeConfig.timeseries.auditlogs.enable | Optional | false | Set this value to true to export audit log data from Citrix ADC. |
| coeConfig.timeseries.events.enable | Optional | false | Set this value to true to export events from the Citrix ADC. |
| coeConfig.transactions.enable | Optional | false | Set this value to true to export transactions from Citrix ADC. |
| coeConfig.transactions.port | Optional | 30001 | Specify the port used to expose COE service outside cluster for transaction endpoint. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/citrix-ingress-controller -f values.yaml
   ```

> **Tip:**
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/citrix-ingress-controller/values.yaml) contains the default values of the parameters.

> **Note:**
>
> Please provide frontend-ip (VIP) in your application ingress yaml file. For more info refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/annotations.md).

## Route Addition in MPX/VPX
For seamless functioning of services deployed in the Kubernetes cluster, it is essential that Ingress NetScaler device should be able to reach the underlying overlay network over which Pods are running.
`feature-node-watch` knob of Citrix Ingress Controller can be used for automatic route configuration on NetScaler towards the pod network. Refer [Static Route Configuration](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) for further details regarding the same.
By default, `feature-node-watch` is false. It needs to be explicitly set to true if auto route configuration is required.

This can also be achieved by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).

If your deployment uses one single Citrix ADC Device to loadbalance between multiple k8s clusters, there is a possibilty of CNI subnets to overlap, causing the above mentioned static routing to fail due to route conflicts. In such deployments [Policy Based Routing(PBR)] (https://docs.citrix.com/en-us/citrix-adc/current-release/networking/ip-routing/configuring-policy-based-routes/configuring-policy-based-routes-pbrs-for-ipv4-traffic.html) can be used instead. This would require you to provide one or more subnet IP Addresses unique for each kubernetes cluster either via Environment variable or Configmap, see [PBR Support](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/docs/how-to/pbr.md)

   Use the following command to provide subnet IPAddresses(SNIPs) to configure Policy Based Routes(PBR) on the Citrix ADC

   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,nsSNIPS='[<NS_SNIP1>\, <NS_SNIP2>\, ...]'
   ```

   [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller) by default also adds static routes while creating the VXLAN tunnel. To use [Policy Based Routing(PBR)] (https://docs.citrix.com/en-us/citrix-adc/current-release/networking/ip-routing/configuring-policy-based-routes/configuring-policy-based-routes-pbrs-for-ipv4-traffic.html) to avoid static route clash, both Citrix Node Controller and Citrix Ingress Controller has to work in conjunction and has to be started with specific arguments. For more details refer [CNC-PBR-SUPPORT](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/docs/how-to/pbr.md#configure-pbr-using-the-citrix-node-controller).

   Use the following command to inform Citrix Ingress Controller that Citrix Node Controller is configuring Policy Based Routes(PBR) on the Citrix ADC

   ```
   helm install my-release citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,clusterName=<unique-cluster-identifier>,cncPbr=<True/False>
   ```

For configuring static routes manually on Citrix ADC VPX or MPX to reach the pods inside the cluster follow:
### For Kubernetes:
1. Obtain podCIDR using below options:
   ```
   kubectl get nodes -o yaml | grep podCIDR
   ```
   * podCIDR: 10.244.0.0/24
   * podCIDR: 10.244.1.0/24
   * podCIDR: 10.244.2.0/24

2. Log on to the Citrix ADC instance.

3. Add Route in Netscaler VPX/MPX
   ```
   add route <podCIDR_network> <podCIDR_netmask> <node_HostIP>
   ```
4. Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which K8S nodes communicate with each other. Usually eth0 IP is from this network).

   Example:
   * Node1 IP = 192.0.2.1
   * podCIDR  = 10.244.1.0/24
   * add route 10.244.1.0 255.255.255.0 192.0.2.1

### For OpenShift:
1. Use the following command to get the information about host names, host IP addresses, and subnets for static route configuration.
   ```
    oc get hostsubnet
   ```

2. Log on to the Citrix ADC instance.

3. Add the route on the Citrix ADC instance using the following command.
   ```add route <pod_network> <podCIDR_netmask> <gateway>```

4. Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which OpenShift nodes communicate with each other. Usually eth0 IP is from this network).

    For example, if the output of the `oc get hostsubnet` is as follows:
    * oc get hostsubnet

        NAME            HOST           HOST IP        SUBNET
        os.example.com  os.example.com 192.0.2.1 10.1.1.0/24

    * The required static route is as follows:

           add route 10.1.1.0 255.255.255.0 192.0.2.1

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

   ```
   helm delete my-release
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

- [Citrix ingress controller Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/)
- [Citrix ingress controller GitHub](https://github.com/citrix/citrix-k8s-ingress-controller)
