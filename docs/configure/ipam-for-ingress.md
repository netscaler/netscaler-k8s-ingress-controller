# IP address management using the Citrix IPAM controller for Ingress resources

IPAM controller is an application provided by Citrix for IP address management and it runs in parallel to the Citrix ingress controller in the Kubernetes cluster. Automatically allocating IP addresses to services of type LoadBalancer from a specified IP address range using the IPAM controller is already supported. Now, you can also assign IP addresses to Ingress resources from a specified range using the IPAM controller.

You can specify IP address ranges in the YAML file while deploying the IPAM controller using YAML. The Citrix ingress controller configures the IP address allocated to the Ingress resource as a virtual IP address (VIP) in Citrix ADC MPX or VPX.

The IPAM controller requires the VIP [CustomResourceDefinition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRD) provided by Citrix. The VIP CRD is used for internal communication between the Citrix ingress controller and the IPAM controller.

## Assign IP address for Ingress resource using the IPAM controller

This topic provides information on how to use the IPAM controller to assign IP addresses for Ingress resources.

To configure an Ingress resource with an IP address from the IPAM controller, perform the following steps:

1.  Deploy the VIP CRD
2.	Deploy the Citrix ingress controller
3.	Deploy the IPAM controller
4.	Deploy the application and Ingress resource

### Step 1: Deploy the VIP CRD

Perform the following step to deploy the Citrix VIP CRD which enables communication between the Citrix ingress controller and the IPAM controller.

    kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/crd/vip/vip.yaml

For more information on VIP CRD, see the VIP [CustomResourceDefinition](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/vip/).

### Step 2: Deploy the Citrix ingress controller

Perform the following steps to deploy the Citrix ingress controller with the IPAM controller argument.

1. Download the `citrix-k8s-ingress-controller.yaml` file using the following command:

        wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

1. Edit the Citrix ingress controller YAML file:

    - Specify the values of the environment variables as per your requirements. For more information on     specifying the environment variables, see the [Deploy Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/). Here, you don’t need to specify `NS_VIP`.

    - Specify the IPAM controller as an argument using the following:

          args:
            - --ipam
              citrix-ipam-controller

    Here is a snippet of a sample Citrix ingress controller YAML file with the IPAM controller argument:

    **Note:** This YAML is for demonstration purpose only and not the full version. Always, use the latest version of the YAML and edit as per your requirements. For the latest version see the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file.

    

        apiVersion: v1
        kind: Pod
        metadata:
          name: cic-k8s-ingress-controller
        spec:
              serviceAccountName: cic-k8s-role
              containers:
              - name: cic-k8s-ingress-controller
                image: "quay.io/citrix/citrix-k8s-ingress-controller:1.21.9"
                env:
                  - name: "NS_IP"
                    value: "x.x.x.x"
                  - name: "NS_USER"
                    valueFrom:
                    secretKeyRef:
                      name: nslogin
                      key: username
                  - name: "NS_PASSWORD"
                    valueFrom:
                    secretKeyRef:
                      name: nslogin
                      key: password
                  - name: "EULA"
                    value: "yes"
                  - name: POD_NAME
                    valueFrom:
                    fieldRef:
                      apiVersion: v1
                      fieldPath: metadata.name
                  - name: POD_NAMESPACE
                    valueFrom:
                    fieldRef:
                      apiVersion: v1
                      fieldPath: metadata.namespace
                args:
                  - --ipam citrix-ipam-controller
                imagePullPolicy: Always
    

3. Deploy the Citrix ingress controller using the edited YAML file with the following command:

        kubectl create -f citrix-k8s-ingress-controller.yaml

    For more information on how to deploy the Citrix ingress controller, see the [Deploy Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/).

### Step 3: Deploy the IPAM controller

  Perform the following steps to deploy the IPAM controller.

 1. Create a file named `citrix-ipam-controller.yaml` with the following configuration:


        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: citrix-ipam-controller
          namespace: kube-system
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: citrix-ipam-controller
          template:
            metadata:
              labels:
                app: citrix-ipam-controller
            spec:
              serviceAccountName: citrix-ipam-controller
              containers:
              - name: citrix-ipam-controller
                image: quay.io/citrix/citrix-ipam-controller:1.0.3
                env:
                # This IPAM controller takes envirnment variable VIP_RANGE. IPs in this range are used to assign values for IP range
                - name: "VIP_RANGE"
                  value: '[["10.217.6.115-10.217.6.117"], {"one-ip": ["5.5.5.5"]}, {"two-ip": ["6.6.6.6", "7.7.7.7"]}]'
                # The IPAM controller can also be configured with name spaces for which it would work through the environment variable
                # VIP_NAMESPACES, This expects a set of namespaces passed as space separated string
                imagePullPolicy: Always
      

    The manifest contains two environment variables, `VIP_RANGE` and `VIP_NAMESPACES`. You can specify the appropriate routable IP range with a valid CIDR under the `VIP_RANGE`. If necessary, you can also specify a set of namespaces under `VIP_NAMESPACES` so that the IPAM controller allocates addresses only for services or Ingress resources from specific namespaces.

2. Deploy the IPAM controller using the following command:

       kubectl create -f citrix-ipam-controller.yaml

### Step 4: Deploy Ingress resources

Perform the following steps to deploy a sample application and Ingress resource.

1. Deploy the Guestbook application using the following command:

        kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/example/guestbook/guestbook-all-in-one.yaml

2. Create the guestbook-ingress YAML file with Ingress resource definition to send traffic to the front-end of the guestbook application.

    The following is a sample YAML:

    
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: guestbook-ingress
          annotations:
        annotations:
          ingress.citrix.com/ipam-range: "two-ip"
          #ingress.citrix.com/frontend-ip: "5.5.5.5"
          kubernetes.io/ingress.class: "cic-vpx"
        spec:
          rules:
          - host:  www.guestbook.com
            http:
              paths:
              - path: /
                backend:
                  serviceName: frontend
                  servicePort: 80

3. Deploy the Ingress resource.

        kubectl create -f guestbook-ingress.yaml

**Multiple IP address allocations**

For Ingress resources, an IP address can be allocated multiple times since multiple ingress resources may be handled by a single csvserver. If the specified IP range has only a single IP address, it is allocated multiple times. But, if the named IP range consists of multiple IP addresses, only one of them is constantly allocated.

To facilitate multiple allocations, the IPAM controller keeps track of allocated IP addresses. The IPAM controller places an IP address into the free pool only when all allocations of that IP address by Ingress resources are released.

**Allocations by different resources**

Both services of type LoadBalancer and Ingress resources can use the IPAM controller for IP allocations at the same time. If an IP address is allocated by one type of resource, it is not available for a resource of another type. But, the same IP address may be used by multiple ingress resources.
