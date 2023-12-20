# main.tf

terraform {
  required_version = ">= 1.0.0"
  #   When getting started and the back end resource is not set up, comment out the back end block
   backend "s3" {
       # Replace this with your bucket name!
      bucket = "terraform-back-end-bucket"
      key = "./terraform.tfstate"
      region = "us-east-2"
      # Replace this with your DynamoDB table name!
      dynamodb_table = "terraform-backend-lock-table"
      encrypt = true
     }
# after running the first terraform init for the resources below, uncomment the backend block
# and do terraform init again and then terraform deploy again
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-2"
  # Add other AWS provider configurations if needed
}

# ===============================INFRASTRUCTURE============================================#
# when getting started with backend, comment out the resources config
# Your actual infrastructure resources go here
# Data Lake Bucket (AWS S3)
resource "aws_s3_bucket" "data-lake-bucket" {
  bucket        = var.s3_bucket_name_datalake
  force_destroy = true
}

# Enable versioning for the Data Lake Bucket (AWS S3)
resource "aws_s3_bucket_versioning" "datalake_versioning" {
  bucket = aws_s3_bucket.data-lake-bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Data Lake Bucket Lifecycle Configuration
resource "aws_s3_bucket_lifecycle_configuration" "datalake-lifecycle" {
  bucket = aws_s3_bucket.data-lake-bucket.id

  rule {
    id = "expiration-rule"

    expiration {
      days = 30
    }

    status = "Enabled"
  }
}


# Data Warehouse (AWS Redshift)
# retrieve redshift masterpassword using the AWS ssm parameter
data "aws_ssm_parameter" "redshift_password" {
  name = "/redshift/zoomcamp-dataset" #assume you have saved a Parameter in the SSM Manager's Parameter Store
}

## Below is code for configuring Redshift Cluster service
# resource "aws_redshift_cluster" "data_set" {
#   cluster_identifier = var.redshift_cluster_name_dataset
#   database_name      = var.redshift_cluster_db_dataset
#   master_username    = "masteruser" # note that you may be prompted with error message if the master_username has a bad format
#   master_password    = data.aws_ssm_parameter.redshift_password.value # you need to ensure your master_password contain at least a number
#   node_type          = "dc2.large" # double check with the node_type available in your region, as this could be different in other regions
#   cluster_type       = "single-node"
#   skip_final_snapshot = true
#   iam_roles = var.redshift_iam_roles
#   default_iam_role_arn = var.redshift_service_role
#   vpc_security_group_ids = var.redshift_security_group_list
# }

## Below is configuration for Redshift Serverless namespace

resource "aws_redshiftserverless_namespace" "zoomcamp_dataset" {
  namespace_name = var.redshift_serverless_ns_name
  iam_roles = var.redshift_iam_roles
  default_iam_role_arn = var.redshift_service_role
  admin_username = "masteruser"
  admin_user_password = data.aws_ssm_parameter.redshift_password.value
  db_name = var.redshift_cluster_db_dataset
}

resource "aws_redshiftserverless_workgroup" "zoomcamp_dataset" {
  namespace_name = aws_redshiftserverless_namespace.zoomcamp_dataset.id
  workgroup_name = var.redshift_serverless_wg_name
  publicly_accessible = true
  security_group_ids = var.redshift_security_group_list
}

# set a limit to redshift serverless to save money ;)
# checkout reference section for more information
resource "aws_redshiftserverless_usage_limit" "zoomcamp_dataset" {
  resource_arn = aws_redshiftserverless_workgroup.zoomcamp_dataset.arn
  usage_type   = "serverless-compute"
  amount       = 8
}

## glue connection for uploading data to Redshift
## may be needed if connecting to redshift serverless via aws wrangle
## does not need if connecting using redshift-connector module
# resource "aws_glue_connection" "redshift_serverless_glue" {
#     name = "zoomcamp glue"
#     connection_type = "JDBC"
#     description = "Connection created for Redshift serverless namespace and aws wrangler python notebook demo"

#     connection_properties = {
#       JDBC_CONNECTION_URL = "jdbc:redshift://${aws_redshiftserverless_workgroup.zoomcamp_dataset.endpoint[0].address}/${aws_redshiftserverless_namespace.zoomcamp_dataset.db_name}"
#       USERNAME = "masteruser"
#       PASSWORD = data.aws_ssm_parameter.redshift_password.value
#     }

# }