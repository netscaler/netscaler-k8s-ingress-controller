# Citrix Ingress Controller Helm Charts

This[https://github.com/citrix/citrix-helm-charts] repository contains [helm](https://helm.sh) charts of Citrix ingress controller configuring Citrix ADC CPX, VPX or MPX in [Kubernetes](https://kubernetes.io) and [OpenShift](https://www.openshift.com) platform.

> Note: Charts may require access to kube-system namespace and/or cluster wide permissions for full functionality. Install/configure helm/tiller appropriately.

###### Charts
[citrix-k8s-cpx-ingress-controller](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-k8s-cpx-ingress-controller) - Use this chart to deploy Citrix ADC CPX with Citrix ingress controller running as [side car](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/).

[citrix-k8s-ingress-controller](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-k8s-ingress-controller) - Use this chart to deploy Citrix ingress controller configuring Citrix ADC VPX/MPX.

## Documentation
Each charts README describe the functionality and values.yaml shows the default values.

## Examples
[This section](https://github.com/citrix/citrix-helm-charts/tree/master/examples) contains examples on how the above mentioned charts can be used.

##### Charts
[citrix-k8s-cpx-ingress-controller](https://github.com/citrix/citrix-helm-charts/tree/master/examples/citrix-k8s-cpx-ingress-controller) - Use this chart to deploy Citrix ADC CPX with Citrix ingress controller running as sidecar, load balancing Guestbook App in a Kubernetes cluster on in an OpenShift platform.

[citrix-k8s-ingress-controller](https://github.com/citrix/citrix-helm-charts/tree/master/examples/citrix-k8s-ingress-controller) - Use this chart to deploy Citrix ingress controller configuring Citrix ADC VPX/MPX load balancing Guestbook App in a Kubernetes cluster on in an OpenShift platform.
