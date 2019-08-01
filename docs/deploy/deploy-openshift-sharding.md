# Deploy the Citrix ingress controller with OpenShift router sharding support

[OpenShift router sharding](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html#router-sharding) allows distributing a set of routes among multiple OpenShift routers. By default, an OpenShift router selects all routes from all namespaces. In router sharding, labels are added to routes or namespaces and label selectors to routers for filtering routes. Each router shard selects only routes with specific labels that match its label selection parameters.

Citrix ADC can be integrated with OpenShift in two ways and both deployments support OpenShift router sharding.

-  Citrix ADC CPX deployed as an OpenShift router along with Citrix ingress controller inside the cluster
-  Citrix ingress controller as a router plug-in for Citrix ADC MPX or VPX deployed outside the cluster

To configure router sharding for a Citrix ADC deployment on OpenShift, a Citrix ingress controller instance is required per shard. The Citrix ingress controller instance is deployed with route or namespace labels or both as environment variables depending on the criteria required for sharding.
When the Citrix ingress controller processes a route, it compares the route’s labels or route’s namespace labels with the selection criteria configured on it. If the route satisfies the criteria, the appropriate configuration is applied to Citrix ADC, otherwise it does not apply the configuration.

In router sharding, selecting a subset of routes from the entire pool of routes is based on selection expressions. Selection expressions are a combination of multiple values and operations.

For example, consider there are some routes with various labels for service level agreement(sla), geographical location (geo), hardware requirements(hw), department (dept), type, and frequency as shown in the following table.

| Label   | Values             |
|---------|--------------------|
|  sla    | high, medium, low  |
|  geo    | east, west |
|  hw     |  modest, strong     |  
|  dept   |  finance, dev, ops  |
|  type    | static, dynamic |
| frequency | high, weekly |

The following table shows selectors for route labels or namespace labels and a few sample selection expressions based on labels in the example. Route selection criteria is configured on the Citrix ingress controller by using environment variables ROUTE_LABELS and NAMESPACE_LABLES.

| Type of selector               | Example                       |
|--------------------------------|-------------------------------|
|          OR operation         | ROUTE_LABELS='dept in (dev, ops)'|
|          AND operation         | ROUTE_LABELS='hw=strong,type=dynamic,geo=west' |
|          NOT operation        | ROUTE_LABELS='dept!= finance'     |  
|      Exact match               | NAMESPACE_LABELS='frequency=weekly' |
|      Exact match with both route and namespace labels   |  NAMESPACE_LABELS='frequency=weekly' ROUTE_LABELS='sla=low' |
| Key based matching independent of value | NAMESPACE_LABELS='name'  |
| NOT operation with key based matching independent of value | NAMESPACE_LABELS='!name'  |

!!! note "Note"
    The label selectors use the language supported by Kubernetes labels.

If you want, you can change route or namespace labels by editing them later. Once you change the labels, router shard is revalidated and based on the change the Citrix ingress controller updates the configuration on Citrix ADC.

## Deploy Citrix ADC CPX with OpenShift router sharding

To deploy CPX with OpenShift router sharding support, perform the following steps:

1.  Download the [cpx_cic_side_car.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml) file using the following command:

         wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml

2.  Edit the [cpx_cic_side_car.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml) file and specify the route labels and namespace label selectors as environment variables.  

    The following example shows how to specify a sample route label and namespace label in the `cpx_cic_side_car.yaml` file. This example selects routes with label "name" values as either abc or xyz and with namespace label as frequency=high.

                env:    
                - name: "ROUTE_LABELS"
                  value: "name in (abc,xyz)"
                - name: "NAMESPACE_LABELS"
                  value: "frequency=high"       

3.  Deploy the Citrix ingress controller using the following command.

        oc create -f cpx_cic_side_car.yaml

## Deploy the Citrix ingress controller router plug-in with OpenShift router sharding support

To deploy a Citrix ingress controller router plug-in with router sharding, perform the following steps:

1.  Download the [cic.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml) file using the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml

2.  Edit the [cic.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml) file and specify the route labels and namespace label selectors as environment variables.

    The following example shows how to specify a sample route label and namespace label in the `cic.yaml` file. This example selects routes with label "name" values as either abc or xyz and with namespace label as frequency=high.

                env:
                - name: "ROUTE_LABELS"
                  value: "name in (abc,xyz)"
                - name: "NAMESPACE_LABELS"
                  value: "frequency=high"

3.  Deploy the Citrix ingress controller using the following command.

        oc create -f cic.yaml

## **Example:** Create an OpenShift route and verify the route configuration on Citrix ADC VPX

This example shows how to create an OpenShift route with labels and verify the router shard configuration.
In this example, route configuration is verified on a [Citrix ADC VPX deployment](#deploy-the-citrix-ingress-controller-router-plug-in-with-openshift-router-sharding-support).

Perform the following steps to create a sample route with labels.

1.  Define the route in a YAML file. Following is an example for a sample route named as `route.yaml`.

        apiVersion: v1
        kind: Route
        metadata:
            name: web-backend-route
            namespace: default
            labels:
                sla: low
                name: abc
        spec:
            host: web-frontend.cpx-lab.org
            path: "/web-backend"
            port:
                targetPort: 80
            to:
                kind: Service
                name: web-backend

1.  Use the following command to deploy the route.

        oc create -f route.yaml

1.  Add labels to the namespace where you create the route.

        oc label namespace default 'frequency=high'

### Verify route configuration

You can verify the OpenShift route configuration on a Citrix ADC VPX by performing the following steps:

1.  Log on to Citrix ADC VPX by performing the following:

    -  Use an SSH client such as PuTTy, to open an SSH connection to Citrix ADC VPX.
    -  Log on to Citrix ADC VPX by using administrator credentials.

1.  Check if the service group is created using the following command.

        show serviceGroup 

1.  Verify the route configuration on Citrix ADC VPX in the ``show serviceGroup`` command output.

    Following is a sample route configuration from the ``show serviceGroup`` command output.

        > show serviceGroup
        k8s-web-backend-route_default_80_k8s-web-backend_default_80_svc - HTTP
        State: ENABLED  Effective State: DOWN Monitor Threshold : 0
        Max Conn: 0     Max Req: 0 Max Bandwidth: 0 kbits
        Use Source IP: NO    
        Client Keepalive(CKA): NO
        TCP Buffering(TCPB): NO
        HTTP Compression(CMP): NO
        Idle timeout: Client: 180 sec    Server: 360 sec
        Client IP: DISABLED 
        Cacheable: NO
        SC: OFF
        SP: OFF
        Down state flush: ENABLED
        Monitor Connection Close : NONE
        Appflow logging: ENABLED
        ContentInspection profile name: ???
        Process Local: DISABLED
        Traffic Domain: 0
