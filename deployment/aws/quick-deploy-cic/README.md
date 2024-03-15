# Deploy Citrix Ingress Controller in EKS with Netscaler VPX

This guide details the steps to deploy Citrix Ingress Controller in EKS with Netscaler VPX.

## Pre-requisites:

   * [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
   * [EKSCTL](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)
   * [KUBECTL](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Topology:

![](https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/docs/media/singletopology.png)

## Create a AWS managed Kubernetes cluster (EKS) with Netscaler VPX

To create a AWS managed Kubenetes cluster, we will use EKSCTL.

Please make sure to configure (`aws configure`) the AWS CLI with the Access Key, Secret and Region.

```
eksctl create cluster --name quick-cic-vpx-deploy --region ap-south-1
```

When the cluster creation is done, please note the VPC-ID in which the nodes are deployed using the below command

```
$ eksctl get cluster quick-cic-vpx-deploy -r ap-south-1
NAME			VERSION	STATUS	CREATED			VPC			SUBNETS									SECURITYGROUPS
quick-cic-vpx-deploy	1.12	ACTIVE	2019-08-08T06:09:02Z	vpc-id	subnet-ids	security-group-id
```

## Create a Netscaler VPX instance from AWS Marketplace

Create a Netscaler VPX from the AWS Marketplace. For this guide, we will use the Netscaler VPX Express which does not have any software charges.

Launch the Netscaler Instance from the AWS marketplace according to the snapshot below


![](images/Citrix-ADC-VPX-Express.png)

Assign two secondary IPs when creating the Netscaler VPX

![](images/assign-secondary-ips.png)

**Important points to consider when creating the Netscaler VPX**

   * Create the Netscaler VPX with a single interface (NIC/ENI)
   * Create the Netscaler VPX in the same VPC and subnet as that of the EKS nodes. The VPC ID and the subnet IDs of the EKS nodes can be got from the `eksctl get cluster quick-cic-vpx-deploy -r ap-south-1` command.
   * Assign two secondary IPs (one for SNIP and another for VIP). See above snapshot.
   * Configure the security group of the Netscaler VPX to allow ports 22, 80 and 443.
   * [Disable Source and Destination Check](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html#EIP_Disable_SrcDestCheck) on the ENI of the Netscaler VPX instance
   * Assign an Elastic IP for the Primary IP of the Netscaler VPX. This would be the Management IP of the Netscaler VPX.
   * Assign an Elastic IP to one of the secondary IP of the Netscaler VPX. This would the public facing VIP for data traffic.
   * Make sure you modify the security groups of the EKS nodes to allow traffic from the Netscaler VPX. This can be done by adding an inbound rule of the security groups to the EKS nodes to allow traffic from the security group of the Netscaler VPX.

***The instructions provided above are just for this illustration. Actual deployment may vary according to your requirement***


## Deploy Citrix Ingress Controller


#### Create Netscaler VPX login credentials using Kubernetes secret

```
kubectl create secret  generic nslogin --from-literal=username=<username> --from-literal=password=<instance-id-of-vpx>
```

The Netscaler VPX password is usually the instance-id of the VPX if you have not changed it.


#### Configure SNIP in the Netscaler VPX

SSH to the Netscaler VPX and configure a SNIP, which is the secondary IP of the VPX to which no Elastic IP is assigned

```
add ns ip 192.168.84.93 255.255.224.0
```

This is required for Netscaler to interact with the pods inside the Kubernetes cluster.


#### Update the Netscaler VPX management IP and VIP in the Citrix Ingress controller manifest

```
wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/quick-deploy-cic/manifest/cic.yaml
```

***If you don't have `wget` installed, you can use `fetch` or `curl`***

Update the Netscaler VPX's primary IP in the `cic.yaml` in the below field

```
# Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled) 
- name: "NS_IP"
  value: "X.X.X.X"
```

Update the Netscaler VPX VIP in the `cic.yaml` in the below field. This is the private IP to which you have assigned an EIP.

```
# Set NetScaler VIP for the data traffic
- name: "NS_VIP"
  value: "X.X.X.X"
```

#### Create the Citrix Ingress Controller

Now that we have configure the Citrix Ingress controller with the required values, let's deploy it.

```
kubectl create -f cic.yaml
```

## Create example microservice and Ingress

#### Example Microservice

In this example, we will deploy an Apache microservice.

Please  update the image field with the required Apache image.

```
wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/quick-deploy-cic/manifest/apache.yaml
```

***If you don't have `wget` installed, you can use `fetch` or `curl`***


Create the microservice

```
kubectl create -f apache.yaml
```

#### Ingress

Now let's apply the ingress 

```
kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/quick-deploy-cic/manifest/ingress.yaml
```

## Test your deployment

To validate your deployment, send a curl to the Elastic IP of the VIP of the Netscaler VPX.

```
$ curl --resolve citrix-ingress.com:80:<EIP-of-VIP> http://citrix-ingress.com
<html><body><h1>It works!</h1></body></html>
```

The response received is from example microservice (apache) which is inside the Kubernetes cluster. Netscaler VPX being an ingress has load-balanced the request.

