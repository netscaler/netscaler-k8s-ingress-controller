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

locals {
  // Parse the Input YAML File
  input_yaml_file = "input-config.yaml"
  input_data = "${yamldecode(file(local.input_yaml_file))}"
  // Parse Citrix ADC Details from Input 
  citrix_adc_ip = local.input_data["citrixadc"]["managementip"]
  citrix_username = local.input_data["citrixadc"]["username"]
  citrix_password = local.input_data["citrixadc"]["password"]
  // Parse Admin Cluster details from Input
  admin_cluster = local.input_data["admincluster"]
  admin_cluster_control_plane_sg_members = formatlist("%s:%s", local.admin_cluster["nodes"], local.admin_cluster["manuallbspec"]["controlplanenodeport"])
  admin_cluster_addons_sg_members = formatlist("%s:%s", local.admin_cluster["nodes"], local.admin_cluster["manuallbspec"]["addonsnodeport"])
  admin_cluster_ingress_http_sg_members = formatlist("%s:%s", local.admin_cluster["nodes"], local.admin_cluster["manuallbspec"]["ingresshttpnodeport"])
  admin_cluster_ingress_https_sg_members = formatlist("%s:%s", local.admin_cluster["nodes"], local.admin_cluster["manuallbspec"]["ingresshttpsnodeport"])
  // Parse User Cluster details from Input
  user_cluster = local.input_data["usercluster"]
  user_cluster_count = length(local.user_cluster)
}

provider "citrixadc" {
    username = local.citrix_username
    password = local.citrix_password
    endpoint = format("https://%s/", local.citrix_adc_ip)
    insecure_skip_verify = false
}

// Admin Cluster Control Plane LB
resource "citrixadc_lbvserver" "anthos_admin_cluster_control_plane" {
  name = "anthos_lb_admin_cluster_control_plane"
  ipv46 = local.admin_cluster["vips"]["controlplanevip"]
  port = "443"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_admin_cluster_control_plane" {
  servicegroupname = "anthos_sg_admin_cluster_control_plane"
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_admin_cluster_control_plane.name}"]
  servicegroupmembers = local.admin_cluster_control_plane_sg_members
}

// Admin Cluster Addons LB
resource "citrixadc_lbvserver" "anthos_admin_addons" {
  name = "anthos_lb_admin_addons"
  ipv46 = local.admin_cluster["vips"]["addonsvip"]
  port = "8443"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_admin_addons" {
  servicegroupname = "anthos_sg_admin_addons"
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_admin_addons.name}"]
  servicegroupmembers = local.admin_cluster_addons_sg_members
}

// Admin Cluster HTTP Ingress
resource "citrixadc_lbvserver" "anthos_admin_http_ingress" {
  name = "anthos_lb_admin_http_ingress"
  ipv46 = local.admin_cluster["vips"]["ingressvip"]
  port = "80"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_admin_http_ingress" {
  servicegroupname = "anthos_sg_admin_http_ingress"
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_admin_http_ingress.name}"]
  servicegroupmembers = local.admin_cluster_ingress_http_sg_members
}

// Admin Cluster HTTPS Ingress
resource "citrixadc_lbvserver" "anthos_admin_https_ingress" {
  name = "anthos_lb_admin_https_ingress"
  ipv46 = local.admin_cluster["vips"]["ingressvip"]
  port = "443"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_admin_https_ingress" {
  servicegroupname = "anthos_sg_admin_https_ingress"
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_admin_https_ingress.name}"]
  servicegroupmembers = local.admin_cluster_ingress_https_sg_members
}

// User Clusters Control Plane
resource "citrixadc_lbvserver" "anthos_user_cluster_control_plane" {

  count = local.user_cluster_count

  name = format("anthos_lb_user_cluster-%s-control_plane", local.user_cluster[count.index]["name"])
  ipv46 = local.user_cluster[count.index]["vips"]["controlplanevip"]
  port = "443"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_user_cluster_control_plane" {

  count = local.user_cluster_count

  servicegroupname = format("anthos_sg_user_cluster-%s-control_plane", local.user_cluster[count.index]["name"])
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_user_cluster_control_plane[count.index].name}"]
  servicegroupmembers = formatlist("%s:%s", local.admin_cluster["nodes"], local.user_cluster[count.index]["manuallbspec"]["controlplanenodeport"])
}

// User Clusters HTTP Ingress
resource "citrixadc_lbvserver" "anthos_user_cluster_http_ingress" {

  count = local.user_cluster_count

  name = format("anthos_lb_user_cluster-%s-http_ingress", local.user_cluster[count.index]["name"])
  ipv46 = local.user_cluster[count.index]["vips"]["ingressvip"]
  port = "80"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_user_cluster_http_ingress" {

  count = local.user_cluster_count

  servicegroupname = format("anthos_sg_user_cluster-%s-http_ingress", local.user_cluster[count.index]["name"])
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_user_cluster_http_ingress[count.index].name}"]
  servicegroupmembers = formatlist("%s:%s", local.user_cluster[count.index]["nodes"], local.user_cluster[count.index]["manuallbspec"]["ingresshttpnodeport"])
}

// User Clusters HTTPS Ingress
resource "citrixadc_lbvserver" "anthos_user_cluster_https_ingress" {

  count = local.user_cluster_count

  name = format("anthos_lb_user_cluster-%s-https_ingress", local.user_cluster[count.index]["name"])
  ipv46 = local.user_cluster[count.index]["vips"]["ingressvip"]
  port = "443"
  servicetype = "TCP"
}
resource "citrixadc_servicegroup" "anthos_user_cluster_https_ingress" {

  count = local.user_cluster_count

  servicegroupname = format("anthos_sg_user_cluster-%s-https_ingress", local.user_cluster[count.index]["name"])
  servicetype = "TCP"
  lbvservers = ["${citrixadc_lbvserver.anthos_user_cluster_https_ingress[count.index].name}"]
  servicegroupmembers = formatlist("%s:%s", local.user_cluster[count.index]["nodes"], local.user_cluster[count.index]["manuallbspec"]["ingresshttpsnodeport"])
}
