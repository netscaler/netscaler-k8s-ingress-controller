# Deploy the Citrix ingress controller as an OpenShift router plug-in

In an OpenShift cluster, external clients need a way to access the services provided by pods. OpenShift provides two resources for communicating with services running in the cluster: [routes](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html) and [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/).

In an OpenShift cluster, a route exposes a service on a given domain name or associates a domain name with a service. OpenShift routers route external requests to services inside the OpenShift cluster according to the rules specified in routes. When you use the OpenShift router, you must also configure the external DNS to make sure that the traffic is landing on the router.

The Citrix ingress controller can be deployed as a router plug-in in the OpenShift cluster to integrate with Citrix ADCs deployed in your environment. The Citrix ingress controller enables you to use the advanced load balancing and traffic management capabilities of Citrix ADC with your OpenShift cluster.

OpenShift routes can be secured or unsecured. Secured routes specify the TLS termination of the route.

The Citrix ingress controller supports the following OpenShift routes:

-  **Unsecured Routes**: For Unsecured routes, HTTP traffic is not encrypted.

-  **Edge Termination**: For edge termination, TLS is terminated at the router. Traffic from the router to the endpoints over the internal network is not encrypted.

-  **Passthrough Termination**: With passthrough termination, the router is not involved in TLS offloading and encrypted traffic is sent straight to the destination.

-  **Re-encryption Termination**: In re-encryption termination, the router terminates the TLS connection but then establishes another TLS connection to the endpoint.

For detailed information on routes, see the [OpenShift documentation](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html#secured-routes).

You can either deploy a Citrix ADC MPX or VPX appliance outside the OpenShift cluster or deploy Citrix ADC CPXs as pods inside the cluster. The Citrix ingress controller integrates Citrix ADCs with the OpenShift cluster and automatically configures Citrix ADCs based on rules specified in routes.

Based on how you want to use Citrix ADC, there are two ways to deploy the Citrix Ingress Controller as a router plug-in in the OpenShift cluster:

-  As a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) container alongside Citrix ADC CPX in the same pod: In this mode, the Citrix ingress controller configures the Citrix ADC CPX.
  
-  As a standalone pod in the OpenShift cluster: In this mode, you can control the Citrix ADC MPX or VPX appliance deployed outside the cluster.

For information on deploying the Citrix ingress controller to control the OpenShift ingress, see the [Citrix ingress controller for Kubernetes](../index.md).

You can use Citrix ADC for load balancing Openshift control plane (master nodes). Citrix provides a solution to automate the configuration of Citrix ADC using Terraform instead of manually configuring the Citrix ADC. For more information, see [Citrix ADC as a load balancer for the OpenShift control plane](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/openshift/citrix-adc-for-control-plane/README.md).

