resource "google_service_account" "rudeler_scheduler_service_account" {
  account_id   = "${local.deployment_name}-scheduler-sa"
  display_name = "${local.deployment_name} scheduler service account"
  description  = "Service account for scheduling cloud function ${local.deployment_name}"
}

resource "google_cloud_scheduler_job" "rudeler_schedule_job" {
  name             = "${google_cloudfunctions_function.rudeler.name}-scheduler"
  description      = "Schedules ${google_cloudfunctions_function.rudeler.name} cloud function"
  schedule         = var.rudeler_schedule
  time_zone        = "Europe/Berlin"
  attempt_deadline = "320s" # maybe change?

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.rudeler.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.rudeler_scheduler_service_account.email
    }
  }
}

resource "google_cloudfunctions_function_iam_member" "rudeler_scheduler_cloudfunctions_iam_roles" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.rudeler.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.rudeler_scheduler_service_account.email}"
}

resource "google_secret_manager_secret_iam_member" "rudeler_scheduler_secrets_iam_roles" {
  for_each  = local.rudeler_secrets

  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.rudeler_scheduler_service_account.email}"
}
