variable "project_id" {
  default = "project-7aaa7a69-7aef-409d-94b"
}

variable "region" {
  default = "asia-south1"
}

variable "environment" {
  type = string
}

locals {
  repo_name = "weather-repo-${var.environment}"
}


variable "service_name" {
  default = "weather-app"
}

variable "image" {}