## Alternate Backend Support
[OpenShift Alternate backends](https://docs.openshift.com/container-platform/3.7/architecture/networking/routes.html#alternateBackends) is now supported by Citrix ingress controller.

Citrix ADC is configured according to the weights provided in the routes definition and traffic is distributed among the service pods based on those weights.

The following is an example of a route manifest with alternate backend:

	
	kind: Route
	apiVersion: route.openshift.io/v1
	metadata:
	  name: r1 
	  labels:
	    name: apache
	  annotations:
	    ingress.citrix.com/frontend-ip: "<Frontend-ip>"
	spec:
	  host: some.alternate-backends.com
	  to:
	    kind: Service
	    name: apache-1
	    weight: 30
	  alternateBackends:
	    - kind: Service
	      name: apache-2
	      weight: 20
	    - kind: Service
	      name: apache-3
	      weight: 50
	  port:
	    targetPort: 80
	  wildcardPolicy: None
	
For this route, 30 percent of the traffic is sent to the service apache-1 and 20 percent is sent to the service apache2 and 50 percent to the service apache-3 based on weights provided in the route manifest 

## Supported Citrix components on OpenShift

| Citrix components | Versions |
| ----------------- | -------- |
| Citrix ingress controller | Latest  |
| Citrix ADC VPX | 12.1 50.x and later |
| Citrix ADC CPX | 13.0–36.28 |

**Note:** [CRDs](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/crd) provided for the Citrix ingress controller is not supported for OpenShift routes. You can use OpenShift ingress to use CRDs.

## Deploy Citrix ADC CPX as a router within the OpenShift cluster

In this deployment, you can use the Citrix ADC CPX instance for load balancing the North-South traffic to microservices in your OpenShift cluster. The Citrix ingress controller is deployed as a sidecar alongside the Citrix ADC CPX container in the same pod using the [cpx_cic_side_car.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml) file.

**Before you begin**

  When you deploy Citrix ADC CPX as a router, port conflicts can arise with the default router in OpenShift. You should remove the default router in OpenShift before deploying Citrix ADC CPX as a router. To remove the default router in OpenShift, perform the following steps:

1.  Back up the default router configuration using the following command.

        oc get -o yaml dc/router clusterrolebinding/router-router-role serviceaccount/router > default-router-backup.yaml

2.  Delete the default router using the following command.

        oc delete -f default-router-backup.yaml

Perform the following steps to deploy Citrix ADC CPX as a router with the Citrix ingress controller as a sidecar.

1.  Download the [cpx_cic_side_car.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml) file using the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cpx_cic_side_car.yaml


2.  Add the service account to privileged security context constraints (SCC) of OpenShift.

        oc adm policy add-scc-to-user privileged system:serviceaccount:default:citrix

3.  Deploy the Citrix ingress controller using the following command:

        oc create -f cpx_cic_side_car.yaml

4.  Verify if the Citrix ingress controller is deployed successfully using the following command:

        oc get pods --all-namespaces

## Deploy Citrix ADC MPX/VPX as a router outside the OpenShift cluster

In this deployment, the Citrix ingress controller which runs as a stand-alone pod allows you to control the Citrix ADC MPX, or VPX appliance from the OpenShift cluster.
You can use the [cic.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml) file for this deployment.

**Note:** The Citrix ADC MPX or VPX can be deployed in *[standalone](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc.html)*, *[high-availability](https://docs.citrix.com/en-us/citrix-adc/12-1/getting-started-with-citrix-adc/configure-ha-first-time.html)*, or *[clustered](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering.html)* modes.

**Note:** In the latest versions of OpenShift when OVN CNI is used, `—feature-node-watch` might not work. In that case, you must manually configure the static routes on Citrix ADC VPX.

### Prerequisites

-  Determine the IP address needed by the Citrix ingress controller to communicate with the Citrix ADC appliance. The IP address might be any one of the following depending on the type of Citrix ADC deployment:
    -  NSIP (for standalone appliances): The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).
    -  SNIP (for appliances in High Availability mode):  The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).
    -  CLIP (for appliances in clustered mode): The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).
-  The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. If you are not using the default credentials, the Citrix ADC appliance must have a system user account with certain privileges so that the Citrix ingress controller can configure the Citrix ADC MPX, or VPX appliance. To create a system user account on Citrix ADC, see [Create a system user account for the Citrix ingress controller in Citrix ADC](#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc).

    You can directly pass the user name and password as environment variables to the Citrix ingress controller or use OpenShift secrets (recommended). If you want to use OpenShift secrets, create a secret for the user name and password using the following command:

        oc create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'

#### Create a system user account for the Citrix ingress controller in Citrix ADC

The Citrix ingress controller configures a Citrix ADC appliance (MPX or VPX) using a system user account of the Citrix ADC appliance. The system user account must have the permissions to configure the following tasks on the Citrix ADC:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Cofigure SSL certkeys
-  Configure routes
-  Configure user monitors
-  Add system file (for uploading SSL testkeys from OpenShift)
-  Configure Virtual IP address (VIP)
-  Check the status of the Citrix ADC appliance
-  Configure SSL actions and policies
-  Configure SSL vServer
-  Configure responder actions and policies

**To create the system user account, perform the following:**

1.  Log on to the Citrix ADC appliance using the following steps:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.

    1.  Log on to the appliance by using the administrator credentials.

1.  Create the system user account using the following command:

        add system user <username> <password>

    For example:

        add system user cic mypassword

1.  Create a policy to provide required permissions to the system user account. Use the following command:

        add cmdpolicy cic-policy ALLOW '^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(\?!shell)(\?!sftp)(\?!scp)(\?!batch)(\?!source)(\?!.*superuser)(\?!.*nsroot)(\?!install)(\?!show\s+system\s+(user|cmdPolicy|file))(\?!(set|add|rm|create|export|kill)\s+system)(\?!(unbind|bind)\s+system\s+(user|group))(\?!diff\s+ns\s+config)(\?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)'

    **Note**: The system user account would have privileges based on the command policy that you define.
    The command policy mentioned in ***step 3*** is similar to the built-in `sysAdmin` command policy with another permission to upload files.

    The command policy spec provided above have already escaped special characters for easier copy pasting into the Citrix ADC command line.

    For configuring the command policy from Citrix ADC Configuration Wizard (GUI), use the below command policy spec.

        ^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)^(?!shell)(?!sftp)(?!scp)(?!batch)(?!source)(?!.*superuser)(?!.*nsroot)(?!install)(?!show\s+system\s+(user|cmdPolicy|file))(?!(set|add|rm|create|export|kill)\s+system)(?!(unbind|bind)\s+system\s+(user|group))(?!diff\s+ns\s+config)(?!(set|unset|add|rm|bind|unbind|switch)\s+ns\s+partition).*|(^install\s*(wi|wf))|(^\S+\s+system\s+file)



