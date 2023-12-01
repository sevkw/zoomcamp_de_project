## backend out puts

output "s3_bucket_arn" {
  value       = aws_s3_bucket.terraform_backend_bucket.arn
  description = "The ARN of the S3 bucket"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_lock_table.name
  description = "The name of the DynamoDB table"
}

#========================================================================== infrastructure outputs===========================================================#
# when getting started, comment out this section

output "datalake_s3_bucket_arn" {
  value       = aws_s3_bucket.data-lake-bucket.arn
  description = "The ARN of the S3 bucket for datalake."
}

output "redshift_cluster_db_name" {
  value       = aws_redshift_cluster.data_set.arn
  description = "The name of the DynamoDB table"
}