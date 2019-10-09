# Expose services of type LoadBalancer

In a single-tier deployment, the Ingress Citrix ADC (VPX or MPX) outside the Kubernetes cluster receives all the Ingress traffic to the microservices deployed in the Kubernetes cluster. You need to establish network connectivity between the Ingress Citrix ADC instance and the pods for the ingress traffic to reach the microservices.

The microservice is accessed using a dedicated service. You can create the service of type `LoadBalancer` and expose it outside the Kubernetes cluster. Service of type `LoadBalancer` is natively support in managed Kubernetes deployments on public clouds such as, AWS, GCP, or Azure. In cloud deployments, when you create a service of type `LoadBalancer`, a cloud managed load balancer is assigned to the service and the service is exposed using the load balancer. Achieving a similar solution for service of type `LoadBalancer` for on-premises Kubernetes deployment is a challenge.

The Citrix ingress controller supports the services of type `LoadBalancer`. You can create a service of type `LoadBalancer` and expose it using the ingress Citrix ADC in Tier-1. The ingress Citrix ADC provisions a load balancer for the service and an IP address is assigned to the service.

You can manually assign an IP address to the service using the `spec.loadBalancerIP` field in your service definition. Else, you can also automatically assign IP address to service using the **IPAM controller** provided by Citrix.

## Difference between service of type LoadBalancer and an Ingress

Service of type `LoadBalancer` is a service type in Kubernetes. When you deploy the service, it automatically configures an external load balancer, which in this case is a Citrix ADC VPX. The service of type `LoadBalancer` does not require any Ingress resource as the service itself configures the Citrix ADC VPX with a virtual IP address. And, the service can be accessed using the IP address.

Therefore, in the case of services of type `LoadBalancer`, you need to deploy the ingress resource to access the service. When the service is deployed, the external IP address provided using the **IPAM controller** or `spec.loadBalancerIP`  is configured on the Citrix ADC VPX. The service is accessed using the external IP address without the need of any ingress resource.  

## Expose services of type LoadBalancer using a standalone IP address

Create a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), in your service definition file, specify `spec.type:LoadBalancer` and specify an IP address in the `spec.loadBalancerIP` field.

When you create a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), the Citrix ingress controller configures the IP address you have defined in the `spec.loadBalancerIP` field as virtual IP (VIP) in Citrix ADX. And, the service is exposed using the IP address.

In this section, we shall deploy an `apache` application in your Kubernetes cluster. The following is a manifest for the Deployment:

```yml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: apache
  labels:
      name: apache
spec:
  selector:
    matchLabels:
      app: apache
  replicas: 8
  template:
    metadata:
      labels:
        app: apache
    spec:
      containers:
      - name: apache
        image: httpd:latest
        ports:
        - name: http
          containerPort: 80
        imagePullPolicy: IfNotPresent
```

The containers in this Deployment listen on port 80.

Copy the manifest to a file named `apache-deployment.yaml` and create the Deployment using the following command:

    kubectl create -f apache-deployment.yaml

Verify that eight Pods are running using the following:

    kubectl get pods

Output:

    NAME                         READY   STATUS              RESTARTS   AGE
    apache-7db8f797c7-5fwwk      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-69mj5      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-84xxk      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-dvsml      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-gq5zw      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-mtk4x      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-rjckb      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-w2wlp      0/1     ContainerCreating   0          6s

The following is a manifest for a service of type `LoadBalancer`.

```yml
apiVersion: v1
kind: Service
metadata:
  name: apache
  labels:
    name: apache
spec:
  externalTrafficPolicy: Local
  loadBalancerIP: "110.217.212.16"
  type: LoadBalancer
  selector:
    name: apache
  ports:
  - name: http
    port: 80
    targetPort: http
  selector:
    app: apache
---
```

Note that `10.217.212.16` is added as the standalone IP address of the service using the `service.citrix.com/frontend-ip`.

Copy the manifest to a file named `apache-service.yaml` and create the Deployment using the following command:

    kubectl create -f apache-service.yaml

When you create the service (`apache`) of type `LoadBalancer`, the Citrix ingress controller configures `10.217.212.16` as virtual IP address (VIP) in Citrix ADC VPX.

### Access the service

You can access the `apache` service using the standalone IP address (`10.217.212.16`) that you had assigned to the service. Use the `curl` command to access the service:

    curl 10.217.212.16

The response should be:

    <html><body><h1>It works!</h1></body></html>

## Expose services of type LoadBalancer using an IP address from the Citrix IPAM controller

When creating a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), you can use IPAM controller to automatically allocate an IP address to the service.

