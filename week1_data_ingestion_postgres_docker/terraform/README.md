# Terraform Configuration for AWS Resources

When following the Terraform exercise, I decide to provision the services using AWS instead of GCP.
I find the Zoomcamp does a poor job in going through critical Terraform items, so I decided to pick up the knowledge myself.

I find Terraform actually does a great job with Tutorials.

Follow this set of [Terraform AWS Tutorials](https://developer.hashicorp.com/terraform/tutorials/aws-get-started) to get started.

After that you should be able to create some AWS sources with a local backend on your local machine.

# Remote Backend in S3 and DynamoDB
In [the last section of the Terraform AWS tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-remote), the idea of Store Remote State is introduced. However, to set up the backend, I went through a different track through provisioning the backend storage through S3 bucket and DynamoDB.

The original reference I used to experiment this was through this blog: [Deploying a Terraform Remote State Backend with AWS S3 and DynamoDB](https://hackernoon.com/deploying-a-terraform-remote-state-backend-with-aws-s3-and-dynamodb).

In my actual work, I updated the main.tf a bit differently. However the concept is still the same.

To summarize, we have to go through the following steps to ensure we have our whole infrastructure backed-up properly:

1. Initiate the Backend resources. To do so, please pay attention to the inline comments and comment out the `backend` block in the `terraform` block. Other than that, you also need to comment out the resource configuration blocks for your actual infrastructure. Do the same for the `outputs.tf`. Eventually, you should first run `terraform init` and `terraform apply` with only the backend resources.
2. After you have provisioned the backend resources, you should uncomment the `backend{}` block in the `main.tf` as well as the infrastructure resources' variables and outputs. After that run `terraform init` and `terraform apply` again to fully provision your infrastructure that will be backed up in cloud.

