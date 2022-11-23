locals {
  cloud_functions_sources_archive_path = abspath("${path.module}/..")
  cloud_functions_source_archive_path  = "${local.cloud_functions_sources_archive_path}/${var.rudeler_archive}"

  asvz_username_secret_id = "${var.environment}-asvz-username"
  asvz_password_secret_id = "${var.environment}-asvz-password"
  spond_username_secret_id = "${var.environment}-spond-username"
  spond_password_secret_id = "${var.environment}-spond-password"
}

resource "google_project_service" "enable_cloud_build_api" {
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "enable_cloud_functions_api" {
  service = "cloudfunctions.googleapis.com"
}

resource "google_storage_bucket" "rudeler_sources_bucket" {
  name     = "${local.deployment_name}-cloud-function-sources"
  location = var.region
}

resource "google_storage_bucket_object" "rudeler_sources_bucket_object" {
  bucket = google_storage_bucket.rudeler_sources_bucket.name
  name   = var.rudeler_archive
  source = local.cloud_functions_source_archive_path
}

resource "google_secret_manager_secret_iam_member" "rudeler_access_asvz_username" {
  secret_id = local.asvz_username_secret_id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}

resource "google_secret_manager_secret_iam_member" "rudeler_access_asvz_password" {
  secret_id = local.asvz_password_secret_id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}

resource "google_secret_manager_secret_iam_member" "rudeler_access_spond_username" {
  secret_id = local.spond_username_secret_id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}

resource "google_secret_manager_secret_iam_member" "rudeler_access_spond_password" {
  secret_id = local.spond_password_secret_id#
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}

resource "google_cloudfunctions_function" "rudeler" {
  name                         = local.deployment_name
  source_archive_bucket        = google_storage_bucket.rudeler_sources_bucket.name
  source_archive_object        = google_storage_bucket_object.rudeler_sources_bucket_object.name
  runtime                      = "python310"
  entry_point                  = "run_rudeler"
  available_memory_mb          = 128
  max_instances                = 1
  timeout                      = 180
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"
  service_account_email        = google_service_account.scheduler_service_account.email

  environment_variables = {
    RUDELER_SEARCH_CONFIGURATION = var.rudeler_search_configuration
    SPOND_BOT_ACCOUNT_ID         = var.spond_bot_account_id
    SPOND_GROUP_ID               = var.spond_group_id
    SPOND_SUB_GROUP_ID           = var.spond_sub_group_id
  }

  secret_environment_variables {
    key     = "ASVZ_USERNAME"
    secret  = local.asvz_username_secret_id
    version = 1
  }

  secret_environment_variables {
    key     = "ASVZ_PASSWORD"
    secret  = local.asvz_password_secret_id
    version = 1
  }

  secret_environment_variables {
    key     = "SPOND_USERNAME"
    secret  = local.spond_username_secret_id
    version = 1
  }

  secret_environment_variables {
    key     = "SPOND_PASSWORD"
    secret  = local.spond_password_secret_id
    version = 1
  }

  depends_on = [
    google_project_service.enable_cloud_build_api,
    google_project_service.enable_cloud_functions_api,

    google_secret_manager_secret_iam_member.rudeler_access_asvz_username,
    google_secret_manager_secret_iam_member.rudeler_access_asvz_password,
    google_secret_manager_secret_iam_member.rudeler_access_spond_username,
    google_secret_manager_secret_iam_member.rudeler_access_spond_password
  ]
}
