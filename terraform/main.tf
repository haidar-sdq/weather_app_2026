provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {}

module "artifact_registry" {
  source    = "./modules/artifact_registry"
  repo_name = var.repo_name
  region    = var.region
}

module "secrets" {
  source           = "./modules/secrets"
  project_number   = data.google_project.project.number
}

module "cloud_run" {
  source       = "./modules/cloud_run"
  service_name = var.service_name
  region       = var.region
  image        = var.image

  depends_on = [
    module.secrets
  ]
}