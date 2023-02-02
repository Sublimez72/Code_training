

variable "password" {}
variable "user_name" {}
variable "tenant_name" {}


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


resource "openstack_networking_router_v2" "router" {
  name                = "router"
  admin_state_up      = true
  external_network_id = "776f27b0-7447-4e35-acc0-4f4893c44d0c"
}


resource "openstack_compute_keypair_v2" "debian_keypair" {
  name = "debian-keypair"
  public_key = file("id_rsa.pub")
}


resource "openstack_compute_keypair_v2" "macbook_keypair" {
  name = "macbook-keypair"
  public_key = file("macbook_key.pub")
}


resource "openstack_compute_servergroup_v2" "lab2_webservers" {
  name = "webservers"
  policies = ["anti-affinity"]
}


resource "openstack_compute_secgroup_v2" "ssh_sg" {
  name = "ssh-sg"
  description = "ssh security group"
  rule {
    from_port = 22
    to_port = 22
    ip_protocol = "tcp"
    cidr = "0.0.0.0/0"
  }
}


resource "openstack_compute_secgroup_v2" "webserver_sg" {
  name = "webserver-sg"
  description = "webserver security group"
  rule {
    from_port = 80
    to_port = 80
    ip_protocol = "tcp"
    cidr = "0.0.0.0/0"
  }
  rule {
    from_port = 22
    to_port = 22
    ip_protocol = "tcp"
    from_group_id = "${openstack_compute_secgroup_v2.ssh_sg.id}"
  }
}


resource "openstack_networking_network_v2" "lab2_network" {
  name           = "lab2_network"
  admin_state_up = "true"
}


resource "openstack_networking_subnet_v2" "lab2_subnet" {
  network_id = "${openstack_networking_network_v2.lab2_network.id}"
  cidr = "10.10.1.0/24"
}


resource "openstack_networking_router_interface_v2" "int-ext-interface" {
  router_id = openstack_networking_router_v2.router.id
  subnet_id = openstack_networking_subnet_v2.lab2_subnet.id
}


resource "openstack_compute_instance_v2" "lab2_webserver1" {
  name            = "lab2_webserver1"
  image_id        = "ad091b52-742f-469e-8f3c-fd81cadf0743"
  flavor_id       = "3"
  key_pair        = "my_key_pair_name"
  security_groups = ["default"]

  metadata = {
    this = "that"
  }

  network {
    name = "my_network"
  }
}