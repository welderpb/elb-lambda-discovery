
variable "asg_name" {
  description = ""
  type = string
}

variable "environment" {
  description = ""
  type = string
}

variable "name" {
  description = ""
  type = string
}

variable "aws_region" {
  description = ""
  type = string
}

variable "zone_id" {
  description = ""
  type = string
}

variable "cname_tag" {
  type = string
}

variable "regions" {
  type = list(string)
  default = ["us-east-1"]
}
