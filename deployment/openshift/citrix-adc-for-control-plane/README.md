# Citrix ADC as a load balancer for the OpenShift control plane

You can use Citrix ADC for load balancing the OpenShift control plane (master nodes). Citrix provides a solution to automate the configuration of the Citrix ADC using [Terraform](https://www.terraform.io/) instead of manually configuring the Citrix ADC.

## Configuring Citrix ADC for the OpenShift control plane using Terraform

**Prerequisites**

You must perform the following prerequisites:

- Install Terraform.

    If you are using macOS, then use the following command to install terraform on your Mac:

        brew install terraform
    
    For installing Terraform on other operating systems, see the [official Terraform installation guide](https://learn.hashicorp.com/terraform/getting-started/install.html).

- Download and install Citrix ADC Terraform provider plug-in from the [Citrix ADC Terraform Provider Official Repo](https://github.com/citrix/terraform-provider-citrixadc).

    You can download a release from the [releases page](https://github.com/citrix/terraform-provider-citrixadc/releases) and untar the binary into `~/.terraform.d/plugins/`.

### Perform the following steps for configuring Citrix ADC for the OpenShift control plane using Terraform.

1. Clone the `citrix-k8s-ingress-controller` repository from GitHub using the following command.

       git clone https://github.com/citrix/citrix-k8s-ingress-controller.git
    
1. After cloning, change your directory using the following command.


        cd citrix-k8s-ingress-controller/deployment/openshift/citrix-adc-for-control-plane/


2. Initialize Terraform by using the following step.

        terraform init

3. Create a Terraform execution plan using the following step.


        terraform plan -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]'

   **Note:** The values used in this step are only for the demonstration purpose. You can replace them according to your OpenShift set up.

   The description for the variables used in this example is provided as follows.


   | Variable | Description |
   |-------------------------------------|--------------------------------|
   | `citrix_adc_ip`  | Management IP address of the Citrix ADC |
   | `citrix_adc_username` | User name of the Citrix ADC |
   | `citrix_adc_password` | Password of the Citrix ADC |
   | `lb_ip_address`      | VIP for the Citrix ADC - provided in    the installer configuration file |
   | `api_backend_addresses` | Kubernetes control plane node IP addresses|
   | `ingress_backend_addresses` | Kubernetes compute node IP addresses |

4. Apply the changes using the `terraform apply` command.


        terraform apply -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]' -auto-approve

## Unconfiguring Citrix ADC (Optional)

If the Citrix ADC configuration needs to be removed for some reason, you can use the `terraform destroy` command.


        terraform destroy -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]' -auto-approve
