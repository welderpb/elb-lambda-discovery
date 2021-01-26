
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
  description = "List of regions for Domain Discovery"
  type        = list(string)
  default     = ["us-east-1"]
}

variable "types" {
  description = "List of types of ELB"
  type        = list(string)
  default     = ["application"]
}

variable "api_url" {
  type    = string
  default = "https://com.com"
}

variable "source" {
  type    = string
  default = "ELB"
}
