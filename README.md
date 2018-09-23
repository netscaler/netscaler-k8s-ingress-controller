# **Description**

This repository contains the CITRIX ingress controller built around the Kubernetes Ingress resource that automatically configures CITRIX ADC based upon ingress resource.
Learn more about using Ingress on [k8s.io](https://kubernetes.io/docs/concepts/services-networking/ingress/) 

# **What is an Ingress Controller?**

Configuring a  ADC is harder in kubernetes environment where microservices will be coming up and going down.
The Ingress resource simplifies the configuration, and an Ingress controller is meant to handle it.
An Ingress Controller is a daemon, deployed as a Kubernetes Pod, that watches the apiserver's /ingresses endpoint for updates to the Ingress resource. Its job is to satisfy requests for Ingresses  and configure the Ingress ADC accordingly.

## **Deployment** 
Use the YAML in this section to deploy Citrix Ingress Controller in the Kubernetes Cluster. Follow the readme in the ['deployment'](./deployment) folder. 

## **Example**
An example for quick hands on with Citrix Ingress Controller  can be found at [example](./example). 

## **Questions**
For questions and support please use https://discussions.citrix.com/forum/1657-netscaler-cpx/ forum. 

## **Version**
Citrix Ingress Controller version can be found by using "version" command from the Citrix Ingress Controller shell.
```
  root@ubuntu194:~# kubectl exec -it citrix-k8s-ingress-controller  bash

  root@citrix-k8s-ingress-controller:/# version
  1.0.0
```
## **Issues**
Use the forum mentioned below
```
   https://discussions.citrix.com/forum/1657-netscaler-cpx/
```
Describe the Issue in Details 
Collects the logs via following command
```
  kubectl logs citrix-k8s-ingress-controller > log_file
```
Get version of Citrix Ingress Controller
```
  root@citrix-k8s-ingress-controller:/# version
  1.0.0
```

## **Code of Conduct**
This project adheres to the [Kubernetes Community Code of Conduct](https://github.com/kubernetes/community/blob/master/code-of-conduct.md). By participating in this project you agree to abide by its terms.

## **License**
[Apache License 2.0](./license/LICENSE)
