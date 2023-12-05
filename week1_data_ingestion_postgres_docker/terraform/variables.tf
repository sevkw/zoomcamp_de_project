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