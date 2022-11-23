resource "google_project_service" "enable_cloud_scheduler_api" {
  service = "cloudscheduler.googleapis.com"
}

resource "google_service_account" "scheduler_service_account" {
  account_id   = "${local.deployment_name}-scheduler-sa"
  display_name = "Service account for scheduling cloud function ${local.deployment_name}"
}

resource "google_cloud_scheduler_job" "schedule_rudeler" {
  name             = "${google_cloudfunctions_function.rudeler.name}-scheduler"
  description      = "Schedules ${google_cloudfunctions_function.rudeler.name} cloud function"
  schedule         = var.rudeler_schedule
  time_zone        = "Europe/Berlin"
  attempt_deadline = "320s" # maybe change?

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.rudeler.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.scheduler_service_account.email
    }
  }

  depends_on = [
    google_project_service.enable_cloud_scheduler_api,
  ]
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.rudeler.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}
