# Dual Tiered Ingress Deployment

In a Dual Tiered Ingress deployment Citrix ADC VPX/MPX is deployed outside the Kubernetes cluster (Tier-1) and Citrix ADC CPX(s) are deployed inside the Kubernetes cluster (Tier-2).<br>
The Tier-1 VPX/MPX would load-balance the Tier-2 CPX inside the Kubernetes cluster.

This is a generic deployment model followed widely irrespective of the platform. Be it Google Cloud or AWS or Azure or On-premises deployment, Dual tiered Ingress deployment is mostly followed.

### Automation of the Tier-1 VPX/MPX:
Typically, the Tier-1 VPX/MPX is automated to load-balance the Tier-2 CPX(s). This is done by the [Citrix Ingress Controller (CIC)](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal#install-citrix-ingress-controller-on-kubernetes) running as a pod inside the Kubernetes cluster.

A seperate [Ingress class](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/ingress-classes.md) is configured for Tier-1 VPX/MPX so that the configuration does not overlap with other Ingress resources.


## Topology:

<img
src="https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/dual-tier/images/Generic-Dual-Tiered-Ingress-Topology.png"
width="750">

### Pre-requisites for deploying Tier-1 VPX/MPX:

* An UP and running Kubernetes cluster
* In cloud deployments, VPX usually would be deployed in a multiple subnet mode with separate subnets for management, client (public) and server (private). VPX/MPX should be deployed in such a way that it has one subnet/vpc configured to receive external client traffic through a VIP and another subnet as the same subnet/vpc where the Kubernetes cluster is deployed (usually the server subnet is where the Kubernetes cluster would be deployed). This communication to the Kubernetes cluster is through a SNIP configured in the VPX.
* After deploying a VPX/MPX, make sure you configure a SNIP in the Citrix ADC as the same subnet of the Kubernetes cluster.
* In this case, enable management access for the SNIP which is in the same subnet of the Kubernetes cluster. This SNIP would be used as ```NS_IP``` variable in the [CIC yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/dual-tier/manifest/tier-1-vpx-cic.yaml) file to enable Citrix Ingress controller to configure the Tier-1 VPX.
* Enable Mac based Forwarding mode in the Tier-1 VPX. Since VPX is deployed in multiple subnet mode, it would not have return route to reach the POD CNI network or the Client network. Enabling MBF mode in the Tier-1 VPX would resolve this.
* For Citrix Ingres Controller to automate the configuration of the VPX/MPX, it requires access to the VPX/MPX through a Citrix ADC system user. Please read through the [installation guide](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal#install-citrix-ingress-controller-on-kubernetes) for more details.
* Firewall rules/Security groups (usually 80, 443,etc ports) should be allowed for the required ports for the VPX/MPX

### Reaching the Kubernetes CNI network from VPX/MPX:

Since the VPX/MPX deployed in Tier-1 is going to load-balance the CPX(s) inside the Kubernetes cluster, a SNIP should be configured in the Tier-1 VPX/MPX. This SNIP should be of the same subnet/vpc of the Kubernetes cluster. 

When this pre-requisite is met, [Citrix Ingress Controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal#install-citrix-ingress-controller-on-kubernetes) can automate the static route configuration in the VPX/MPX, so that Tier-1 Citrix ADC can reach the pods inside the Kubernetes cluster

Please read our [detailed guide](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal#install-citrix-ingress-controller-on-kubernetes) for more information on the pod reachability from Tier-1 VPX/MPX.

## Deployment Steps:

### Create a Kubernetes cluster:
Create a Kubernetes cluster in cloud or on-premises.<br> The Kubernetes cluster in cloud could be a managed Kubernetes (like GKE, EKS or AKS) or a custom created Kubernetes.

### Deploy a VPX/MPX:
Deploy the VPX/MPX in a multiple subnet mode outside the Kubernetes cluster.<br>
Configure a SNIP in the same subnet of the Kubernetes cluster.<br>
Enable [MBF mode](https://docs.citrix.com/en-us/netscaler/12/networking/interfaces/configuring-mac-based-forwarding.html) in the VPX.<br>
Refer the pre-requisites section.

#### Deployment guides of VPX in Clouds:

Please deploy the VPX in the cloud of your choice by using the below deployment guides.

* [AWS](https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-aws/launch-vpx-for-aws-ami.html)
* [Azure](https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-vpx-on-azure.html)
* [GCP](https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-vpx-google-cloud.html)


### Deploy a sample microservice

Let us deploy a sample microservice inside the Kubernetes cluster using Citrix ADC CPX (Tier-2) as an Ingress device. We would then extend this CPX to be load-balance using a Tier-1 VPX which is automated by the Citrix Ingress Controller.

**Create a sample application and expose it as service.**<br>
In our demo, we would use a simple apache pod as a microservice.

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/apache.yaml
```

**Create a Citrix CPX as Tier-2 Ingress**<br>

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/tier-2-cpx.yaml
```

**Create an ingress object for Tier-2 CPX**<br>

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/ingress-tier-2-cpx.yaml
```

**Create a Citrix Ingress Controller for Tier-1 VPX**<br>

Download the manifest file and update the Citrix ADC IP, Credentials , Citrix ADC VIP IP and other required details.

```
wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/tier-1-vpx-cic.yaml
```

After updating the details, apply the manifest to Kubernetes

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/tier-1-vpx-cic.yaml
```

**Create an Ingress object for Tier-1 VPX**<br>

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/ingress-tier-1-vpx.yaml
```

**DNS changes**<br>
You can now update your DNS servers in cloud/on-premises to point your website to the VIP of the Tier-1 VPX.

For example,
```citrix-ingress.com 10.250.9.1```<br>
where ```10.250.9.1``` is the VIP of the Tier-1 VPX and ```citrix-ingress.com``` is the microservice inside the Kubernetes cluster

**Deployment Complete!** You can now try accessing the URL of the Microservice and it should be up and running.

### One step deployment 
For easing the deployment, we have an all-in-one deployment manifest. Just download the manifest and update the required details like NS_IP, NS_VIP, etc and apply to Kubernetes and you are done!


```
wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/all-in-one-dual-tier-demo.yaml
```

Apply to Kubernetes after updating details in the manifest

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/all-in-one-dual-tier-demo.yaml
```
