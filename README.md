# **Description**

This repository contains the CITRIX ingress controller built around the Kubernetes Ingress resource that automatically configures CITRIX ADC based upon ingress resource.
Learn more about using Ingress on [k8s.io](https://kubernetes.io/docs/concepts/services-networking/ingress/) 

# **What is an Ingress Controller?**

Configuring a  ADC is harder in kubernetes environment where microservices will be coming up and going down.
The Ingress resource simplifies the configuration, and an Ingress controller is meant to handle it.
An Ingress Controller is a daemon, deployed as a Kubernetes Pod, that watches the apiserver's for ingresses  updates and configures the Ingress ADC accordingly.

# **Examples**

Loadbalance simple, multi-tier web application using Citrix Ingress Contoller [Quick Deploy](./example). 

# **Questions**
For questions and support please use https://discussions.citrix.com/forum/1657-netscaler-cpx/ forum. 

# **Issues**
Describe the Issue in Details, Collects the logs and  Use the forum mentioned below
```
   https://discussions.citrix.com/forum/1657-netscaler-cpx/
  
   Get Logs: kubectl logs citrix-k8s-ingress-controller > log_file
```

# **Code of Conduct**
This project adheres to the [Kubernetes Community Code of Conduct](https://github.com/kubernetes/community/blob/master/code-of-conduct.md). By participating in this project you agree to abide by its terms.

# **License**
[Apache License 2.0](./license/LICENSE)
