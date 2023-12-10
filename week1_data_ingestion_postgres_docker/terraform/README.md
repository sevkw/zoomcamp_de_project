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

1. Initiate the Backend resources. To do so, please first `cd` into the backend directory. From there, run `terraform init` and `terraform apply`.
   
2. You should have the s3 and dynamoDB resources being provisioned.
   
3. After you have provisioned the backend resources, go back to the terraform directory, and run `terraform init` and `terraform apply`. This will get the infrastructure provisioned for the s3 bucket for raw data and the Redshift. Note that the infrastructure will have a remote backend.
4. To avoid being charged for Redshift instances, you can run `terraform destroy` to remove all the infrastructure services. Please ensure you are running `terraform destroy` in the `terraform` directory, not the `backend` directory.

# Reference

- When I ran `terraform destroy`, an ERROR message saying `Redshift Cluster Instance FinalSnapshotIndentifier is required when a fianl snapshot is required` came up. I found [this Stackoverflow](https://stackoverflow.com/questions/50930470/terraform-error-rds-cluster-finalsnapshotidentifier-is-required-when-a-final-s) thread to be helpful.