Citrix provides a controller called **IPAM controller** for IP address management. You must deploy the IPAM controller as a separate pod along with the Citrix ingress controller. Once the IPAM controller is deployed, it allocates IP address to the service from a defined IP address range. The Citrix ingress controller configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADX. And, the service is exposed using the IP address.

The IPAM controller requires the Vip [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRD) provided by Citrix for asynchronous communication between the IPAM controller and Citrix ingress controller.

When a new service is created, the Citrix ingress controller creates a VIP CRD object for the service with an empty IP address field. The IPAM Controller listens for addition, deletion, or modification of the VIP CRD and updates it with an IP address to the VIP CRD. Once the VIP CRD object is updated, the Citrix ingress controller automatically configures Citrix ADC-specfic configuration in the ier-1 Citrix ADC VPX.

In this section, we shall deploy the IPAM controller, create a sample Deployment, create a service of type LoadBalancer, and access the service.

### Deploy the IPAM controller

Before you deploy the IPAM controller, deploy the Citrix VIP CRD. For more information see, [VIP CustomResourceDefinitions](../crds/vip.md).

After you have deployment the Citrix VIP CRD, create the Citrix ingress controller with the `--ipam.citrix-ipam-controller` argument in the `args` field.

The following is the manifest of the Citrix ingress controller:

```yml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cic-k8s-role
rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "ingresses", "pods", "secrets", "routes", "routes/status", "nodes", "namespaces"]
    verbs: ["*"]
  - apiGroups: ["extensions"]
    resources: ["ingresses", "ingresses/status"]
    verbs: ["*"]
  - apiGroups: ["citrix.com"]
    resources: ["rewritepolicies", "vips"]
    verbs: ["*"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["*"]
  - apiGroups: ["apiextensions.k8s.io"]
    resources: ["customresourcedefinitions"]
    verbs: ["get", "list", "watch"]

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cic-k8s-role
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cic-k8s-role
subjects:
- kind: ServiceAccount
  name: cic-k8s-role
  namespace: default

---

apiVersion: v1
kind: ServiceAccount
metadata:
  name: cic-k8s-role
  namespace: default

---
apiVersion: v1
kind: Pod
metadata:
  name: cic-k8s-ingress-controller
  labels:
    app: cic-k8s-ingress-controller
spec: 
      serviceAccountName: cic-k8s-role
      containers:
      - name: cic-k8s-ingress-controller
        image: "quay.io/citrix/citrix-k8s-ingress-controller:1.4.392"
        env:
         # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled) 
         - name: "NS_IP"
           value: "x.x.x.x"
         # Set username for Nitro
         - name: "NS_USER"
           valueFrom:
            secretKeyRef:
             name: nslogin
             key: username
         # Set user password for Nitro
         - name: "NS_PASSWORD"
           valueFrom:
            secretKeyRef:
             name: nslogin
             key: password
         # Set log level
         - name: "EULA"
           value: "yes"
        args:
          - --ingress-classes
            citrix
          - --feature-node-watch
            false
          - --ipam
            citrix-ipam-controller
        imagePullPolicy: Always
```

Copy the manifest to a file name, `cic-k8s-ingress-controller.yaml`, and create the Deployment using the following command:

    kubectl create -f cic-k8s-ingress-controller.yaml

For more information on how to deploy the Citrix ingress controller, see the [Deploy Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/).

Now, deploy the IPAM controller. The following is manifest of the IPAM controller Deployment:

```yml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: citrix-ipam-controller
  namespace: kube-system
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: citrix-ipam-controller
rules:
- apiGroups:
  - citrix.com
  resources:
  - vips
  verbs:
  - '*'
- apiGroups:
  - apiextensions.k8s.io
  resources:
  - customresourcedefinitions
  verbs:
  - '*'
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: citrix-ipam-controller
subjects:
- kind: ServiceAccount
  name: citrix-ipam-controller
  namespace: kube-system
roleRef:
  kind: ClusterRole
  apiGroup: rbac.authorization.k8s.io
  name: citrix-ipam-controller

---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: citrix-ipam-controller
  namespace: kube-system
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: citrix-ipam-controller
    spec:
      serviceAccountName: citrix-ipam-controller
      containers:
      - name: citrix-ipam-controller
        image: quay.io/citrix/citrix-ipam-controller:latest
        env:
        # This IPAM controller takes environment variable VIP_RANGE. IPs in this range are used to assign values for IP range
        - name: "VIP_RANGE"
          value: '["10.105.158.195/32", "10.105.158.196/31", "10.105.158.198"]'
        # The IPAM controller can also be configured with name spaces for which it would work through the environment variable
        # VIP_NAMESPACES, This expects a set of namespaces passed as space separated string
```

