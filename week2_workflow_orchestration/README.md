# 🤖Week2 Summary

## Pre-requests
To be able to run the local python codes and load the data to the postgres database, the docker containers created from Week1 must be up and running. Simply start the two containers from the application or run the following commands **from the week1's folder**:

```bash
docker compose up -d
```

### Terraform from Week1 Can be Used for This Week's Exercise
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

**WARNING**

Note that the block setting above via driver `postgresql+psycopg2` no longer works as running flows using this connect will result in an `AttributeError: 'SQLAlchemyConnector' object has no attribute 'cursor'.`. Referencing [this Stackoverflow discussion](https://stackoverflow.com/questions/75315117/attributeerror-connection-object-has-no-attribute-connect-when-use-df-to-sq), it appears that there is an issue with pandas to_sql(). 

Instead, please set up the block as **DatabaseCredentials** ([docs](https://prefecthq.github.io/prefect-sqlalchemy/credentials/#prefect_sqlalchemy.credentials.DatabaseCredentials)) and then call the [.get_engine() method](https://prefecthq.github.io/prefect-sqlalchemy/credentials/#prefect_sqlalchemy.credentials.DatabaseCredentials.get_engine) as exemplified in `data_etl.py`. You can use the same settings from SQLAlchemy Connector block. After that, your flow should run successfully.

```
Connection Info
postgresql://admin:admin@localhost:5432/ny_taxi
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

Overall the code files are very straight forward:

`-create_table_queries.py`: this is not the code file, but a variable I created to store the CREATE TABLE sql query, which would later be used in the `extract_s3_to_redshift.py`
- `extract_to_aws.py`: this is the code that extracts the original data from the public source and store a copy of the exact source to s3 bucket. In actual practice, your company may have data generated from a source system. You should always make a copy of the original source data and save it (for backup purpose), and then run your transformation based on this copy.
- `parameterized_extract_to_s3.py`: This is the `parameterized version` of `extract_to_aws.py` that demonstrate how you can avoid running the same flow for multiple times by parameterizing some critical variables into the flow code.
- `extract_to_s3_parent_flow-deployment.yaml`: This is the deployment build file based on building the `parameterized_extract_to_s3.py` into a deployment by running `prefect deployment build -n` command.See more explanation on deployment below.
- `extract_s3_to_redshift.py`: this is the code where the source data copy in the s3 is transformed and cleaned up, and then the cleaned-up version is saved to a transformed folder in the data warehouse (AWS Redshift).


## Creating a AWS Credentials Block in Prefect UI
According to the [prefect-aws documentation](https://prefecthq.github.io/prefect-aws/#saving-credentials-to-a-block), an AWS Credentials Block has to be created. This can be done by a script or configured in the Prefect UI. I created mine via the UI, but you can follow the official documentation to create one using a script (see reference link in the Reference section).

## Using Prefect with AWS S3
To be able to follow this section, we will need to create a new bucket for us to save the extracted and cleaned data.
Follow [this section](https://prefecthq.github.io/prefect-aws/#using-prefect-with-aws-s3) of the documentation to add the code.

Note that, unlike the previous section, the code was started from scratch. This means that the `data_ingest.py` code we had from week 1 would not be reused. However, the idea is still the same.

## Deployment in Prefect
Deployment is a server-side concept that allows a flow to be scheduled and triggered through the Prefect API, automatically. (Think about we have to trigger the run in our local machine using cli command, which can be super slow.)
We will need to first configure the deployment and tell Prefect how to behave and run the flows automatically.
Note that multiple deployments are possible for a single flow. For example, with different deployments taking different parameters when run.

To make a flow into a deployment run:
```
prefect deployment build path_to_flow.py:entrypoint_flow(here should be parent flow) -n "Name of the deployment
```

**You can run `prefect deployment build --help` to checkout the tags you could use**

For example, when I deployed the `parameterized_extract_to_s3.py` I ran:

```
prefect deployment build ./parameterized_extract_to_s3.py:extract_to_s3_parent_flow -n "Parameterized Extract to S3"
```

After running the command, a `YAML` file will be created in the same folder. Inside the `yaml` file, the parameters could be updated. In line 11 in the `yaml` file, the `parameter` will take the parameters we have entered in the .py file for running the main flow: 

```
extract_to_s3_parent_flow(months=[6, 7, 8], year=2023, color='yellow')
```

It is entered as key-value pairs as:

```
parameters: {"color": "yellow", "months":[6, 7, 8], "year": 2023}
```

After updating the `yaml` file (and saving it), run `prefect deployment apply` command:

```
prefect deployment apply <name_of_yaml>
```

for example, I ran:

```
prefect deployment apply extract_to_s3_parent_flow-deployment.yaml
```

This command will ensure all the updated metadata saved in the `yaml` file is sent over to the Prefect API. Note that in the Prefect UI Server, you should be able to see the deployment being switched on.

### Prefect Work Pools and Agents
Also note that the command line also returns the following info:

```
To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
```

If the agent is not set up, your flow will not be run if you trigger the deployedment to be run in the UI. Instead this run will be marked as scheduled. You can also check it in the Prefct UI `Work Pools` section.

An agent, according to the Zoomcamp training video, is a `very very lightweight Python process` and it `lives in the execution environment`. (In our case we are running on our local machine)

The agent is pulling things to run from a `Work Pool`. In the deployment settings, you can set which work pool you want to send the runs to. This is great if you want a flow to be run on a certain server or a Cloud deployment.

In the `Work Pool` section, copy over the command from the top of the UI page to start the agent and run it in your terminal:

```
prefect agent start --pool "default-agent-pool"
```

Notice that the flow run was completed very quickly versus you triggering it with your local machine! (You can do Ctrl + C to stope the agent).

## Notification

We should always set up notifications to notify the status of a deployment flow run, especially when it fails!

A notification can be set up in the Prefect UI's `Notification` section. Where it allows you to set up notifications by the Run States. You can also do a Slack webhook to forward the notification to your Slack.
Follow [this Slack guide](https://api.slack.com/messaging/webhooks) to learn how to set up a Slack App to receive notifications using Incoming Webhooks.

## Prefect Flow Schedule
Deployments can be scheduled through Prefect UI or the corresponding YAML file. Read more about Prefect schedules [here](https://docs.prefect.io/latest/concepts/schedules/).

### Scheduling upon Deployment Creation
In the video, the lecturer demonstrated how a schedule could be attached upon building a new deployment via CLI.

```
prefect deployment build ./parameterized_extract_to_s3.py:extract_to_s3_parent_flow -n extract_to_s3_v2 --cron "0 0 * * *" -a 
```
`-a` at the end means to apply the cron configuration immediately

### Scheduling after Deployment Creation
Scheduling can also be set up after a deployment has been built. We use the `set-schedule` command to set the schedule for a given deployment. 

## Running Prefect Flow in Docker Containers

Our flow code can be stored in a Docker image and then uploaded to a Docker hub. A Docker container could be created based on that image, in which our flow code has been stored.

### Creating a Dockerfile

A `Dockerfile` is created in `week2_workflow_orchestration` folder to demonstrate this concept.

The docker file inherits FROM the [prefect image](https://hub.docker.com/r/prefecthq/prefect).


Run `docker image build -t sevkw/prefect:zoomcamp .` to get an image built (while ensure you are still in Week2 folder where the Dockerfile is located).  Note, for the first build, it could take some ⏲️.
To learn more about `docker image build -t` command, check [here](https://docs.docker.com/reference/cli/docker/image/build/#tag).

Once the image is build, you can run `docker images` to view a list of images you have. You should see the image you just built showing up like below:

```
REPOSITORY                   TAG               IMAGE ID       CREATED          SIZE
prefect/zoomcamp             latest            4098e2f8dab7   15 seconds ago   934MB
```

You can push this image to docker hub by running `docker image push <image_name>`, check command reference [here](https://docs.docker.com/reference/cli/docker/image/push/).

### Building a New Prefect Block for Docker Container

We need to build a new prefect block for the docker container we will be creating for our deployment. This can be created via the Prefect server UI Block section. See reference [here](https://docs.prefect.io/latest/guides/docker/).

I named the block as `zoomcamp-prefect-container`.

Under the `Image` section, after ensuring you have pushed your image to Docker hub, you need to drop the name of your image here. For me, I entered `sevkw/prefect:zoomcamp`. After creating the container (following [this video](https://youtu.be/psNSzqTsi-s?feature=shared)) you should have copied the following code to a deploy.py file you would soon create

```
from prefect.infrastructure.container import DockerContainer
docker_container_block = DockerContainer.load("zoomcamp-prefect-container")
```

Then follow the rest of the video to complete the deployment python code and run the deployment on a Docker container. After ensuring you have set the prefect profile to the Prefect server api and the Redshift serverless has been provisioned. You can run the deployment using:

```bash
prefect deployment run extract-to-s3-parent-flow/docker-deployment-flow
```

you can override the pre-existing parameter by adding `-p`

```bash
prefect deployment run extract-to-s3-parent-flow/docker-deployment-flow -p "months=[1,2]"
```

When I ran the command my flow seemed to be Crashed and it was due to Network Connection Error.

[This documentation](https://www.restack.io/docs/prefect-knowledge-prefect-api-connection-error) gives some clue. However, it does not resolve the issue on my end.

# Uploading DataFrame to Redshift
To be able to do this, the best approach would be using the AWS SDK called [aws-wrangler](https://aws-sdk-pandas.readthedocs.io/en/stable/).
The `/aws_wrangler_tutorial` contains some simple python notebook exercise I did to test out this method before adding it to the actual code.

The following has to be set up to ensure correct connection to Redshift and run the python notebook:
1. Ensure you provision the redshift resource. This can be done by running `terraform apply -target=aws_redshift_cluster.data_set` in week1's terraform folder.
2. After the cluster is created, create a Glue Connection so that you can reference the Glue connection in the `awswranger.connect()`

This [Stackoverflow thread](https://stackoverflow.com/questions/67557052/connect-to-aws-redshift-using-awswrangler) provides very good detail on how this step is done.

**Note: if the provisioned Redshift cluster is destroyed and recreated when you resume your work. You need to double check your connection is configured correctly. You will also need to recreate Glue Connection.**

You will also need to ensure your VPC cluster's security group is configured to allow inbound traffic via port 5439. For simplicity I just allowed all IPv4 and IPv6 inbound flow from anywhere to my Redshift Cluster. If this is not properly set up, you will encounter a timeout when trying to connect to Redshift using the awswrangler.

After you have uploaded data to redshift, make sure you are connecting to the database using username and password. By default, you will be connected via your current IAM user, which you will not see any data coming up. 

# 🐎 Recap Quick Notes

In case you return to this week's project folder after idling for a while (like me, coming back after a long trip). You can simply rerun the project in the following steps:

1. You do not need to have docker container started 
2. ensure you run the `terraform apply` command to provision the Redshift Serverless
3. `cd` into the `extraction_aws/` directory and run `python3 parameterized_extract_to_s3.py` to trigger this flow to be run. You should see the flow completed successfully.
4. You can also go to the Prefect Server UI and trigger the deployment to be run, but ensure you have the agent pool running first by running `prefect agent start --pool "default-agent-pool" ` in your terminal. You should see a 🟢 next to your deployed flow and you can trigger the deployment to run now. Below is what you should expect to see:

```
11:50:00.106 | INFO    | Flow run 'overjoyed-mamba' - Finished in state Completed('All states completed.')
11:50:00.187 | INFO    | Flow run 'magic-dormouse' - Finished in state Completed('All states completed.')
11:50:00.955 | INFO    | prefect.infrastructure.process - Process 'magic-dormouse' exited cleanly.
```
5. **Ensure you stop your provisioned service to avoid being charged**. Run the following command in week1's `terraform/` directory:

```
terraform destroy -target=aws_redshiftserverless_namespace.zoomcamp_dataset -target=aws_redshiftserverless_workgroup.zoomcamp_dataset -target=aws_redshiftserverless_usage_limit.zoomcamp_dataset
```
6. Also remember to stop your Prefect server (Ctl+c)

# 📚References

- Original source code from the zoomcamp demo can be found [here](https://github.com/discdiver/prefect-zoomcamp)
- Learn about Prefect Blocks [here](https://docs.prefect.io/latest/concepts/blocks/)
## Prefect Reference
- `prefect-aws` [documentation](https://prefecthq.github.io/prefect-aws/)
- prefect deployment [documentation](https://docs.prefect.io/latest/tutorial/deployments/)
- more on prefect deployment and Work Pools [here](https://docs.prefect.io/latest/guides/prefect-deploy/)
- Prefect [Blog post](https://discourse.prefect.io/t/how-does-the-prefect-deployment-build-and-apply-cli-work-and-how-can-you-customize-it/1456#what-does-prefect-deployment-build-do-1) explaining what does `prefect deployment build` do
- Learn more about Prefect deployment Work Pool and Workers [here](https://docs.prefect.io/latest/concepts/work-pools/)
- Learn more about Prefect [Schedules](https://docs.prefect.io/latest/concepts/schedules/)
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