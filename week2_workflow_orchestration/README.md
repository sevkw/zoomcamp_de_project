# 🤖Week2 Summary

## Pre-requests
To be able to run the local python codes and load the data to the postgres database, the docker containers created from Week1 must be up and running. Simply start the two containers from the application or run the following commands **from the week1's folder**:

```bash
docker compose up -d
```

### Terraform from Week1 Can be Used for This Week's Exerice
This week's exercise involves extracting raw data from original source and save a copy to s3 bucket. Then reading the raw copy from s3 bucket and transform it. The transformed data will be uploaded to Amazon Redshift. 

Recall from Week 1's exercise, we have used Terraform to configure the resources we need. Therefore, before beginning this week's exericse, you can go into week1 folder and run `terraform apply` command inside the `terraform/` directory to start the service.

If you only want to provision only 1 resource, for example, only provision the Redshift service, simply run the following:

```bash
terraform apply -target=aws_redshift_cluster.data_set
```
For provisioning only the Redshift Serverless namespace and workgroup at once:

```bash
terraform apply -target=aws_redshiftserverless_namespace.zoomcamp_dataset -target=aws_redshiftserverless_workgroup.zoomcamp_dataset -target=aws_redshiftserverless_usage_limit.zoomcamp_dataset
terraform destroy -target=aws_redshiftserverless_namespace.zoomcamp_dataset -target=aws_redshiftserverless_workgroup.zoomcamp_dataset -target=aws_redshiftserverless_usage_limit.zoomcamp_dataset
```
**Note: Can only choose Redshift Clusters or Redshift Serverless Namespace & Workgroup. Also remember to comment/uncomment out the corresponding service configuration sections in the `main.tf`**

For provisioning only the S3 bucket service, simply run:

```bash
terraform apply -target=aws_s3_bucket.data-lake-bucket
```

Doing so will help you save the money from being charged from using the Redshift cluster resource. After finishing your exercise, you can also run `terraform destroy -target=` to destroy the resource you want to remove.

## Prefect Tutorial
I personally felt a bit nervous when just learning about Prefect from scratch through the zoomcamp. Therefore, before I started, I studied the basic concepts via Prefect's guide. I highly recommend following the official website to learn the basic, because the zoomcamp contents will make more sense afterwards.

