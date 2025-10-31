# AWS CloudFormation template for Netscaler VPX

Citrix provides an [AWS CloudFormation Template](https://aws.amazon.com/cloudformation/aws-cloudformation-templates/) for Netscaler VPX. The CloudFormation template deploys a Netscaler VPX with one [Elastic Network Interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) (ENI). You can modify the CloudFormation template based on your production or testing requirements.

The [CloudFormation template](/deployment/aws/templates/eks_single_nic/eks.1nic.template) provisions the [NSIP](https://docs.citrix.com/en-us/netscaler/12/networking/ip-addressing/configuring-netscaler-owned-ip-addresses/configuring-netscaler-ip-address.html), [VIP](https://docs.citrix.com/en-us/netscaler/12/networking/ip-addressing/configuring-netscaler-owned-ip-addresses/configuring-and-managing-virtual-ip-addresses-vips.html), and [SNIP](https://docs.citrix.com/en-us/netscaler/12/networking/ip-addressing/configuring-netscaler-owned-ip-addresses/configuring-subnet-ip-addresses-snips.html) for the Netscaler VPX instance. The primary IP address of the Netscaler VPX EC2 instance is assigned as VIP so that multiple instances of Netscaler VPX can be deployed and load balanced using AWS ELB. The template also creates and attaches a security group to the ENI of the associated Netscaler VPX to allow all TCP traffic on port `22`, `80`, and `443`. You can modify these port numbers based on your requirement.

>**Important:**
> The CloudFormation template includes AMI IDs of customer licensed BYOL (Bring your own License) variant and Netscaler VPX 12.1 version. For more information see, [Netscaler VPX - Customer Licensed](https://aws.amazon.com/marketplace/pp/B00AA01BOE?ref_=aws-mp-console-subscription-detail).
> If you want to use a different version of Netscaler VPX with the CloudFormation template, you need template and replace the AMI Ids.

## Prerequisites

Ensure that you have:

-  Provided sufficient permission to the CloudFormation template for creating IAM roles. The permissions should be beyond normal EC2 full privileges.
-  Accepted the terms of AWS Marketplace products and subscribed to them.
-  Connected VPC to the internet gateway.
-  Configured one public subnet.

## Parameters in the CloudFormation template

To use the CloudFormation template, you need to edit the template and provide values for the following parameters:

| Parameter | Description |
| --------- | ----------- |
| `VpcID`     | The ID of the Virtual Private Cloud (VPC) where you want to deploy Netscaler VPX. |
| `SubnetID`  | The ID of the subnet in which you want to deploy Netscaler VPX. |
| `VPXInstanceType` | The instance type to you want to use for the Netscaler VPX instance. |
| `VPXTenancyType` | The tenancy type. It can be either Dedicated or Shared. |
| `KeyName` | The **SSH** key name to access the Netscaler VPX instance using SSH. |

## How the CloudFormation template works?

When the CloudFormation template is used, it provisions a lambda function that initializes the Netscaler VPX instance with NSIP, VIP, and SNIP. The lambda function performs an initial configuration on the Netscaler VPX. The configurations include network interface, VIP, and features. You can further configure the Netscaler VPX instance either logging in to Netscaler VPX GUI or using SSH (the user name is `nsroot` and the password is same as `InstanceIdNS`).

The output of the CloudFormation template includes:

| Output | Description |
| ------ | ----------- |
| `InstanceIdNS` | Instance ID of the created Netscaler VPX instance. The instance ID is the default password to access the Netscaler VPX GUI or command-line |
| `ManagementURL` | The HTTPS url to access the Netscaler VPX GUI. Use this URL to log on to the Netscaler VPX GUI using self-signed certificates. |
| `ManagementURL2` | The HTTP url to access the Netscaler VPX GUI. Use this URL to log on to the Netscaler VPX GUI if your browser has any problems with self-signed certificates. |
| `PublicNSIp` | The public IP address to access the Netscaler VPX instance using SSH. |
| `PublicIpVIP` | The public IP address to access the load balanced applications. |
| `PrivateNSIP` | The private IP address used to manage Netscaler VPX. The IP address is mapped to public elastic IP address: `PublicNSIp`. |
| `PrivateVIP` | The private IP address that is used as virtual IP address for hosting the application. The IP address is mapped to public elastic IP address: `PublicIpVIP`. |
| `SNIP` |The private IP address used for back-end communication between EKS pods. |
| `SecurityGroup` | The security group associated with the Netscaler VPX ENI. |

## Related documentation

-  [Deploying Netscaler VPX in AWS](https://docs.citrix.com/en-us/citrix-adc/12-1/deploying-vpx/deploy-aws.html).
-  [Netscaler 12.1 Documentation](https://docs.citrix.com/en-us/citrix-adc/12-1.html).
-  [Netscaler Overview](https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html).