variable "project_id" {
  type        = string
  description = "The GCP project to deploy resources in"
  default     = "rudeler"
}

variable "region" {
  type        = string
  description = "The GCP region to deploy resources in"
  default     = "europe-west1"
}

variable "service_name" {
  type        = string
  description = "The name of the service to deploy"
  default     = "rudeler"
}

variable "rudeler_schedule" {
  type        = string
  description = "The cron expression for the scheduling of rudeler bot"
  default     = "0 * * * *"
}

variable "rudeler_archive" {
  type        = string
  description = "The name archive containing sources for the google cloud functon"
  default     = "rudeler.zip"
}

variable "environment" {
  type        = string
  description = "The environment to deploy in"
}
