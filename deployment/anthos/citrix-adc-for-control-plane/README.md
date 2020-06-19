# Citrix ADC as a load balancer for the Anthos control plane

You can use Citrix ADC for load balancing the Anthos control plane. Citrix provides a solution to automate the configuration of the Citrix ADC using [Terraform](https://www.terraform.io/) instead of manually configuring the Citrix ADC.

## Configuring Citrix ADC for the Anthos control plane using Terraform

**Prerequisites**

You must perform the following prerequisites:

- Install Terraform.

    If you are using macOS, then use the following command to install terraform on your Mac:

        brew install terraform

    For installing Terraform on other operating systems, see the [official Terraform installation guide](https://learn.hashicorp.com/terraform/getting-started/install.html).

- Download and install the Citrix ADC Terraform provider plug-in from the [Citrix ADC Terraform Provider Official Repo](https://github.com/citrix/terraform-provider-citrixadc).

    You can download a release from the [releases page](https://github.com/citrix/terraform-provider-citrixadc/releases) and untar the binary into `~/.terraform.d/plugins/`.

### Perform the following steps for configuring Citrix ADC for the Anthos control plane using Terraform.

1. Clone the `citrix-k8s-ingress-controller` repository from GitHub using the following command.

       git clone https://github.com/citrix/citrix-k8s-ingress-controller.git
    
1. After cloning, change your directory using the following command.


        cd citrix-k8s-ingress-controller/deployment/anthos/citrix-adc-for-control-plane/

2. Provide the input configuration for Anthos.

   Update the [input-config.yaml](https://github.com/citrix/citrix-adc-anthos/blob/master/input-config.yaml) file according to your Anthos deployment.

   This input file is in-line with the Anthos input configuration YAML file.

   The following is a sample `input-config.yaml`.

   ```

    citrixadc:
        managementip: "10.20.30.40"
        username: "myuser"
        password: "mypassword"
    admincluster:
        nodes:
           - 10.0.0.1
           - 10.0.0.2
           - 10.0.0.3
           - 10.0.0.4
           - 10.0.0.5
        manuallbspec:
            ingresshttpnodeport: 32527
            ingresshttpsnodeport: 30139
            controlplanenodeport: 30968
            addonsnodeport: 31405
        vips:
            controlplanevip: "192.168.1.1"
            ingressvip: "192.168.1.2"
            addonsvip: "192.168.1.3"
    usercluster:
        - name: user-cluster-1
          manuallbspec:
            ingresshttpnodeport: 30243
            ingresshttpsnodeport: 30879
            controlplanenodeport: 30562
          vips:
            controlplanevip: "192.168.2.1"
            ingressvip: "192.168.2.2"
          nodes:
            - 10.1.0.1
            - 10.1.0.2
            - 10.1.0.3
        - name: user-cluster-2
          manuallbspec:
            ingresshttpnodeport: 30244
            ingresshttpsnodeport: 30880
            controlplanenodeport: 30563
          vips:
            controlplanevip: "192.168.3.1"
            ingressvip: "192.168.3.2"
          nodes:
            - 10.2.0.1
            - 10.2.0.2
            - 10.2.0.3
   ```

    **Note:**  The file name must be `input-config.yaml`. You should not change this file name.

3. Initialize Terraform by using the following step.

        terraform init

4. Apply the changes using the `terraform apply` command.


        terraform apply -auto-approve

## Unconfiguring Citrix ADC (Optional)

If the Citrix ADC configuration needs to be removed for some reason, you can use the `terraform destroy` command.


    terraform destroy -auto-approve

