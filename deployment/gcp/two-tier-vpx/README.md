# Two tier deployment with VPX load-balancing CPX ingress

This guide describes a two tier ingress deployment in Google cloud, replacing the Google's Load-balancer with Citrix ADC (VPX) which provides much more capabilities and performance.

## Deployment Diagram

<img src="https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/gcp/images/CPX-GCP-2tier-Topology.png" width="500">


## Deployment Approach

To deploy a VPX in Google cloud and do the basic configuration you can choose a manual approach where you deploy the VPX and configure it step by step or an automated approach where a script would do all that for you. We have a simple script that would deploy the VPX in Google cloud and would do the basic configs required for interacting with the pods in the kubernetes cluster. 


- [Step by Step deployment](#step-by-step-deployment)
- [Automated deployment](#automated-deployment)


### Step by Step deployment

We would explain the deployment of Citrix ADC VPX in Google Cloud step by step.


#### Pre-requisites:

- A Kubernetes cluster which is up and running
- Another VPC (apart from default) which would be configured in the VPX to receive traffic from internet
- Firewall rules allowed on GCP for VPC on required ports

#### Steps:

1. [Deploy a VPX in Google cloud in two-arm mode](#deploy-a-vpx-in-google-cloud-in-two-arm-mode)
2. [Find the POD CIDR from all the cluster nodes](#find-the-pod-cidr-from-all-the-cluster-nodes)
3. [Configure VPX with the SNIPs and the Routes to reach the pods in the Cluster](#configure-vpx-with-the-snips-and-the-routes-to-reach-the-pods-in-the-cluster)
4. [Deploy the sample application with CPX and CIC container using the manifest files](#deploy-the-sample-application-with-cpx-and-cic-container-using-the-manifest-files)


#### Deploy a VPX in Google cloud in two-arm mode

Deploy the Citrix ADC VPX using the below gcloud api


```
gcloud compute --project=netscaler-networking-k8 instances create vpx-frontend-ingress \
--zone=asia-southeast1-a --machine-type=n1-standard-4 \
--network-interface subnet=default,private-network-ip=10.148.0.201,address='',aliases=10.148.0.202 \
--network-interface subnet=k8-vpc-subnet,private-network-ip=10.10.0.10,address='',aliases=10.10.0.11 \
--image=nsvpx-kamet-50-4001 --image-project=netscaler-networking-k8 --boot-disk-size=20GB
```

The above gcloud cli creates a Citrix ADC VPX with two interfaces. One interface in the same VPC of kubernetes cluster (default VPC) to reach the kubernetes cluster and another in the VPC k8-vpc which is internet facing.
There are alias IP addresses in each interface. Those IP addresses would be added as SNIP in the Citrix ADC VPX.

**Explanation of the above command:**

```--project=<Specify your google project here>```
```--zone=<Specify the zone where your kubernetes cluster is running>```


Networking related parameters for VPX:
```
--network-interface subnet=<subnet of kubernetes cluster>,private-network-ip=<some free ip from the subnet>,address='',aliases=<some free ip from the alias range of subnet>
```
```
--network-interface subnet=<subnet from another VPC to receive internet traffic>,private-network-ip=<some free ip from the subnet>,address='',aliases=<some free ip from the alias range of subnet>
```

VPX image related:
```--image=<name of VPX image> --image-project=<project where VPX image is placed>```
```--machine-type=<Size of the VPX required>```

After executing the above command successsfully the Citrix ADC should have two interfaces like below:


<img src="https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/gcp/images/VPX-on-GCP-Interfaces.png" width="500">



#### Find the POD CIDR from all the cluster nodes

Describe the cluster using gcloud api and find out the Cluster IPv4 CIDR

```
$ gcloud container --project=netscaler-networking-k8 clusters describe cpx-cluster-1 --zone asia-southeast1-a | grep "clusterIpv4Cidr"

clusterIpv4Cidr: 10.4.0.0/14
```

Now find the IPs of the kubernetes cluster nodes

```
$ kubectl get nodes -o wide
NAME                                           STATUS    ROLES     AGE       VERSION        INTERNAL-IP   EXTERNAL-IP      OS-IMAGE                             KERNEL-VERSION   CONTAINER-RUNTIME
gke-cpx-cluster-1-default-pool-c2a88192-m9t7   Ready     <none>    2d        v1.9.7-gke.6   10.148.0.3    <External IP>   Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-cpx-cluster-1-default-pool-c2a88192-qcj4   Ready     <none>    2d        v1.9.7-gke.6   10.148.0.2    <External IP>   Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-cpx-cluster-1-default-pool-c2a88192-rv5l   Ready     <none>    2h        v1.9.7-gke.6   10.148.0.5    <External IP>   Container-Optimized OS from Google   4.4.111+         docker://17.3.2

```

We need to add static routes in VPX for the destination network **10.4.0.0/14** via **10.148.0.3** or **10.148.0.2** or **10.148.0.5**

#### Configure VPX with the SNIPs and the Routes to reach the pods in the Cluster

Execute the below commands in Citrix ADC VPX

```
clear config -f full
enable ns mode MBF
enable ns mode L3 USNIP
add ns ip 10.148.0.202 255.255.255.0
add ns ip 10.10.0.11 255.255.255.0

add route 10.4.0.0 255.252.0.0 10.148.0.3
add route 10.4.0.0 255.252.0.0 10.148.0.2
add route 10.4.0.0 255.252.0.0 10.148.0.5
```

In the above command since same destination is configured via multiple gateways, Citrix ADC VPX would automatically do a ECMP for the above static routes

#### Deploy the sample application with CPX and CIC container using the manifest files

Execute the below kubectl command to deploy a sample application with CPX ingress.

```
kubectl create -f https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/gcp/two-tier-vpx/manifest/two-tier-deployment-demo.yaml
```

Your deployment should now be UP and Running.

This sample application assumes your website is at citrix-ingress.com

To access your application, just do a curl to the Citrix ADC VPX's internet facing VPC's public IP

```
curl http://<public IP of VPX>/ -H 'Host: citrix-ingress.com'
```




### Automated deployment

Automated deployment is pretty straight forward. Just execute a script and Citrix ADC VPX is up and running in Google Cloud.


#### Pre-requisites for the automated script to run:

- A Kubernetes cluster which is up and running
- Another VPC (apart from default) which would be configured in the VPX to receive traffic from internet
- Firewall rules allowed on GCP for VPC on required ports
- Make sure the client from where the commands are executed satisfies below requirements
	- gcloud sdk is installed and authenticated for client(gcloud auth application-default login)
	- python 2.7+ is installed
	- kubectl command line is installed


#### Steps:

1. [Execute the Script to create a Citrix ADC VPX with necessary arguments](#execute-the-script-to-create-a-citrix-adc-vpx-with-necessary-arguments)
2. [Deploy the sample application with CPX and CIC container using the manifest files](#deploy-the-sample-application-with-cpx-and-cic-container-using-the-manifest-files)

#### Execute the Script to create a Citrix ADC VPX with necessary arguments

Execute the below command to deploy VPX using a script


```
curl -k https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/gcp/two-tier-vpx/scripts/automated_vpx_deployment_gcp.py | \
python - --project=netscaler-networking-k8,--zone=asia-southeast1-a,\
--cluster_name=cpx-cluster-1,--image=nsvpx-kamet-50-4001,--vpx_name=vpx-frontend-ingress,\
--public_subnet=k8-vpc-subnet,--public_ip=10.10.0.10,--public_alias=10.10.0.11,\
--private_subnet=default,--private_ip=10.148.0.201,--private_alias=10.148.0.202
```


#### Deploy the sample application with CPX and CIC container using the manifest files



Execute the below kubectl command to deploy a sample application with CPX ingress.

```
kubectl create -f https://code.citrite.net/projects/NS/repos/citrix-k8s-ingress-controller/raw/deployment/gcp/two-tier-vpx/manifest/two-tier-deployment-demo.yaml
```

Your deployment should now be UP and Running.

This sample application assumes your website is at citrix-ingress.com

To access your application, just do a curl to the Citrix ADC VPX's internet facing VPC's public IP

```
curl http://<public IP of VPX>/ -H 'Host: citrix-ingress.com'
```
