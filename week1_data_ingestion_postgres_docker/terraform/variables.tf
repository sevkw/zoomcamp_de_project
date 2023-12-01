## backend variables

variable "aws_region" {
  description = "AWS region for the backend resources"
  type        = string
  default     = "us-east-2"
}

variable "s3_bucket_name_backend" {
  description = "Name for the S3 bucket used as Terraform backend"
  type        = string
  default     = "terraform-back-end-bucket"
}

variable "dynamodb_table_name_backend" {
  description = "Name for the DynamoDB table used as Terraform backend lock table"
  type        = string
  default     = "terraform-backend-lock-table"
}

## infrastructure variables

variable "s3_bucket_name_datalake" {
  description = "Name for the S3 bucket used for Zoomcamp Datalake"
  type        = string
  default     = "datalake-bucket-zoomcamp-2023"
}

variable "redshift_cluster_name_dataset" {
  description = "Name for the Redshift cluster"
  type = string
  default = "dataset-redshift"
}

variable "redshift_cluster_db_dataset" {
  description = "The database name for Redshift cluster for dataset"
  type = string
  default = "trips_data_all"
}