1.  Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0

## Deploy the Citrix ingress controller as a pod in an OpenShift cluster

Perform the following steps to deploy the Citrix ingress controller as a pod:

1.  Download the [cic.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml) file using the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml

2.  Edit the [cic.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/cic.yaml) file and enter the values for the following environmental variables:

    | Environment Variable | Mandatory or Optional | Description |
    | ---------------------- | ---------------------- | ----------- |
    | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/openshift#prerequisites). |
    | NS_USER and NS_PASSWORD | Mandatory | The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/openshift#prerequisites). |
    | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
    | NS_VIP | Optional | Citrix ingress controller uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. **Note:** NS_VIP acts as a fallback when the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/annotations.md) annotation is not provided in Ingress or Route yaml. Not supported for Type Loadbalancer service. |

3.  Add the service account to privileged security context constraints (SCC) of OpenShift.

        oc adm policy add-scc-to-user privileged system:serviceaccount:default:citrix

4.  Save the edited ``cic.yaml`` file and deploy it using the following command:

         oc create -f cic.yaml

5.  Verify if the Citrix ingress controller is deployed successfully using the following command:

        oc create get pods --all-namespaces

6.  Configure static routes on Citrix ADC VPX or MPX to reach the pods inside the OpenShift cluster.

      1.  Use the following command to get the information about host names, host IP addresses, and subnets for static route configuration.

              oc get hostsubnet
    
      1.  Log on to the Citrix ADC instance.
   
      2.  Add the route on the Citrix ADC instance using the following command.

              add route <pod_network> <netmask> <gateway>

	       <B>Example:</b>



	
	          oc get hostsubnet
	 
	          NAME            HOST           HOST IP        SUBNET
	          os.example.com  os.example.com 192.168.122.46 192.1.1.0/24
    
 
          From the output of the `oc get hostsubnet` command:


       

  
              <pod_network> = 192.1.1.0
              Value for subnet = 192.1.1.0/x where x = 24 that means <netmask>= 255.255.255.0
              <gateway> = 192.168.122.46


	        The required static route to add on Citrix ADC is as follows:


              add route 10.1.1.0 255.255.255.0 192.168.122.46

## Example: Deploy the Citrix ingress controller as a router plug-in in an OpenShift cluster

In this example, the Citrix ingress controller is deployed as a router plug-in in the OpenShift cluster to load balance an application.

1.  Deploy a sample application ([apache.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/apache.yaml)) in your OpenShift cluster and expose it as a service in your cluster using the following command.

        oc create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/apache.yaml

    **Note:**
        When you deploy a normal Apache pod in OpenShift, it may fail as Apache pod always runs as a root pod. OpenShift has strict security checks which block running a pod as root or binding to port 80. As a workaround, you can add the default service account of the pod to the privileged security context of OpenShift by using the following commands:

            oc adm policy add-scc-to-user privileged system:serviceaccount:default:default
            oc adm policy add-scc-to-group anyuid system:authenticated
  
    The content of the `apache.yaml` file is given as follows.

        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          labels:
            name: apache-only-http
          name: apache-only-http
        spec:
          replicas: 4
          selector:
            matchLabels:
              app: apache-only-http
          template:
            metadata:
              labels:
                app: apache-only-http
            spec:
              containers:
              - image: raghulc/apache-multiport-http:1.0.0
                imagePullPolicy: IfNotPresent
                name: apache-only-http
                ports:
                - containerPort: 80
                  protocol: TCP
                - containerPort: 5080
                  protocol: TCP
                - containerPort: 5081
                  protocol: TCP
                - containerPort: 5082
                  protocol: TCP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          labels:
            name: apache-only-ssl
          name: apache-only-ssl
        spec:
          replicas: 4
          selector:
            matchLabels:
              app: apache-only-ssl
          template:
            metadata:
              labels:
                app: apache-only-ssl
            spec:
              containers:
              - image: raghulc/apache-multiport-ssl:1.0.0
                imagePullPolicy: IfNotPresent
                name: apache-only-ssl
                ports:
                - containerPort: 443
                  protocol: TCP
                - containerPort: 5443
                  protocol: TCP
                - containerPort: 5444
                  protocol: TCP
                - containerPort: 5445
                  protocol: TCP
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: svc-apache-multi-http
        spec:
          ports:
          - name: apache-http-6080
            port: 6080
            targetPort: 5080
          - name: apache-http-6081
            port: 6081
            targetPort: 5081
          - name: apache-http-6082
            port: 6082
            targetPort: 5082
          selector:
            app: apache-only-http
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: svc-apache-multi-ssl
        spec:
          ports:
          - name: apache-ssl-6443
            port: 6443
            targetPort: 5443
          - name: apache-ssl-6444
            port: 6444
            targetPort: 5444
          - name: apache-ssl-6445
            port: 6445
            targetPort: 5445
          selector:
            app: apache-only-ssl
        ---

