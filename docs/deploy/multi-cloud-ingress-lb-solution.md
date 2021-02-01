# Multi-cloud and multi-cluster ingress and load balancing solution with Amazon EKS and Microsoft AKS clusters

You can deploy multiple instances of the same application across multiple clouds provided by different cloud providers. This multi-cloud strategy helps you to ensure resiliency, high availability, and proximity. A multi-cloud approach also allows you to take advantage of the best of each cloud provider by reducing the risks such as vendor lock-in and cloud outages.

Citrix ADC with the help of Citrix ingress controller can perform multi-cloud load balancing. Citrix ADC can direct traffic to clusters hosted on different cloud provider sites. The solution performs load balancing by distributing the traffic intelligently between the workloads running in Amazon EKS (Elastic Kubernetes Service) and Microsoft AKS (Azure Kubernetes Service).

You can deploy the multi-cloud and multi-cluster ingress and load balancing solution with Amazon EKS and Microsoft AKS.

## Deployment topology

The following diagram explains a deployment topology of the multi-cloud ingress and load balancing solution for Kubernetes service provided by Amazon EKS and Microsoft AKS.

 ![Deployment topology](../media/multi-cloud-ingress-architecture.png)

**Prerequisites**

  -  You should be familiar with AWS and Azure.
  -  You should be familiar with Citrix ADC and [Citrix ADC networking](https://docs.citrix.com/en-us/citrix-adc/current-release/networking.html).
  -  Instances of the same application must be deployed in Kubernetes clusters on Amazon EKS and Microsoft AKS.

To deploy the multi-cloud multi-cluster ingress and load balancing solution, you must perform the following tasks.

1.	Deploy Citrix ADC VPX in AWS
1.	Deploy Citrix ADC VPX in Azure
1.	Configure ADNS service on Citrix ADC VPX deployed in AWS and AKS
1.	Configure GSLB service on Citrix ADC VPX deployed in AWS and AKS
1.  Apply GTP and GSE CRDs on AWS and Azure Kubernetes clusters
1.	Deploy multi-cluster controller

## 	Deploying Citrix ADC VPX in AWS

You must ensure that the Citrix ADC VPX instances are installed in the same VPC on the EKS cluster. It enables Citrix ADC VPX to communicate with EKS workloads. You can use an existing EKS subnet or create a subnet to install the Citrix ADC VPX instances.

Also, you can install the Citrix ADC VPX instances in a different VPC, but you must ensure that the VPC for EKS can communicate using VPC peering. For more information about VPC peering, see [VPC peering documentation](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html). 

For high availability, you can install two instances of Citrix ADC VPX in HA mode.

1. Install Citrix ADC VPX in AWS. For information on installing Citrix ADC VPX in AWS, see [Deploy Citrix ADC VPX instance on AWS](https://docs.citrix.com/en-us/citrix-adc/current-release/deploying-vpx/deploy-awshtml#deploy-a-citrix-adc-vpx-instance-on-aws).

    Citrix ADC VPX requires a secondary public IP address other than the NSIP to run GSLB service sync and ADNS service.   

1. Open the AWS console and choose **EC2** > **Network Interfaces** > **VPX primary ENI ID** > **Manage IP addresses**. Click **Assign new IP Address**.

   ![](../media/multi-cloud-manage-ipaddress.png)

    After the secondary public IP address has been assigned to the VPX ENI, associate an elastic IP address to it. 

1. Choose **EC2** > **Network Interfaces** > **VPX ENI ID** - **Actions** , click **Associate IP Address**. Select an elastic IP address for the secondary IP address and click **Associate**.

   ![](../media/multi-cloud-associate-elasticip.png)

1. Log in to the Citrix ADC VPX instance and add the secondary IP address as SNIP and enable the management using the following command:

        add ip 192.168.211.73 255.255.224.0 -mgmtAccess ENABLED -type SNIP

    **Note**:  To log in to Citrix ADC VPX using SSH, you must allow the SSH port in the Security group. Route tables must have an internet gateway configured for the default traffic and the NACL must allow the SSH port.

    **Note**: If you are running the Citrix ADC VPX in HA (High Availability) mode, you must perform the preceding configuration in both of the Citrix ADC VPX instances.

1. Enable the features: CS (Content Switching), LB (Load Balancing), GSLB (Global Server Load Balancing), and SSL in Citrix ADC VPX using the following command:

        enable feature *feature*

    **Note**: To enable GSLB, you must have an additional license.

1. Enable port 53 UDP and TCP ports in the VPX security group for VPX to receive DNS traffic. Also enable TCP: 22 for SSH and TCP: 3008–3011 for GSLB metric exchange. 

    For information on adding rules to the security group, see [Adding rules to a security group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#adding-security-group-rule).

1.	Add a nameserver to Citrix ADC VPX using the following command:

        add nameserver *nameserver IP*

##	Deploying Citrix ADC VPX in Azure

You can run a standalone Citrix ADC VPX instance on an AKS cluster or run two Citrix ADC VPX instances in High Availability mode on the AKS cluster. 

While installing, ensure that the AKS cluster must have connectivity with the VPX instances. To ensure that, you can install the Citrix ADC VPX in the same VNet on the AKS cluster in a different resource group.

While installing the Citrix ADC VPX, select the VNet where the AKS cluster is installed. Alternatively, you can use VNet peering to ensure the connectivity between AKS and Citrix ADC VPX if the VPX is deployed in a different VNet other than the AKS cluster.

1. Install Citrix ADC VPX in AWS. For information on installing Citrix ADC VPX in AKS, see [Deploy a Citrix ADC VPX instance on Microsoft Azure](https://docs.citrix.com/en-us/citrix-adc/current-release/deploying-vpx/deploy-vpx-on-azure.html).

    You must have a SNIP with public IP for GSLB sync and ADNS service. If SNIP is already exist, associate a public IP with it. 
    
1. To associate, choose **Home** > **Resource group** > **VPX instance** > **VPX NIC instance**. Associate a public IP as shown in the following image. Click **Save** to save the changes.

   ![](../media/multi-cloud-snip.png)

1. Log in to the Azure Citrix ADC VPX instance and add the secondary IP as SNIP with the management access enabled using the following command:

        add ip 10.240.0.11 255.255.0.0 -type SNIP -mgmtAccess ENABLED

    If the resource exists, you can use the following command to set the management access enabled on the existing resource. 

        set ip 10.240.0.11 -mgmtAccess ENABLED

1. Enable the CS, LB, SSL, and GSLB features in the Citrix ADC VPX using the following command:

        enable feature *feature*

    To access the Citrix ADC VPX instance through SSH, you must enable the inbound port rule for SSH port in the Azure network security group that is attached to the Citrix ADC VPX primary interface. 

1. Enable the inbound rule for the following ports in the network security group on the Azure portal.

    - TCP: 3008–3011 for GSLB metric exchange
    - TCP: 22 for SSH
    - TCP and UDP: 53 for DNS

1. Add a nameserver to Citrix ADC VPX using the following command:

        add nameserver *nameserver IP*

##	Configure ADNS service in Citrix ADC VPX deployed in AWS and Azure

  ADNS service in Citrix ADC VPX acts as an authoritative DNS for your domain. For more information on ADNS service, see [Authoritative DNS service](https://docs.citrix.com/en-us/citrix-adc/current-release/global-server-load-balancing/configure/configure-gslb-adns-service.html).

1. Log in to AWS Citrix ADC VPX and configure the ADNS service on secondary IP and port 53 using the following command:

        add service Service-ADNS-1 192.168.211.73 ADNS 53

    Verify the configuration using the following command:

        show service Service-ADNS-1

1.	Log in to Azure Citrix ADC VPX and configure the ADNS service on secondary IP and port 53 using the following command:

        add service Service-ADNS-1 10.240.0.8 ADNS 53

    Verify the configuration using the following command:

        show service Service-ADNS-1  

1.	After creating two ADNS service for the domain, update the NS record of the domain to point to the ADNS services in the domain registrar. 

    For example, create an 'A' record ns1.domain.com pointing to the ADNS service public IP. NS record for the domain must point to ns1.domain.com.


##	Configure GSLB service in Citrix ADC VPX deployed in AWS and Azure

You must create GSLB sites on Citrix ADC VPX deployed on AWS and Azure.

1.	Log in to AWS Citrix ADC VPX and configure GSLB sites on secondary IP using the following command. Also, specify the public IP using the *–publicIP* argument. For example:

        add gslb site aws_site 192.168.197.18 -publicIP 3.139.156.175

        add gslb site azure_site 10.240.0.11 -publicIP 23.100.28.121

2.	Log in to Azure Citrix ADC VPX and configure GSLB sites. For example:

        add gslb site aws_site 192.168.197.18 -publicIP 3.139.156.175

        add gslb site azure_site 10.240.0.11 -publicIP 23.100.28.121

3.	Verify that the GSLB sync is successful by initiating a sync from any of the sites using the following command:

        sync gslb config –debug

**Note**: If initial sync fails, review the security groups on both AWS and Azure to allow the required ports.

##  Apply GTP and GSE CRDs on AWS and Azure Kubernetes clusters

The Global traffic policy (GTP) and Global service entry (GSE) CRDs help to configure Citrix ADC for performing GSLB in Kubernetes applications. These CRDs are designed for configuring multi-cluster ingress and load balancing solution for Kubernetes clusters.

**GTP CRD**

The GTP CRD accepts the parameters for configuring GSLB on the Citrix ADC including deployment type (canary, failover, and local-first), GSLB domain, health monitor for the ingress, and service type.

For GTP CRD definition, see [GTP CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/multicluster/multi-cluster/#gtp-crd-definition). Apply the GTP CRD definition on AWS and Azure Kubernetes clusters using the following command:

    kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/multicluster/Manifest/gtp-crd.yaml

**GSE CRD**

The GSE CRD dictates the endpoint information (information about any Kubernetes object that routes traffic into the cluster) in each cluster. GSE automatically picks the application’s external IP, which routes traffic into the cluster. If the external IP of the routes change, Global Service Entry picks a newly assigned IP address and configure the Citrix ADC’s multi-cluster endpoints accordingly.

For the GSE CRD definition, see [GSE CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/multicluster/multi-cluster/#gse-crd-definition). Apply the GSE CRD definition on AWS and Azure Kubernetes clusters using the following command:

    kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/multicluster/Manifest/gse-crd.yaml
 
##	Deploy multi-cluster controller

Multi-cluster controller helps you to ensure high availability of the applications across the clusters in a multi-cloud environment.

You can install the multi-cluster controller on the AWS and Azure clusters. Multi-cluster controller listens to GTP and GSE CRDs and configures the Citrix ADC for GSLB that provides high availability across multiple regions in a multi-cloud environment.

To deploy the multi-cluster controller, perform the following steps:

1. Create an RBAC for the multi-cluster ingress controller on the AWS and Azure Kubernetes clusters.

        kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/multicluster/Manifest/gslb-rbac.yaml

2. Create the secrets on the AWS and Azure clusters using the following command: 

    **Note**: Secrets enable the GSLB controller to connect and push the configuration to the GSLB devices.

        kubectl create secret generic secret-1 --from-literal=username=<username> --from-literal=password=<password>

    **Note**: You can add a user to Citrix ADC using the `add system user` command.


3.	Download the GSLB controller YAML file from [gslb-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/multicluster/Manifest/gslb-controller.yaml).

4. Apply the `gslb-controller.yaml` in an AWS cluster using the following command:

        kubectl apply -f  gslb-controller.yaml

    For the AWS environment, edit the `gslb-controller.yaml` to define the LOCAL_REGION, LOCAL_CLUSTER, and SITENAMES environment variables. 

    The following example defines the environment variable `LOCAL_REGION` as *us-east-2* and `LOCAL_CLUSTER` as *eks-cluster* and the  `SITENAMES` environment variable as *aws_site,azure_site*.

        name: "LOCAL_REGION"
        value: "us-east-2"
        name: "LOCAL_CLUSTER"
        value: "eks-cluster"
        name: "SITENAMES"
        value: "aws_site,azure_site"
        name: "aws_site_ip"
        value: "NSIP of aws VPX(internal IP)"
        name: "aws_site_region"
        value: "us-east-2"
        name: "azure_site_ip"
        value: "NSIP of azure_VPX(public IP)"
        name: "azure_site_region"
        value: "central-india"
        name: "azure_site_username"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: username
        name: "azure_site_password"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: password
        name: "aws_site_username"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: username
        name: "aws_site_password"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: password

    Apply the [gslb-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/multicluster/Manifest/gslb-controller.yaml) in the Azure cluster using the following command:

        kubectl apply -f  gslb-controller.yaml

1.  For the Azure site, edit the `gslb-controller.yaml` to define `LOCAL_REGION`, `LOCAL_CLUSTER`, and `SITENAMES` environment variables.

    The following example defines the environment variable `LOCAL_REGION` as *central-india*, `LOCAL_CLUSTER` as *azure-cluster*, and  `SITENAMES` as *aws_site, azure_site*.

        name: "LOCAL_REGION"
        value: "central-india"
        name: "LOCAL_CLUSTER"
        value: "aks-cluster"
        name: "SITENAMES"
        value: "aws_site,azure_site"
        name: "aws_site_ip"
        value: "NSIP of AWS VPX(public IP)"
        name: "aws_site_region"
        value: "us-east-2"
        name: "azure_site_ip"
        value: "NSIP of azure VPX(internal IP)"
        name: "azure_site_region"
        value: "central-india"
        name: "azure_site_username"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: username
        name: "azure_site_password"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: password
        name: "aws_site_username"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: username
        name: "aws_site_password"
        valueFrom:
          secretKeyRef:
           name: secret-1
           key: password

    **Note**: The order of the GSLB site information should be the same in all clusters. The first site in the order is considered as the master site for pushing the configuration. Whenever the master site goes down, the next site in the list becomes the new master. Hence, the order of the sites should be same in all Kubernetes clusters.

### Deploy a sample application

In this example application deployment scenario, an https image is used. However, you can choose a sample application of your choice.

The application is exposed as type LoadBalancer in both AWS and Azure clusters. You must run the commands in both AWS and Azure Kubernetes clusters.

1.	Create a deployment of sample application ‘apache’ using the following command:

        kubectl create deploy apache --image=httpd:latest port=80

1. Expose the apache application as service of type LoadBalancer using the following command:

        kubectl expose deploy apache --type=LoadBalancer --port=80

1. Verify that an external IP is allocated for the service of type LoadBalancer using the following command:

        kubectl get svc apache
        NAME     TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
        apache   LoadBalancer   10.0.16.231   20.62.235.193   80:32666/TCP   3m2s

After deploying the application on AWS and Azure clusters, you must configure GTE custom resource to configure high availability in the multi-cloud clusters. 

Create a GTP YAML resource `gtp_isntance.yaml` as shown in the following example.

```
apiVersion: "citrix.com/v1beta1"
 kind: globaltrafficpolicy
 metadata:
   name: gtp-sample-app
   namespace: default
 spec:
   serviceType: 'HTTP'
   hosts:
   - host: <domain name>
     policy:
       trafficPolicy: 'FAILOVER'
       secLbMethod: 'ROUNDROBIN'
       targets:
       - destination: 'apache.default.us-east-2.eks-cluster'
         weight: 1
       - destination: 'apache.default.central-india.aks-cluster'
         primary: false
         weight: 1
       monitor:
       - monType: http
         uri: ''
         respCode: 200
   status:
     {}
```

In this example, traffic policy is presented as `FAILOVER`. However, the multi-cluster controller supports multiple traffic policies. For more information, see the documentation for the traffic policies. 

Apply the GTP resource in both the clusters using the following command: 

    kubectl apply -f gtp_instance.yaml

You can verify that the GSE resource is automatically created in both of the clusters with the required endpoint information derived from the service status. Verify using the following command: 

    kubectl get gse 
    kubectl get gse *name* -o yaml

Also, log in to Citrix ADC VPX and verify that the GSLB configuration is successfully created using the following command:

    show gslb runningconfig

As the GTP CRD is configured for traffic policy as `failover`, Citrix ADC VPX instances serve the traffic from the primary cluster, in this scenario the application deployed in the EKS cluster.

    curl -v http://*domain_name* 

 However, when there is no endpoint available in the EKS cluster, applications are automatically served from the Azure cluster. You can make sure this by setting the replica count to `0` in the primary cluster.