- Learn Prefect basic [from here](https://docs.prefect.io/latest/getting-started/quickstart/)
- After the Prefect Quickstart, also follow [the Tutorials section](https://docs.prefect.io/latest/tutorial/)

# 📹Intro to Prefect Concepts
Note that the starting code from the original repo and the demo video looks slightly different from the week 1 python code for data ingest. The different part was in the part where argparse was used to allow users to define parameters via cli when running thr commands below:

```bash
$ python3 data_ingest.py \
--user=admin \
--password=admin \
--host=localhost \
--port=5432 \
--db=ny_taxi \
--table-name=yellow_taxi \
--url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet
```

Instead, the starting file had the `main()` function taking the inputs as variables. The `data_ingest.py` in this week starts from here.
The `data_ingest_prefect.py` is the version with prefect module.

## 🏃Running Prefect Flow
The video seems to not demonstrate that, before running a prefect flow, the self-hosted prefect server (for the UI) should be started. After adjusting the data_ingest.py with `@flow` and `@task` decorators, please ensure you run:
```bash
prefect server start
```
After running, you should be able to open the self-hosted Prefect UI via your [local host](http://127.0.0.1:4200).
Note that once this is run, the terminal will be listening to the API, so please start a new terminal to run new commands there. In the new terminal window, run:

```bash
python data_ingest_prefect.py
```
After that you should be able to see this flow being completed in the self-hosted UI.

## Prefect Blocks Setup
Following [the video](https://youtu.be/cdtN6dhp708?feature=shared&t=1861), a SQLAlchemy block has to be set up via the Prefect UI. At a high level, blocks are reusable variables, credentials, and objects that can be referenced in our flows.

The block is set up per below:

```
block name: postgres-connector
driver: postgesql+psycopg2
database: ny_taxi
username: admin
password: admin
host: localhost
port: 5432
```

After setting up the block, copy or retype the following code from the block to the `.py` file:

```python
from prefect_sqlalchemy import SqlAlchemyConnector

database_block = SqlAlchemyConnector.load("postgres-connector")
with database_block:
    ...
```
# Prefect_Intro Folder 📂
This section explains the `.py` code files and what each does.
The corresponding video: [DE Zoomcamp 2.2 - Introduction to Prefect Concepts](https://youtu.be/cdtN6dhp708?feature=shared)
## python file explanation
- `data_ingest.py`: the original data ingest code without any prefect decorators
- `data_ingest_prefect.py`: original data ingest code with simple `@flow` and `@task` decorators for concept demonstration
- `data_etl.py`: improves upon the `data_ingest_prefect.py` by breaking down the big `main_flow()` function into task components to demonstrate the concept of tasks in Prefect
- `data_etl_blocks.py`: additional code added to the `data_etl.py` to demonstrate the concept of blocks in Prefect. **Pay attention to how the postgres connection engine and function parameter code can be simplified when compare to the data_etl.py.**

# Extraction_AWS Folder 📂
Note that in the original video, GCP was used. Because I personally prefer AWS, so I re-write this whole section to allow the ETL to save the final result to AWS S3 bucket.
The package `prefect-aws` was used.

Another thing to point out is that, although the zoomcamp demonstrated with an "etl", it is in fact not an ETL because the original code does not load the data to a database. Instead, the whole process is actually an **Extraction** process, where original raw data taken from the source is cleaned up a bit, and then saved to a landing zone before the actual transformation takes place. Therefore, instead of naming the folder and file to `etl_`, I named it to `extraction_` to reflect the nature of the code. 

## Creating a AWS Credentials Block in Prefect UI
According to the prefect-aws documentation, an AWS Credentials Block has to be created. This can be done by a script or configured in the Prefect UI. I created mine via the UI, but you can follow the official documentation to create one using a script (see reference link in the Reference section).

## Using Prefect with AWS S3
To be able to follow this section, we will need to create a new bucket for us to save the extracted and cleaned data.
Follow [this section](https://prefecthq.github.io/prefect-aws/#using-prefect-with-aws-s3) of the documentation to add the code.

Note that, unlike the previous section, the code was started from scratch. This means that the `data_ingest.py` code we had from week 1 would not be reused. However, the idea is still the same.

## Uploading DataFrame to Redshift
To be able to do this, the best approach would be using the AWS SDK called [aws-wrangler](https://aws-sdk-pandas.readthedocs.io/en/stable/).
The `/aws_wrangler_tutorial` contains some simple python notebook exercise I did to test out this method before adding it to the actual code.

The following has to be set up to ensure correct connection to Redshift and run the python notebook:
1. Ensure you provision the redshift resource. This can be done by running `terraform apply -target=aws_redshift_cluster.data_set` in week1's terraform folder.
2. After the cluster is created, create a Glue Connection so that you can reference the Glue connection in the `awswranger.connect()`

This [Stackoverflow thread](https://stackoverflow.com/questions/67557052/connect-to-aws-redshift-using-awswrangler) provides very good detail on how this step is done.

**Note: if the provisioned Redshift cluster is destroyed and recreated when you resume your work. You need to double check your connection is configured correctly. You will also need to recreate Glue Connection.**

You will also need to ensure your VPC cluster's security group is configured to allow inbound traffic via port 5439. For simplicity I just allowed all IPv4 and IPv6 inbound flow from anywhere to my Redshift Cluster. If this is not properly set up, you will encounter a timeout when trying to connect to Redshift using the awswrangler.

After you have uploaded data to redshift, make sure you are connecting to the database using username and password. By default, you will be connected via your current IAM user, which you will not see any data coming up. 

# 📚References

- Original source code from the zoomcamp demo can be found [here](https://github.com/discdiver/prefect-zoomcamp)
- Learn about Prefect Blocks [here](https://docs.prefect.io/latest/concepts/blocks/)
## Prefect Reference
- `prefect-aws` [documentation](https://prefecthq.github.io/prefect-aws/)
## AWS SDK `awswrangler` Reference
- awswrangler: Redshift copy and upload [tutorial reference](https://aws-sdk-pandas.readthedocs.io/en/stable/tutorials/008%20-%20Redshift%20-%20Copy%20%26%20Unload.html)
- awswrangler.redshift.to_sql [documentation](https://aws-sdk-pandas.readthedocs.io/en/3.4.2/stubs/awswrangler.redshift.to_sql.html)
- awswrangler.redshift.copy [documentation](https://aws-sdk-pandas.readthedocs.io/en/3.4.2/stubs/awswrangler.redshift.copy.html)
- awswrangler.redshift.connect [documentation](https://aws-sdk-pandas.readthedocs.io/en/3.4.2/stubs/awswrangler.redshift.connect.html)
- Connect to AWS Redshift using awswrangler [Stackoverflow thread](https://stackoverflow.com/questions/67557052/connect-to-aws-redshift-using-awswrangler)
## AWS Official Guide
- [AWS Official Documentation](https://docs.aws.amazon.com/redshift/latest/dg/c_loading-data-best-practices.html) for Loading Data to Redshift
- [Great Redshift tutorial](https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html) from AWS for absolute beginners to learn about loading data from s3 to Redshift
- [AWS tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) on IAM Roles (sharing this here b.c it is better to attach IAM roles to Redshift clusters)
- Overview of Redshift Serverless workgroups and namespaces [official guide](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-workgroup-namespace.html)
## Other References
- [Useful Stackoverflow Thread ](https://stackoverflow.com/questions/71521678/configuring-python-redshift-connector-or-psycopg2-to-connect-with-redshift-ser)explaining timeout when trying to connect to Redshift Serverless workgroup using redshift-connect module. Basically we need to configure the workgroup to be **publicly accessible**
- [Documentation page](https://github.com/aws/amazon-redshift-python-driver/blob/master/tutorials/001%20-%20Connecting%20to%20Amazon%20Redshift.ipynb) for redshift-connector