2.  Deploy the Citrix ingress controller for Citrix ADC VPX as a stand-alone pod in the OpenShift cluster using the steps in [Deploy the Citrix ingress controller as a pod](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/openshift#deploy-the-citrix-ingress-controller-as-a-pod-in-an-openshift-cluster).

        oc create -f cic.yaml

    **Note:**
        To deploy the Citrix ingress controller with Citrix ADC CPX in the OpenShift cluster, perform the steps in [Deploy the Citrix ingress controller as a sidecar with Citrix ADC CPX](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/openshift#deploy-citrix-adc-cpx-as-a-router-within-the-openshift-cluster).

3.  Create an OpenShift route for exposing the application.

    -  For creating an unsecured OpenShift route ([unsecured-route.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/unsecured-route.yaml)), use the following command:

            oc create -f unsecured-route.yaml

    -  For creating a secured OpenShift route with edge termination ([secured-edge-route.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/secured-edge-route.yaml)), use the following command.

            oc create -f secured-route-edge.yaml

    -  For creating a secured OpenShift route with passthrough termination ([secured-passthrough-route.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/secured-passthrough-route.yaml)), use the following command.

            oc create -f secured-passthrough-route.yaml

    -  For creating a secured OpenShift route with re-encryption termination ([secured-reencrypt-route.yaml](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/openshift/manifest/secured-reencrypt-route.yaml)), use the following command.

            oc create -f secured-reencrypt-route.yaml

    To see the contents of the YAML files for OpenShift routes in this example, see [YAML files for routes](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/openshift#yaml-files-for-routes).

    **Note:**
        For a secured OpenShift route with passthrough termination, you must include the default certificate.

4.  Access the application using the following command.

      ```
      curl http://<VIP of Citrix ADC VPX>/ -H 'Host: < host-name-as-per-the-host-configuration-in-route >'
      ```

## YAML files for routes

This section contains YAML files for unsecured and secured routes specified in the example.

**Note:** 
    Keys used in this example are for testing purpose only. You must create your own keys for the actual deployment.

The contents of the `unsecured-route.yaml` file is given as follows:

```yml
apiVersion: v1
kind: Route
metadata:
  name: unsecured-route
spec:
  host: unsecured-route.openshift.citrix-cic.com
  path: "/"
  to:
    kind: Service
    name: svc-apache-multi-http
```

The contents of the `secured-edge-route.yaml` file is given as follows:

```yml
apiVersion: v1
kind: Route
metadata:
  name: secured-edge-route
spec:
  host: secured-edge-route.openshift.citrix-cic.com
  path: "/"
  to:
    kind: Service
    name: svc-apache-multi-http
  tls:
    termination: edge

    key: |-
      -----BEGIN RSA PRIVATE KEY-----
            [...]
      -----END RSA PRIVATE KEY-----

    certificate: |-
      -----BEGIN CERTIFICATE-----
            [...]
      -----END CERTIFICATE-----


```

The contents of the ``secured-passthrough-route`` is given as follows:

```yml
apiVersion: v1
kind: Route
metadata:
  name: secured-passthrough-route
spec:
  host: secured-passthrough-route.openshift.citrix-cic.com
  to:
    kind: Service
    name: svc-apache-multi-ssl
  tls:
    termination: passthrough
```

The contents of the ``secured-reencrypt-route.yaml`` is given as follows:

```yml
apiVersion: v1
kind: Route
metadata:
  name: secured-reencrypt-route
spec:
  host: secured-reencrypt-route.openshift.citrix-cic.com
  path: "/"
  to:
    kind: Service
    name: svc-apache-multi-ssl
  tls:
    termination: reencrypt

    key: |-
      -----BEGIN RSA PRIVATE KEY-----
            [...]
      -----END RSA PRIVATE KEY-----

    certificate: |-
      -----BEGIN CERTIFICATE-----
            [...]
      -----END CERTIFICATE-----

    destinationCACertificate: |-
      -----BEGIN CERTIFICATE-----
            [...]
      -----END CERTIFICATE-----
```

