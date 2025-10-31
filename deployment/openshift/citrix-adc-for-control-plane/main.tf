/*
Copyright 2016 Citrix Systems, Inc
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

provider "citrixadc" {
    username = var.citrix_adc_username
    password = var.citrix_adc_password
    endpoint = format("https://%s/", var.citrix_adc_ip)
    insecure_skip_verify = false
}

locals {
  api_server_sg_members = formatlist("%s:6443", var.api_backend_addresses)
  machine_config_sg_members = formatlist("%s:22623", var.api_backend_addresses)
  ingress_http_sg_members = formatlist("%s:80", var.ingress_backend_addresses)
  ingress_https_sg_members = formatlist("%s:443", var.ingress_backend_addresses)
}

// API Server Load-Balancing
resource "citrixadc_lbvserver" "openshift_api_server" {
  name = "openshift_lb_api_server"
  ipv46 = var.lb_ip_address
  port = var.api_server["lb_port"]
  servicetype = var.api_server["lb_protocol"]
}
resource "citrixadc_servicegroup" "openshift_api_server" {
  servicegroupname = "openshift_sg_api_server"
  servicetype = var.api_server["lb_protocol"]
  lbvservers = ["${citrixadc_lbvserver.openshift_api_server.name}"]
  servicegroupmembers = local.api_server_sg_members
}

// Machine Config Server Load-Balancing
resource "citrixadc_lbvserver" "openshift_machine_config_server" {
  name = "openshift_lb_machine_config_server"
  ipv46 = var.lb_ip_address
  port = var.machine_config_server["lb_port"]
  servicetype = var.machine_config_server["lb_protocol"]
}
resource "citrixadc_servicegroup" "openshift_machine_config_server" {
  servicegroupname = "openshift_sg_machine_config_server"
  servicetype = var.machine_config_server["lb_protocol"]
  lbvservers = ["${citrixadc_lbvserver.openshift_machine_config_server.name}"]
  servicegroupmembers = local.machine_config_sg_members
}

// HTTP Ingress Load-Balancing
resource "citrixadc_lbvserver" "openshift_ingress_http" {
  name = "openshift_lb_ingress_http"
  ipv46 = var.lb_ip_address
  port = var.ingress_http["lb_port"]
  servicetype = var.ingress_http["lb_protocol"]
}
resource "citrixadc_servicegroup" "openshift_ingress_http" {
  servicegroupname = "openshift_sg_ingress_http"
  servicetype = var.ingress_http["lb_protocol"]
  lbvservers = ["${citrixadc_lbvserver.openshift_ingress_http.name}"]
  servicegroupmembers = local.ingress_http_sg_members
}

// HTTPS Ingress Load-Balancing
resource "citrixadc_lbvserver" "openshift_ingress_https" {
  name = "openshift_lb_ingress_https"
  ipv46 = var.lb_ip_address
  port = var.ingress_https["lb_port"]
  servicetype = var.ingress_https["lb_protocol"]
}
resource "citrixadc_servicegroup" "openshift_ingress_https" {
  servicegroupname = "openshift_sg_ingress_https"
  servicetype = var.ingress_https["lb_protocol"]
  lbvservers = ["${citrixadc_lbvserver.openshift_ingress_https.name}"]
  servicegroupmembers = local.ingress_https_sg_members
}
