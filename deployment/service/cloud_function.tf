locals {
  cloud_functions_sources_archive_path = abspath("${path.module}/../..")
  cloud_functions_source_archive_path  = "${local.cloud_functions_sources_archive_path}/${var.rudeler_archive}"
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
  service_account_email        = google_service_account.rudeler_scheduler_service_account.email

  environment_variables = {
    RUDELER_SEARCH_CONFIGURATION = var.rudeler_search_configuration
    SPOND_BOT_ACCOUNT_ID         = var.spond_bot_account_id
    SPOND_GROUP_ID               = var.spond_group_id
    SPOND_SUB_GROUP_ID           = var.spond_sub_group_id
  }

  dynamic "secret_environment_variables" {
    for_each = local.rudeler_secrets

    content {
      key     = secret_environment_variables.key
      secret  = secret_environment_variables.value
      version = 1
    }
  }

  depends_on = [
    google_secret_manager_secret_iam_member.rudeler_scheduler_secrets_iam_roles,
  ]
}
