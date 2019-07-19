# Expose services of type LoadBalancer

In a single-tier deployment, the Ingress Citrix ADC (VPX or MPX) outside the Kubernetes cluster receives all the Ingress traffic to the microservices deployed in the Kubernetes cluster. You need to establish network connectivity between the Ingress Citrix ADC instance and the pods for the ingress traffic to reach the microservices.

The microservice is accessed using a dedicated service. You can create the service of type `LoadBalancer` and expose it outside the Kubernetes cluster. Service of type `LoadBalancer` is natively support in managed Kubernetes deployments on public clouds such as, AWS, GCP, or Azure. In cloud deployments, when you create a service of type `LoadBalancer`, a cloud managed load balancer is assigned to the service and the service is exposed using the load balancer. Achieving a similar solution for service of type `LoadBalancer` for on-premises Kubernetes deployment is a challenge.

The Citrix ingress controller supports the services of type `LoadBalancer`. You can create a service of type `LoadBalancer` and expose it using the ingress Citrix ADC in Tier-1. The ingress Citrix ADC provisions a load balancer for the service and an IP address is assigned to the service.

You can manually assign an IP address to the service using the `service.citrix.com/frontend-ip` annotation. Else, you can also automatically assign IP address to service using the **IPAM controller** provided by Citrix.

## Difference between service of type LoadBalancer and an Ingress

Service of type `LoadBalancer` is a service type in Kubernetes. When you deploy the service, it automatically configures an external load balancer, which in this case is a Citrix ADC VPX. The service of type `LoadBalancer` does not require any Ingress resource as the service itself configures the Citrix ADC VPX with a virtual IP address. And, the service can be accessed using the IP address.

Therefore, in the case of services of type `LoadBalancer`, you need to just deploy the service to access the service. When the service is deployed, the external IP address provided using the **IPAM controller** or the `service.citrix.com/frontend-ip` annotation is configured on the Citrix ADC VPX. The service is accessed using the external IP address without the need of any ingress resource.  

## Expose services of type LoadBalancer using a standalone IP address

Create a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), in your service definition file, specify `spec.type:LoadBalancer` and specify an IP address in the `service.citrix.com/frontend-ip` annotation.

When you create a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), the Citrix ingress controller configures the IP address you have defined in the `service.citrix.com/frontend-ip` annotation as virtual IP (VIP) in Citrix ADX. And, the service is exposed using the IP address.

