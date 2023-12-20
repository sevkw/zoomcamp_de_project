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

# 🚗Provisioning Redshift via Terraform
At the time of the creation of this repo, Redshift Serverless is available for trial. Therefore the best approach would be to go with Redshift Serverless instead of the classical Redshift Cluster. The `main.tf` contains codes to provision Redshift with the clusters and serverless. However, only one should be used. I decided to write out the code for both just for learning purpose. I have comment out the provisioning code for Redshift cluster. However the idea is really the same.

**Please ensure you have the following set up before you configure Redshift service:**
1. IAM Role: I recommend creating a new IAM Role dedicated to be attached to allow the Redshift service to have access to other AWS resources, such as S3 bucket. To learn more about IAM Roles, checkout [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html). Here are the policies I attached to the dedicated IAM role for redshift: `AmazonDMSRedshiftS3Role`, `AmazonRedshiftAllCommandsFullAccess`, `AmazonRedshiftFullAccess`, `AmazonRedshiftQueryEditorV2FullAccess`, `AmazonS3ReadOnlyAccess`. I named this IAM role `redshift-service-role`.
2. Security groups: This has to be set up to allow inbound or outbound traffic to access Redshift. For example, uploading data to Redshift will require an access via port 5439. If the security group is not set up properly, you cannot upload data. To lean more about AWS VPC security groups, check out [here](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html). Here are my settings for the security group, which I named `redshift-security`: Allowed both Ipv4 and Ipv6 traffic via port 5439 from anywhere. (Note that in actual practice this is not the ideal setting.)
   
After setting these up, ensure you configure these for your Redshift resource.

## 🏗️ Provisioning AWS Redshift Serverless
AWS Redshift Serverless provision involves two parts: a namespace - the objects - and a workgroup - the computing resources. Each will be configured individually. You will first need to configure the namespace and then configuring the workgroup while referencing the namespace. See more details in the Terraform AWS documentation in the Reference section.

# Reference 📚

- When I ran `terraform destroy`, an ERROR message saying `Redshift Cluster Instance FinalSnapshotIndentifier is required when a fianl snapshot is required` came up. I found [this Stackoverflow](https://stackoverflow.com/questions/50930470/terraform-error-rds-cluster-finalsnapshotidentifier-is-required-when-a-final-s) thread to be helpful.
- [Terraform aws documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/redshift_cluster) for configuring Redshift cluster
- [Terraform aws documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/redshiftserverless_namespace) for configuring Redshift serverless namespace
- [Terraform aws documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/redshiftserverless_workgroup) for configuring Redshift serverless workgroup 
- [This Medium article](https://gmusumeci.medium.com/how-to-deploy-an-amazon-redshift-serverless-in-aws-using-terraform-1cf67835d3b4) provides great example on how to configure Redshift Serverless. However, for this reference, I do not recommend saving your AWS ACCESS Keys as `variables.tf`. Please only reference to the part that showcases the Redshift Serverless configuration.
- [AWS Official documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html): Compute capacity for Amazon Redshift Serverless