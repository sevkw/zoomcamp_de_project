output "redshift_cluster_arn" {
  value       = aws_redshift_cluster.data_set.arn
  description = "The ARN of the Redshift cluster."
}


output "redshift_cluster_endpoint" {
  value = aws_redshift_cluster.data_set.endpoint  
}

output "redshift_cluster_port" {
  value = aws_redshift_cluster.data_set.port
}

output "redshift_cluster_dbname" {
  value = aws_redshift_cluster.data_set.database_name
}

output "glue_connection_arn" {
  value = aws_glue_connection.redshift_glue.arn
}