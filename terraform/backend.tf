terraform {
  backend "gcs" {
    bucket = "rudeler-bucket-tfstate"
    prefix = "terraform/state/${var.environment}"
  }
}
