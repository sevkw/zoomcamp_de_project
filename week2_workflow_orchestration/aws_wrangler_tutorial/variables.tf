variable "redshift_cluster_name_dataset" {
  description = "Name for the Redshift cluster"
  type = string
  default = "zoomcamp-dataset-redshift"
}

variable "redshift_cluster_db_dataset" {
  description = "The database name for Redshift cluster for dataset"
  type = string
  default = "trips_data_all"
}

variable "redshift_iam_roles" {
  description = "A list of IAM ARNs that should be associated with the provisioned Redshift service"
  type = list
  default = ["arn:aws:iam::571772404385:role/redshift-service-role"]
}

variable "redshift_service_role" {
  description = "IAM role to be attached to provisioned Redshift service. Note that this role should also be included in the redshift_iam_roles list."
  type = string
  default = "arn:aws:iam::571772404385:role/redshift-service-role"
}

variable "redshift_security_group_list" {
  description = "The list of security group IDs to be associated with the provisioned Redshift service"
  type = list
  default = ["sg-0cf5b9ef80fe2fca1"]
}