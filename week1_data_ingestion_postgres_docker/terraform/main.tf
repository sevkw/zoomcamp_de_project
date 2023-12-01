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

## backend resources

resource "aws_s3_bucket" "terraform_backend_bucket" {
  bucket = var.s3_bucket_name_backend
  force_destroy = true
}
# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_backend_bucket" {
  bucket = aws_s3_bucket.terraform_backend_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_lock_table" {
  name           = var.dynamodb_table_name_backend
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
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

resource "aws_redshift_cluster" "data_set" {
  cluster_identifier = var.redshift_cluster_name_dataset
  database_name      = var.redshift_cluster_db_dataset
  master_username    = "masteruser" # note that you may be prompted with error message if the master_username has a bad format
  master_password    = data.aws_ssm_parameter.redshift_password.value # you need to ensure your master_password contain at least a number
  node_type          = "dc2.large" # double check with the node_type available in your region, as this could be different in other regions
  cluster_type       = "single-node"
}
