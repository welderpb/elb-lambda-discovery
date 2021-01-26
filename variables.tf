
variable "environment" {
  description = ""
  type        = string
  default     = "nonprod"
}

variable "name" {
  description = ""
  type        = string
  default     = "ELBDomainDiscovery"
}

variable "skip_tag" {
  description = "ELB Tag key for skip doscovery"
  type        = string
  default     = "SkipDomainDiscovery"
}

variable "regions" {
  description = "Text list of regions for Domain Discovery"
  type        = string
  default     = ["us-east-1"]
}