The manifest contains two environment variables, `VIP_RANGE` or `VIP_NAMESPACES`.

-  `VIP_RANGE` - Use the environment variable to define the IP address range. The IPAM controller assigns the IP address from this IP address range to the service.

    For example:

    To define the IP address range from a subnet:

        - name: "VIP_RANGE"
          value: '["10.xxx.xxx.18/31"]'

    To define the IP address range from multiple subnets, ensure that the values are valid CIDRs for the subnets.

        - name: "VIP_RANGE"
          value: '["10.217.212.18/31",  "10.217.212.20/31", "10.217.212.16/30", "10.217.212.0/24"]'

    Also, you can use dash (`-`) to define the IP address range:

        - name: "VIP_RANGE"
          value: '["10.217.212.18 - 10.217.212.21",  “10.217.212.27 - 10.217.212.31",  “10.217.213.24 - 10.217.213.32" ]'

-  `VIP_NAMESPACES` - Use the environment variable you can define IPAM controller to work only for a set of namespaces.

Copy the manifest to a file named, `citrix-ipam-controller.yaml`, and update the `VIP_RANGE` or `VIP_NAMESPACES` environment variables based on your requirement. Create the Deployment using the following command:

    kubectl create -f citrix-ipam-controller.yaml

### Deploy the Apache microservice application

Deploy an `apache` application in your Kubernetes cluster. The following is a manifest for the Deployment:

```yml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: apache
  labels:
      name: apache
spec:
  selector:
    matchLabels:
      app: apache
  replicas: 8
  template:
    metadata:
      labels:
        app: apache
    spec:
      containers:
      - name: apache
        image: httpd:latest
        ports:
        - name: http
          containerPort: 80
        imagePullPolicy: IfNotPresent
```

The containers in this Deployment listen on port 80.

Copy the manifest to a file named, `apache-deployment.yaml` , and create the Deployment using the following command:

    kubectl create -f apache-deployment.yaml

Verify that eight Pods are running using the following:

    kubectl get pods

Output:

    NAME                         READY   STATUS              RESTARTS   AGE
    apache-7db8f797c7-5fwwk      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-69mj5      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-84xxk      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-dvsml      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-gq5zw      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-mtk4x      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-rjckb      0/1     ContainerCreating   0          6s
    apache-7db8f797c7-w2wlp      0/1     ContainerCreating   0          6s

### Expose the Apache microservice using service of type LoadBalancer

Create a service (`apache`) of type `LoadBalancer`. The following is a manifest for a service of type `LoadBalancer`:

