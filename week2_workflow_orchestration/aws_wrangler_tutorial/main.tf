data "aws_ssm_parameter" "redshift_password" {
  name = "/redshift/zoomcamp-dataset" #assume you have saved a Parameter in the SSM Manager's Parameter Store
}

resource "aws_redshift_cluster" "data_set" {
  cluster_identifier = var.redshift_cluster_name_dataset
  database_name      = var.redshift_cluster_db_dataset
  master_username    = "masteruser" # note that you may be prompted with error message if the master_username has a bad format
  master_password    = data.aws_ssm_parameter.redshift_password.value # you need to ensure your master_password contain at least a number
  node_type          = "dc2.large" # double check with the node_type available in your region, as this could be different in other regions
  cluster_type       = "single-node"
  skip_final_snapshot = true
  iam_roles = var.redshift_iam_roles
  default_iam_role_arn = var.redshift_service_role
  vpc_security_group_ids = var.redshift_security_group_list
}

resource "aws_glue_connection" "redshift_glue" {
    name = "zoomcamp_redshift_glue_connection"
    connection_type = "JDBC"
    description = "Connection created for Redshift cluster and aws wrangler python notebook demo"

    connection_properties = {
      JDBC_CONNECTION_URL = "jdbc:redshift://${aws_redshift_cluster.data_set.endpoint}/${aws_redshift_cluster.data_set.database_name}"
      USERNAME = "masteruser"
      PASSWORD = data.aws_ssm_parameter.redshift_password.value
    }

}