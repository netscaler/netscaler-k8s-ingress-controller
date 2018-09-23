# Description

Citrix Ingress Controller helps expose Kubernetes Ingress resource on Netscaler (VPX/MPX/CPX) 

Citrix Ingress Controller is a daemon that monitors ingress resources and configures the NetScaler automatically. It run as a pod in Kubernetes.


## Deployment 
Use the YAML in this section to deploy Citrix Ingress Controller in the Kubernetes Cluster. Follow the readme in the ['deployment'](./deployment) folder. 

## Example
An example for quick hands on with Citrix Ingress Controller  can be found at [example](./example). 

## Questions
For questions and support please use https://discussions.citrix.com/forum/1657-netscaler-cpx/ forum. 

## Version
Citrix Ingress Controller version can be found by using "version" command from the Citrix Ingress Controller shell.
```
  root@ubuntu194:~# kubectl exec -it citrix-k8s-ingress-controller  bash

  root@citrix-k8s-ingress-controller:/# version
  1.0.0
```
## Issues
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

## Code of Conduct
This project adheres to the [Kubernetes Community Code of Conduct](https://github.com/kubernetes/community/blob/master/code-of-conduct.md). By participating in this project you agree to abide by its terms.

## License
[Apache License 2.0](./LICENSE)