```yml
apiVersion: v1
kind: Service
metadata:
  name: apache
  labels:
    name: apache
spec:
  externalTrafficPolicy: Local
  loadBalancerIP: "110.217.212.16"
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

Copy the manifest to a file named `apache-service.yaml` and create the Deployment using the following command:

    kubectl create -f apache-service.yaml

When you create the service (`apache`) of type `LoadBalancer`, the IPAM controller assigns an IP address to the `apache` service from the IP address range you had defined in the IPAM controller deployment. The Citrix ingress controller configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADX. And, the service is exposed using the IP address.

View the service using the following command:

    kubectl get service apache --output yaml

Output:

    NAME                      READY   STATUS   RESTARTS   AGE
    apache-7db8f797c7-2x6jc   1/1     Running   0          8s
    apache-7db8f797c7-cdgmw   1/1     Running   0          8s
    apache-7db8f797c7-lh447   1/1     Running   0          8s
    apache-7db8f797c7-m7mhd   1/1     Running   0          8s
    apache-7db8f797c7-m9rn7   1/1     Running   0          8s
    apache-7db8f797c7-r9jgz   1/1     Running   0          8s
    apache-7db8f797c7-vwhc8   1/1     Running   0          8s
    apache-7db8f797c7-zslwv   1/1     Running   0          8s

### Access the service

You can access the `apache` service using the IP address assigned by IPAM controller to the service. Use the `curl` command to access the service:

    curl <IP_address>

The response should be:

    <html><body><h1>It works!</h1></body></html>

## Example: Expose microservices using services of type LoadBalancer in Citrix ADC dual-tier deployment

In this example, you will learn how to expose microservices using services of type LoadBalancer in a Citrix ADC [dual-tier](../deployment-topologies#dual-tier-topology) deployment.

Citrix ADC in a [dual-tier](../deployment-topologies#dual-tier-topology) deployment solution enables you to load balance enterprise grade applications deployed in microservices and access them through internet. In the dual-tier deployment, you can deploy Citrix ADC VPX, MPX, or CPX as a traditional load balancer in Tier-1 to manage high scale North-South traffic to the microservices. And, in Tier-2, you can deploy Citrix ADC CPX to load balance the North-South and East-West traffic to the microservices.

In this example, a Citrix ADC VPX is used in Tier-1 to load balance North-South traffic and a Citrix ADC CPX used in Tier-2 to load balance the North-South and East-West traffic.

The following diagram depicts the microservice deployment used in this example. The deployment contains three services that are highlighted in blue, red, and green colors respectively. And, 12 pods running across two worker nodes. These deployments are logically categorized by Kubenetes namespace (for example, team-hotdrink namespace).

![Sample microservice deployment](../media/sample-deployment.png)

### Prerequisites

Ensure that you have:

-  Deployed a Kubernetes cluster. For more information, see [https://kubernetes.io/docs/setup/scratch/](https://kubernetes.io/docs/setup/scratch/).
-  Set up the Kubernetes dashboard for deploying containerized applications. For more information, see [https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).
-  The route configuration present in Tier-1 Citrix ADC so that the Ingress Citrix ADC is able to reach the Kubernetes pod network for seamless connectivity. For detailed instructions, see [Manually configure route on the Citrix ADC instance](staticrouting.md#manually-configure-route-on-the-citrix-adc-instance).

**To deploy microservices using Kubernetes service of type LoadBalancer solution:**

1.  Clone the GitHub repository to your Master node using following command:

        git clone https://github.com/citrix/example-cpx-vpx-for-kubernetes-2-tier-microservices.git

1.  Using the master nodes' CLI console, create namespaces using the following command:

        kubectl create -f namespace.yaml

    Verify if the namespaces are created in your Kubernetes cluster using the following command:

        kubectl get namespaces

    The output of the command should be:

    ![Namespace](../media/namespaces.png)

1.  From the Kubernetes dashboard, deploy the `rbac.yaml` in the default namespace using the following command:

        kubectl create -f rbac.yaml 

1.  Deploy the Citrix IPAM CRD and Citrix IPAM controller for automatically assigning IP addresses to the Kubernetes services. Use the following command:

        kubectl create -f vip.yaml
        kubectl create -f ipam_deploy.yaml

1.  Deploy the Citrix ADC CPX for `hotdrink`, `colddrink` , and `guestbook` microservices using following commands:

        kubectl create -f cpx.yaml -n tier-2-adc
        kubectl create -f hotdrink-secret.yaml -n tier-2-adc

1.  Deploy three types of `hotdrink` beverage microservices using following commands:

        kubectl create -f team_hotdrink.yaml -n team-hotdrink
        kubectl create -f hotdrink-secret.yaml -n team-hotdrink

1.  Deploy the `colddrink` beverage microservice using following commands:

        kubectl create -f team_colddrink.yaml -n team-colddrink
        kubectl create -f colddrink-secret.yaml -n team-colddrink

1.  Deploy the `guestbook` no SQL type microservice using following commands:

        kubectl create -f team_guestbook.yaml -n team-guestbook

1.  Log on to Tier-1 Citrix ADC to verify if no configuration is pushed from the Citrix ingress controller before automating the Tier-1 Citrix ADC.

1.  Deploy the Citrix ingress controller to push the Citrix ADC CPX configuration to the Tier-1 Citrix ADC automatically. In the `cic_vpx.yaml`, change the value of the NS_IP environment variable with your Citrix ADC VPX NS_IP. For more information on the Citrix ingress controller deployment, see [Deploy the Citrix ingress controller using YAML](../deploy/deploy-cic-yaml.md).
    
    After you update the `cic_vpx.yaml` file, deploy the file using the following command: 

        kubectl create -f cic_vpx.yaml -n tier-2-adc

1.  Verify if the Citrix IPAM controller has assigned the IP addresses to the Citrix ADC CPX services. Use the following command:

        kubectl get svc -n tier-2-adc

1.  Add the following DNS entries in your local machine host files to access the microservices using Internet:

        <frontend-ip from ingress_vpx.yaml> hotdrink.beverages.com
        <frontend-ip from ingress_vpx.yaml> colddrink.beverages.com
        <frontend-ip from ingress_vpx.yaml> guestbook.beverages.com

You can now access the microservices using the following URL: [https://hotdrink.beverages.com](https://hotdrink.beverages.com)

![Coffee and Tea Services](../media/coffee-and-tea-services.png)
