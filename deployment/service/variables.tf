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

variable "rudeler_archive" {
  type        = string
  description = "The name archive containing sources for the google cloud functon"
  default     = "rudeler.zip"
}

variable "rudeler_schedule" {
  type        = string
  description = "The cron expression for the scheduling of rudeler bot"
}

variable "environment" {
  type        = string
  description = "The environment to deploy in"
}

variable "rudeler_search_configuration" {
  type        = string
  description = "The search configuration to run events with"
}

variable "spond_bot_account_id" {
  type        = string
  description = "The spond account id to run rudeler with"
}

variable "spond_group_id" {
  type        = string
  description = "The spond group id to run rudeler with"
}

variable "spond_sub_group_id" {
  type        = string
  description = "The spond sub group id to run rudeler with"
}
