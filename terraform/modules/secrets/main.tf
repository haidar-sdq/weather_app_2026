resource "google_secret_manager_secret" "weather" {
  secret_id = "weather-api-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "weather_version" {
  secret      = google_secret_manager_secret.weather.id
  secret_data = var.weather_api_key
}

resource "google_secret_manager_secret" "jwt" {
  secret_id = "jwt-secret"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "jwt_version" {
  secret      = google_secret_manager_secret.jwt.id
  secret_data = var.jwt_secret
}

resource "google_secret_manager_secret_iam_member" "weather_access" {
  secret_id = google_secret_manager_secret.weather.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
}

resource "google_secret_manager_secret_iam_member" "jwt_access" {
  secret_id = google_secret_manager_secret.jwt.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
}