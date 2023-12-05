# main.tf

terraform {
  required_version = ">= 1.0.0"
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