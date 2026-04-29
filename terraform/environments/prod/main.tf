provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {}

terraform {
  backend "gcs" {
    bucket  = "weather-tf-state-bucket"
    prefix  = "prod/terraform"
  }
}

module "artifact_registry" {
  source    = "../../modules/artifact_registry"
  repo_name = local.repo_name
  region    = var.region
}

module "secrets" {
  source           = "../../modules/secrets"
  project_number   = data.google_project.project.number
}

module "cloud_run" {
  source       = "../../modules/cloud_run"
  service_name = "weather-app-${var.environment}"
  region       = var.region
  image        = var.image

  depends_on = [
    module.secrets
  ]
}