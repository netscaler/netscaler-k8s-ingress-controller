# Description

Citrix Ingress Controller helps expose Kubernetes Ingress resource on NetScaler (VPX/MPX/CPX) 

CIC is a daemon that monitors ingress resources and configures the NetScaler automatically. It run as a pod in Kubernetes.


## Deployment 
Use the YAML in this section to deploy Citrix Ingress Controller in the Kubernetes Cluster. Follow the readme in the ['deployment'](./deployment) folder. 

## Example
An example for quick hands on with CIC can be found at [Example](./example). 

## Documentation
Detailed documentation can be found at [Doc](./docs/deploy-cic.md).

## Questions
For questions and support please use `https://discussions.citrix.com/forum/1657-netscaler-cpx/` forum. 

## Version
CIC version can be found by using "version" command from the CIC shell.
```
  root@ubuntu194:~# kubectl exec -it cic-k8s-ingress-controller  bash

  root@cic-k8s-ingress-controller:/# version
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
  kubectl logs cic-k8s-ingress-controller > log_file
```
Get version of CIC
```
  root@cic-k8s-ingress-controller:/# version
  1.0.0
```

## Code of Conduct
This project adheres to the [Kubernetes Community Code of Conduct](https://github.com/kubernetes/community/blob/master/code-of-conduct.md). By participating in this project you agree to abide by its terms.

## License
[Apache License 2.0](./license/LICENSE)
