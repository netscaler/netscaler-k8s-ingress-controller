# Installing Citrix IPAM controller

IPAM controller is an application provided by Citrix for IP address management and it runs in parallel to the Citrix ingress controller in the Kubernetes cluster. It automatically allocates IP addresses to services of type LoadBalancer and ingress resources from a specified IP address range.

The IPAM controller requires the [VIP](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/crds/vip.md) custom resource definition (CRD) provided by Citrix. The VIP CRD is used for internal communication between the Citrix ingress controller and the Citrix IPAM controller.

## Prerequisites

You must perform the following steps before installing Citrix IPAM controller:

-  You need a Kubernetes cluster and kubectl command-line tool to communicate with the cluster.

-  This tutorial uses a separate namespace called `netscaler`  for keeping things isolated. Run the following command to create a separate namespace:

        kubectl create namespace netscaler

-  Deploy your application. For this tutorial, a sample application `cnn-website` is used. Deploy the application using the following YAML in the `netscaler` namespace:

        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: cnn-website
          labels:
              name: cnn-website      
              app: cnn-website     
        spec:
          selector:
            matchLabels:
               app: cnn-website     
          replicas: 2
          template:
            metadata:
              labels:
                name: cnn-website     
                app: cnn-website     
            spec:
              containers:
              - name: cnn-website     
                image: ns-local-docker.repo.citrite.net/apoorvak/cnnapp:v1    
                ports:
                - name: http-80
                  containerPort: 80
                - name: https-443
                  containerPort: 443

-  You need to install Citrix ingress controller for your NetScaler VPX or MPX, and the VIP CRD. Use the following Helm commands:

        helm repo add citrix https://citrix.github.io/citrix-helm-charts/
        
        helm install demo1 citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,adcCredentialSecret=<Secret-for-ADC-credentials>,ingressClass[0]=netscaler,serviceClass[0]=netscaler,ipam=true,crds.install=true -n netscaler

    For detailed information on deploying and configuring Citrix ingress controller using Helm charts see [the Helm chart repository](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-ingress-controller).

    **Note:**
     Make sure that you create a secret using the Tier-1 NetScaler VPX or MPX credentials before performing this step.

## Deploy IPAM controller

For deploying IPAM controller, use the following Helm command:

    helm repo add citrix https://citrix.github.io/citrix-helm-charts/

    helm install demo2 citrix/citrix-ipam-controller --set vipRange='[{"cnn": ["<ip-range>"]}]' -n netscaler

For information about all the configurable parameters that can be used while installing IPAM controller using Helm charts, see the [Helm chart repository](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-ipam-controller).

## Use IPAM controller for services of type LoadBalancer

For using IPAM controller for your service of type LoadBalancer, you must add the annotation `service.citrix.com/ipam-range` and the value of the annotation should be the key of the VIP range provided while deploying Citrix IPAM controller.

For example, for our sample application deploy the following service in the `netscaler` namespace:
```
    apiVersion: v1
    kind: Service
    metadata:
      name: cnn-website
      labels:
        app: cnn-website
      annotations:
        # CIC uses below annotation to select services to be configured on Netscaler VPX/MPX
        service.citrix.com/class: 'netscaler'
        # IPAM uses below annotation to select the IP Range, from which it will allocate IPs
        service.citrix.com/ipam-range: 'cnn'
    spec:
      type: LoadBalancer
      ports:
      - name: http-80
        port: 80
        targetPort: 80
      - name: https-443
        port: 443
        targetPort: 443
      selector:
        name: cnn-website
```

## Use IPAM controller for Ingress

If you want to expose your application using Ingress, then IPAM controller can be used to manage and allocate IP addresses to configure these ingress resources in the tier-1 NetScaler VPX or MPX.

1.  Deploy a service for your application. For your sample application, deploy the following service in the `netscaler` namespace:

        apiVersion: v1
        kind: Service
        metadata:
          name: cnn-website
          labels:
            app: cnn-website
        spec:
          type: ClusterIP
          ports:
          - name: http-80
            port: 80
            targetPort: 80
          - name: https-443
            port: 443
            targetPort: 443
          selector:
            name: cnn-website

1.  Deploy the Ingress to expose your application to the tier-1 NetScaler VPX or MPX. You must add the annotation `ingress.citrix.com/ipam-range` and the value of the annotation should be the key of the VIP range provided while installing the IPAM controller.

        apiVersion: extensions/v1beta1
        kind: Ingress
        metadata:
          name: vpx-ingress
          annotations:
            # CIC uses below annotation to select services to be configured on Netscaler VPX/MPX
            kubernetes.io/ingress.class: 'netscaler'
            # IPAM uses below annotation to select the IP Range, from which it allocates IPs
            ingress.citrix.com/ipam-range: 'cnn'
        spec:
          rules:
          - host: "cnn-website.com"
            http:
              paths:
              - path: /
                backend:
                  serviceName: cnn-website
                  servicePort: 80

## Multiple IP address allocations

For Ingress resources, an IP address can be allocated multiple times since a single content switching virtual server may be handling multiple ingress resources.  If the specified IP range has only a single IP address, it is allocated multiple times. But, if the named IP range consists of multiple IP addresses, only one of them is constantly allocated.

To facilitate multiple allocations, the IPAM controller keeps track of allocated IP addresses. The IPAM controller places an IP address into the free pool only when all allocations of that IP address by Ingress resources are released.

## Allocations by different resources

Both services of type LoadBalancer and Ingress resources can use the IPAM controller for IP allocations at the same time. If an IP address is allocated by one type of resource, it is not available for a resource of another type. But, the same IP address may be used by multiple ingress resources.
