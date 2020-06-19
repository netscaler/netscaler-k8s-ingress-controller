# Citrix ADC for Anthos Control Plane

## Pre-requisites:

1. Terraform

    If you are using MacOS, then `brew install terraform` would install terraform on your Mac

    For any other OS, please refer the [official Terraform installation guide](https://learn.hashicorp.com/terraform/getting-started/install.html)

2. Citrix ADC Terraform provider

    [Citrix ADC Terraform Provider Official Repo](https://github.com/citrix/terraform-provider-citrixadc)

    You can download a release from [releases page](https://github.com/citrix/terraform-provider-citrixadc/releases) and just untar the binary into `~/.terraform.d/plugins/`
    

## Provide the Input Configuration for Anthos

Update the [input-config.yaml](https://github.com/citrix/citrix-adc-anthos/blob/master/input-config.yaml) file according to your Anthos deployment.

This input file was designed to be in-line with Anthos Input Config YAML file.

Sample `input-config.yaml` below:

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

**Note:** The file name should not be changed. The file name should be `input-config.yaml` 


## Terraform Init

```
terraform init
```

## Terraform Apply

```
terraform apply -auto-approve
```

## Terrafor Destroy

```
terraform destroy -auto-approve
```
