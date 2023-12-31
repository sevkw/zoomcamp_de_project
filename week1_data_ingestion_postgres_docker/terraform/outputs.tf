#========================================================================== infrastructure outputs===========================================================#

output "datalake_s3_bucket_arn" {
  value       = aws_s3_bucket.data-lake-bucket.arn
  description = "The ARN of the S3 bucket for datalake."
}

# output "redshift_cluster_arn" {
#   value       = aws_redshift_cluster.data_set.arn
#   description = "The ARN of the Redshift cluster."
# }

output "redshift_serverless_namespace_arn" {
  value = aws_redshiftserverless_namespace.zoomcamp_dataset.arn
}

output "redshift_serverless_namespace_dbname" {
  value = aws_redshiftserverless_namespace.zoomcamp_dataset.db_name
}

output "redshift_serverless_workgroup_arn" {
  value = aws_redshiftserverless_workgroup.zoomcamp_dataset.arn
}

output "redshift_serverless_wg_vpcendpoint_address" {
  value = aws_redshiftserverless_workgroup.zoomcamp_dataset.endpoint[0].address
}

output "redshift_serverless_wg_vpcendpoint_port" {
  value = aws_redshiftserverless_workgroup.zoomcamp_dataset.endpoint[0].port
}
