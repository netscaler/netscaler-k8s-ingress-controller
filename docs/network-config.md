# Network Configuration on Ingress NetScaler Device

### Need for Network Configuration

In Kubernetes cluster, pods run in a overlay network, such as flannel, calico, weave etc. All pods get an IP address from this overlay network which is different from the host network.
Ingress NetScaler device fronting the Kubernetes cluster will be accepting all ingress traffic destined towards services deployed in Kubernetes cluster. Ingress NetScaler should be able to reach this pod network for seamless connectivity.

### Route Configuration on Ingress NetScaler

One of the viable option to achieve the connectivity between NetScaler and Pods is to configure routes on the NetScaler towards overlay network.
This can be done manually as well as Citrix Ingress Controller provides a knob to enable automatic configuration. Both approaches are explained below.

**Note:** Kindly ensure that Ingress NetScaler MPX/VPX has a SNIP present in the host-network (i.e. network over which K8S nodes communicate with each other. Usually eth0 IP is from this network).


#### i) Manual configuration of routes on NetScaler Ingress device
   
a) Obtain podCIDR using below command:
```console
    # kubectl get nodes -o jsonpath="{range .items[*]}{'podNetwork: '}{.spec.podCIDR}{'\t'}{'gateway: '}{.status.addresses[0].address}{'\n'}{end}"
      podNetwork: 10.244.0.0/24    gateway: 10.106.162.108
      podNetwork: 10.244.2.0/24    gateway: 10.106.162.109
      podNetwork: 10.244.1.0/24    gateway: 10.106.162.106
```

b) Add Route to Netscaler using info obtained in step (a).
```console
    # add route <pod_Network> <podCIDR_netmask> <gateway>
    Example:
      add route 10.244.0.0 255.255.255.0 10.106.162.108
      add route 10.244.2.0 255.255.255.0 10.106.162.109
      add route 10.244.1.0 255.255.255.0 10.106.162.106
```

#### ii) Auto configuration of routes on NetScaler Ingress device

`feature-node-watch` argument is provided for Citrix Ingress Controller which when set to `true` performs the route configuration on the associated Ingress NetScaler device.
This option can be specified in the yaml file "citrix-k8s-ingress-controller.yaml" as below:

```yaml
   spec:
        serviceAccountName: cic-k8s-role
        containers:
        - name: cic-k8s-ingress-controller
          image: "quay.io/citrix/citrix-k8s-ingress-controller:latest"
        # feature-node-watch argument configures route(s) on the Ingress NetScaler
        # to provide connectivity to the pod network. By default, this feature is disabled.
        args:
        - --feature-node-watch
          true
```

By default, `feature-node-watch` is false. It needs to be explicitly set to true if auto route configuration is required. 

**Note:** For auto route configuration, CIC should be provided with permissions to listen to events of `nodes` resource type. Example snippet of yaml is provided below to enable the same.

```yaml
   kind: ClusterRole
   apiVersion: rbac.authorization.k8s.io/v1beta1
   metadata:
     name: cic-k8s-role
   rules:
   - apiGroups: [""]
     resources: ["services", "endpoints", "ingresses", "pods", "secrets", "nodes"]
     verbs: ["*"]
```
