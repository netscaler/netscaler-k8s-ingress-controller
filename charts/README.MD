# Citrix Ingress Controller Helm Charts

This repository contains [helm](https://helm.sh) charts of Citrix ingress controller configuring Citrix ADC CPX, VPX or MPX in [Kubernetes](https://kubernetes.io) and [OpenShift](https://www.openshift.com) platform.

> Note: Charts may require access to kube-system namespace and/or cluster wide permissions for full functionality. Install/configure helm/tiller appropriately.


## Stable Charts
The stable directory contains charts that are created and tested by Citrix.

###### Charts
[citrix-k8s-cpx-ingress-controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/stable/citrix-k8s-cpx-ingress-controller) - Use this chart to deploy Citrix ADC CPX with Citrix ingress controller running as [side car](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/).

[citrix-k8s-ingress-controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/stable/citrix-k8s-ingress-controller) - Use this chart to deploy Citrix ingress controller configuring Citrix ADC VPX/MPX.

## Documentation
Each charts README describe the functionality and values.yaml shows the default values.

## Examples
[This section](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples) contains chart where Citrix Ingress Controller load balance a simple multi-tier web application in Kubernetes.

##### Charts
[citrix-k8s-cpx-ingress-controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples/citrix-k8s-cpx-ingress-controller) -Use this chart to deploy Citrix CPX with builtin Ingress Controller load balancing Guestbook App in Kubernetes.

[citrix-k8s-ingress-controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/charts/examples/citrix-k8s-ingress-controller) -Use this chart to deploy ingress controller configuring Citrix ADC VPX/MPX load balancing Guestbook App in Kubernetes.
