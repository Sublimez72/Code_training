


variable "password" {}
variable "user_name" {}
variable "tenant_name" {}
variable "az_list" {
  description = "List of Availability Zones available in your OpenStack cluster"
  type = list
  default = ["sto1", "sto2", "sto3"]
}


terraform {
  required_providers {
    openstack = {
        source = "terraform-provider-openstack/openstack"
    }
  }
}

provider "openstack" {
  user_name = var.user_name
  tenant_name = var.tenant_name
  password = var.password
  auth_url = "https://ops.elastx.cloud:5000/v3"
}

resource "openstack_compute_keypair_v2" "demo_keypair" {
  name = "debian-keypair"
  public_key = file("id_rsa.pub")
}

resource "openstack_compute_instance_v2" "name" {
  
}