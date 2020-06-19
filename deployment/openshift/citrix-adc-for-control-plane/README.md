# Citrix ADC for OpenShift Control Plane

## Pre-requisites:

1. Terraform

    If you are using MacOS, then `brew install terraform` would install terraform on your Mac

    For any other OS, please refer the [official Terraform installation guide](https://learn.hashicorp.com/terraform/getting-started/install.html)

2. Citrix ADC Terraform provider

    [Citrix ADC Terraform Provider Official Repo](https://github.com/citrix/terraform-provider-citrixadc)

    You can download a release from the [releases page](https://github.com/citrix/terraform-provider-citrixadc/releases) and just untar the binary into `~/.terraform.d/plugins/`
    

## Terraform Init

`terraform init`

## Terraform Plan

```
terraform plan -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]'
```

**Note:** The variable values used above are just for example. Please replace them according to your OpenShift Setup. The explanation for the variables are provided below.

### Explanation of the Variables:

| Variable | Description | 
| :------: | :---------: | 
| `citrix_adc_ip` | Management IP of the Citrix ADC | 
| `citrix_adc_username` | Username of the Citrix ADC | 
| `citrix_adc_password` | Password of the Citrix ADC |
| `lb_ip_address` | VIP for the Citrix ADC - provided in the installer config file |
| `api_backend_addresses` | Kubernetes Control Plane node IPs |
| `ingress_backend_addresses` | Kubernetes Compute node IPs |

 
## Terraform Apply

```
terraform apply -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]' -auto-approve
```

## Terrafor Destroy

```
terraform destroy -var citrix_adc_ip="<citrix-adc-ip>" -var citrix_adc_username="<citrix-adc-username>" -var citrix_adc_password='<citrix-adc-password>' -var lb_ip_address="<vip-of-citrix-adc>" -var 'api_backend_addresses=["1.1.1.1","1.1.1.2","1.1.1.3"]' -var 'ingress_backend_addresses=["2.2.2.1","2.2.2.2","2.2.2.3"]' -auto-approve
```
