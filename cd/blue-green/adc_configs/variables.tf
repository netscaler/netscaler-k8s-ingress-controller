variable "traffic_weight" {
  description = "Percentage of Traffic to be split"
  type        = number
  default     = 100
}
variable "backend_service_ip" {
  description = "The backend service IP"
  type        = string
  default     = "0.0.0.0"
}
variable "resource_prefix" {
  description = "Prefix of resources to be created"
  type = string
  default = "demo"
}
variable "priority" {
  description = "CS Policy Priority"
  type = number
  default = 100
}