In this section, we shall create a Deployment, `apache`, and deploy it in your Kubernetes cluster. The following is a manifest for the Deployment:

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
  annotations:  
    service.citrix.com/frontend-ip: "110.217.212.16"
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
---
```

Note that `10.217.212.16` is added as the standalone IP address of the service using the `service.citrix.com/frontend-ip`.

Copy the manifest to a file named `apache-service.yaml` and create the Deployment using the following command:

    kubectl create -f apache-service.yaml

When you create the service (`apache`) of type `LoadBalancer`, the Citrix ingress controller configures `10.217.212.16` as virtual IP address (VIP) in Citrix ADC VPX.

View the service using the following command:

    kubectl get service apache --output yaml

Output:

    apiVersion: v1
    kind: Service
    metadata:
      annotations:
        NETSCALER_VPORT: "80"
        service.citrix.com/frontend-ip: 10.217.212.16
      creationTimestamp: "2019-06-27T05:44:57Z"
      labels:
        name: apache
      name: apache
      namespace: default
      resourceVersion: "7905848"
      selfLink: /api/v1/namespaces/default/services/apache
      uid: b2712fac-989e-11e9-a0a9-527c8bde541f
    spec:
      clusterIP: 10.103.129.16
      externalIPs:
      - 10.217.212.16
      externalTrafficPolicy: Local
      healthCheckNodePort: 31621
      ports:
      - name: http
        nodePort: 30014
        port: 80
        protocol: TCP
        targetPort: http
      selector:
        app: apache
      sessionAffinity: None
      type: LoadBalancer
    status:
      loadBalancer: {}

### Access the service

You can access the `apache` service using the standalone IP address (`10.217.212.16`) that you had assigned to the service. Use the `curl` command to access the service:

    curl 10.217.212.16

The response should be:

    <html><body><h1>It works!</h1></body></html>

## Expose services of type LoadBalancer using an IP address from the Citrix IPAM controller

When creating a service of type [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), you can use IPAM controller to automatically allocate an IP address to the service.

Citrix provides a controller called **IPAM controller** for IP address management. You must deploy the IPAM controller as a separate pod along with Citrix ingress controller. Once the IPAM controller is deployed, it allocates IP address to the service from a defined IP address range. The Citrix ingress controller configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADX. And, the service is exposed using the IP address.

The IPAM controller requires the Vip [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRD) provided by Citrix for asynchronous communication between the IPAM controller and Citrix ingress controller.

When a new service is created, the Citrix ingress controller creates a CRD object for the service with an empty IP address field. The IPAM Contr>oller listens to addition, deletion, or modification of the CRD and updates it with an IP address to the CRD. Once the CRD object is updated, the Citrix ingress controller automatically configures Citrix ADC-specfic configuration in the tier-1 Citrix ADC VPX.

In this section, we shall deploy the IPAM controller, create a sample Deployment, create a service of type LoadBalancer, and access the service.

### Deploy the IPAM controller

Before you deploy the IPAM controller, deploy the Citrix VIP CRD. For more information see, [VIP CustomResourceDefinitions](../crds/vip.md).

After you have deployment the Citrix VIP CRD, create the Citrix ingress controller with the `--ipam=citrix-ipam-controller` argument in the `args` field.

The following is the manifest of the Citrix ingress controller:

```yml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cic-k8s-role
rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "ingresses", "pods", "secrets","nodes"]
    verbs: ["*"]
  - apiGroups: ["extensions"]
    resources: ["ingresses", "ingresses/status"]
    verbs: ["*"]
  - apiGroups: ["citrix.com"]
    resources: ["rewritepolicies"]
    verbs: ["*"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["*"]

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
apiVersion: rbac.authorization.k8s.io/v1

---

apiVersion: v1
kind: ServiceAccount
metadata:
  name: cic-k8s-role
  namespace: default

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
        image: "quay.io/citrix/citrix-k8s-ingress-controller:1.2.0"
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
          - --ipam=citrix-ipam-controller
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
        # This IPAM controller takes environment variable VIP_RANGE. IP addresses in this range are used to assign values for IP range
        - name: "VIP_RANGE"
          value: '["10.217.212.18/31"]'
        # The IPAM controller can also be configured with name spaces for which it would work through the environment variable
        # VIP_NAMESPACES, This expects a set of namespaces passed as space separated string
```

The manifest contains two environment variables, `VIP_RANGE` or `VIP_NAMESPACES`.

-  `VIP_RANGE` - Use the environment variable to define the IP address range. The IPAM controller assigns the IP address from this IP address range to the service.

-  `VIP_NAMESPACES` - Use the environment variable you can define IPAM controller to work only for a set of namespaces.

Copy the manifest to a file named, `citrix-ipam-controller.yaml`, and update the `VIP_RANGE` or `VIP_NAMESPACES` environment variables based on your requirement. Create the Deployment using the following command:

    kubectl create -f citrix-ipam-controller.yaml

### Deploy the Apache microservice application

Create a Deployment, `apache`, and deploy it in your Kubernetes cluster. The following is a manifest for the Deployment:

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

Copy the manifest to a file named, `apache-deployment.yaml` and create the Deployment using the following command:

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

### Access the service

You can access the `apache` service using the IP address assigned by IPAM controller to the service. Use the `curl` command to access the service:

    curl <IP_address>

The response should be:

    <html><body><h1>It works!</h1></body></html>
