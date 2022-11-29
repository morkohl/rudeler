locals {
  deployment_name = "${var.service_name}-${var.environment}"

  rudeler_secrets = {
    "ASVZ_USERNAME" : "${local.deployment_name}-asvz-username",
    "ASVZ_PASSWORD" : "${local.deployment_name}-asvz-password",
    "SPOND_USERNAME" : "${local.deployment_name}-spond-username",
    "SPOND_PASSWORD" : "${local.deployment_name}-spond-password"
  }
}
