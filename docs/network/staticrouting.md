# Configure static route on Ingress Citrix ADC VPX or MPX

In a Kubernetes cluster, pods run on an overlay network. The overlay network can be Flannel, Calico, Weave, and so on. The pods in the cluster are assigned with an IP address from the overlay network which is different from the host network.

The Ingress Citrix ADC VPX or MPX outside the Kubernetes cluster receives all the Ingress traffic to the microservices deployed in the Kubernetes cluster. You need to establish network connectivity between the Ingress Citrix ADC instance and the pods for the ingress traffic to reach the microservices.

One of the ways to achieve network connectivity between pods and Citrix ADC VPX or MPX instance outside the Kubernetes cluster is to configure routes on the Citrix ADC instance to the overlay network.

You can either do this manually or Citrix ingress controller provides an option to automatically configure the network.

!!! note "Note"
    Ensure that the Citrix ADC instance (MPX or VPX) has SNIP configured on the host network. The host network is the network on which the Kubernetes nodes communicate with each other.

## Manually configure route on the Citrix ADC instance

Perform the following:

1.  On the master node in the Kubernetes cluster, get the podCIDR using the following command:

        # kubectl get nodes -o jsonpath="{range .items[*]}{'podNetwork: '}{.spec.podCIDR}{'\t'}{'gateway: '}{.status.addresses[0].address}{'\n'}{end}"

          podNetwork: 10.244.0.0/24    gateway: 10.106.162.108
          podNetwork: 10.244.2.0/24    gateway: 10.106.162.109
          podNetwork: 10.244.1.0/24    gateway: 10.106.162.106

    If you are using **Calico** CNI then use the following command to get the podCIDR:

        # kubectl get nodes -o jsonpath="{range .items[*]}{'podNetwork: '}{.metadata.annotations.projectcalico\.org/IPv4IPIPTunnelAddr}{'\tgateway: '}{.metadata.annotations.projectcalico\.org/IPv4Address}{'\n'}"

          podNetwork: 192.168.109.0       gateway: 10.106.162.108/24
          podNetwork: 192.168.174.0       gateway: 10.106.162.109/24
          podNetwork: 192.168.76.128      gateway: 10.106.162.106/24

1.  Log on to the Citrix ADC instance.

1.  Add route on the Citrix ADC instance using the podCIDR information. Use the following command:

        add route <pod_network> <podCIDR_netmask> <gateway>

    For example,

        add route 192.244.0.0 255.255.255.0 192.106.162.108

        add route 192.244.2.0 255.255.255.0 192.106.162.109

        add route 192.244.1.0 255.255.255.0 192.106.162.106

## Automatically configure route on the Citrix ADC instance

In the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file, you can use an argument,`feature-node-watch` to automatically configure route on the associated Citrix ADC instance.

Set the `feature-node-watch` argument to `true` to enable automatic route configuration.

You can specify this argument in the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file as follows:

```yml
   spec:
        serviceAccountName: cic-k8s-role
        containers:
        - name: cic-k8s-ingress-controller
          image: "quay.io/citrix/citrix-k8s-ingress-controller:1.23.10"
        # feature-node-watch argument configures route(s) on the Ingress Citrix ADC
        # to provide connectivity to the pod network. By default, this feature is disabled.
        args:
        - --feature-node-watch
          true
```

!!! info "Points to Note"
    - By default, the `feature-node-watch` argument is set to `false`. Set the argument to `true` to enable the automatic route configuration.
    - For automatic route configuration, you must provide permissions to listen to the events of nodes resource type. You can provide the required permissions in the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file as follows:

```yml
  kind: ClusterRole
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    name: cic-k8s-role
  rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "ingresses", "pods", "secrets", "nodes"]
    verbs: ["*"]
```