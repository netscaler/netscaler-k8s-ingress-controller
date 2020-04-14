# Get Citrix ADC VPX on Azure Marketplace

This guide explains the steps to create Citrix ADC VPX on Azure Markerplace.

#### Prerequisites:

- Valid Azure Marketplace account and Subscription
- An existing Kubernetes cluster in Azure.


## Steps:

1. Login to your Azure Marketplace Account.See, [Azure Market Place](https://azuremarketplace.microsoft.com/en-us)

2. Locate the automatically created resource group as a part of creating the kuberentes cluster to be used with VPX. 
   - If the kubernetes cluster 'X' is a part of a resource group 'Y' in region 'Z' then look for a resource group starting          with "MC" followed ty "X_Y_Z" i.e with the format "MC_X_Y_Z"
   - For instance, if,
       - cluster name is "cic-cluster-basic-1", 
       - resource group for the cluster is "AKS_RG", 
       - region used for cluster is 'southindia'
       
     Then a resouce group would have been automatically created as "MC_AKS_RG_cic-cluster-basic-1_southindia"
     <img src="../../deployment/azure/images/image_vpx_1.png" width="500">
     
3. Add VPX in the located resouce group in step 2.
   - From the resouce group page and click on "+Add"
   - Search for "Citrix ADC 12.1", select a software plan and click on "Create"
     <img src="../../deployment/azure/images/image_vpx_2.png" width="500">

4. Fill in the detais for the VPX
   - Specify a "virtual machine name"
   - Specify a "Region" which should be same as that of the cluster
     <img src="../../deployment/azure/images/image_vpx_3.png" width="500">
   - Specify a "Size" for the VPX
   
     <img src="../../deployment/azure/images/image_vpx_4.png" width="500">
   - You can select 'Password' as "Authentication Type"
   - Specify 'Username' and 'Password'
   - Do select all the relavant 'inbound ports' from Dropdown, then click "Next"
     <img src="../../deployment/azure/images/image_vpx_5.png" width="500">
   - Verify Disk details and click "Next"
   
     <img src="../../deployment/azure/images/image_vpx_6.png" width="500">
   - Verify "Virtual network" and "Subnet", these should be same as that of the resource group. Click "Next"
     <img src="../../deployment/azure/images/image_vpx_7.png" width="500">
   - Verify Management details and click "Next"
   
     <img src="../../deployment/azure/images/image_vpx_8.png" width="500">
   - Verify any Advanced details if required. click "Next"
     <img src="../../deployment/azure/images/image_vpx_9.png" width="500">
   - Specify any Tags if needed, click "Next"
   
     <img src="../../deployment/azure/images/image_vpx_10.png" width="500">
   - Finally review all the details of the VPX and click "Create"
     <img src="../../deployment/azure/images/image_vpx_11.png" width="500">
   - Wait for some time till the deployment is complete.
     
5. Set VPX networking Configurations required for usage in cluster as part of ingress/CIC deployment
  - Go to 'Networking' section on deployed VPX Page and select the 'Network Interface' on the right
    <img src="../../deployment/azure/images/image_vpx_12.png" width="500">
  -  Select 'IP configurations' on the network interface page and click on '+Add' for adding new IP.
    <img src="../../deployment/azure/images/image_vpx_13.png" width="500">
  -  Add a 'SNIP'. Specify a 'Name'. Keep 'Allocation' as Dynamic and 'Public IP' as 'Disabled'
    <img src="../../deployment/azure/images/image_vpx_14.png" width="500">
  -  Add a 'VIP'. Specify a 'Name'. Keep 'Allocation' as Dynamic. Keep 'Public IP' as 'Enabled' then set a 'Name' for same          under required settings
  
     <img src="../../deployment/azure/images/image_vpx_15.png" width="500">
     <img src="../../deployment/azure/images/image_vpx_16.png" width="500">
    
  -  Verify all the IP configurations done and then set 'IP forwarding' as Enabled.
    <img src="../../deployment/azure/images/image_vpx_17.png" width="500">
    
6. Verify if you are able to ssh into VPX using the Primary public IP address, using the username and password set during        VPX creation time
  
 Note : Before proceeding with the deployment testing, please make sure all the necessary firewall settings have been done.           For instance, as part of inbound rules of VPX and network security group for the cluster. Verify SSH access and
        other port 80/443 access.
