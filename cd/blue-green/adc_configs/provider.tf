terraform {
  backend "local" {
  }
  required_providers {
    citrixadc = {
      source = "citrix/citrixadc"
      version = "1.0.1"
    }
  }
}

provider "citrixadc" {
  endpoint = "http://<NSIP>"
  username = "<ADC username>"
  password = "<ADC password>"
}