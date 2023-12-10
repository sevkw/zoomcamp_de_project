# :artificial_satellite: Week 1 Summary 
Course content Reference [link](https://dezoomcamp.streamlit.app/Week_1_Introduction_&_Prerequisites) from Zoomcamp.

Yellow Taxi data [source here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

- Use Docker container and docker-compose to host postgres and pgadmin
- Use Jupyter notebook when drafting the scripts
- Divide the original data into chunks and load them chunk by chunk
  
## ⛈️Cloud Services
**Note:** For this project, I would use AWS services instead of GCP, because I'm more familiar with AWS service, and AWS's SDK client is more developed than that of GCP.

**AWS Equivalents**
- Data Lake: S3
- Data Warehouse: Redshift
  
### 👨‍💻AWS Setups
- Set up a new IAM user and grant FullAccess to Redshift and S3 bucket
- You can continue using your existing IAM user, but just need to ensure the correct policies are attached
- The only difference for GCP is that GCP manages services by projects, and the services accounts created are available under the context of that project. Therefore, each service account is unique in each project.

## 🌮Terraform

I personally find the Zoomcamp video very hard to follow (just not my style), so I consulted other resources online to learn about Terraform.
I find [this video](https://youtu.be/l5k1ai_GBDE?feature=shared) to be a very good resource to get the general idea of the tool.
[This video](https://youtu.be/7xngnjfIlK4?feature=shared) is another comprehensive one (2hrs) for deep dives as it offers multiple demos.
[This link](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) contains all steps to download Terraform to local machine. You can also follow the Ubuntu section when downloading it to EC2 VM.


# 💖Docker Container Warning

Do not remove the containers when you are done because all the data will be lost, as the Postgres database data is saved in the container as there is no volume mounted to the containers. Only remove the containers only you are sure that you never need to reuse those data.
  
# 🏗️Content Structure Explained

## 📂./script_drafts

The `script_drafts` folder contains all the contents used when drafting the scripts to insert data. Before working with the Python Notebook, the docker containers configured in the `docker-compose.yaml` should be run (assume you have `cd`ed into the week_1 folder):

`docker compose up -d`


If all work has been done, the docker containers should be stopped, by running:

`docker compose stop`

[This Stack Overflow thread](https://stackoverflow.com/questions/46428420/docker-compose-up-down-stop-start-difference) discusses the difference between different `docker compose` commands.

## 🐍data_ingest.py
The `data_ingest.py` contains the finished script that ingests the raw data to the Postgres Database.
Note that, because the original data is still too large, so I limited to number of rows to 100,000, which is loaded to the database in chunks at 20,000 rows each.
Run the following commands to run the script from the terminal:

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
## 🐳Dockerfile
The Dockerfile configures the python image, with all dependencies installed, to be able to run the `data_ingest.py`.

When building the image ensure the following:

1. The containers configured in the `docker-compose.yaml` file should be up and running in detach mode.

    ```bash
    docker compose up -d
    ```
2. If it is the first time running the docker container to run the `data_ingest.py`, the following command must be run to build the image:

    ```bash
    docker build -t ingest_taxi_data:ingest .
    ```
    Note that whenever changes are made to the `Dockerfile`, the build command must be run to reflect the updates.

3. Run the python script with the arguments using the following:
    ```bash
    docker run -it \
    --network=week1_data_ingestion_postgres_docker_default \
    ingest_taxi_data:ingest \
    --user=admin \
    --password=admin \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table-name=yellow_taxi \
    --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet
    ```
# ☁️Launching AWS Instances to Run This Week's Exercise in the Cloud
The VM instance exercise is launched using EC2 instance. The idea is basically the same as how GCP instance is set up.
In the video, a Ubuntu image is used with 4GPU and 16GB memory. When setting up a new instance in AWS EC2, we can select the Ubuntu AMI image from the Free tier. However, for computing power, I would recommend using at least t2.small or match the computing power to what the video had (I personally think it is a bit too large, so I used a t2.small).
Ensure the `.pem` key pair is downloaded and saved in the project's directory so that you can SSH into the VM.

## ⚙️Configure EC2 VM
I ran the following commands in the virtual machine. Note that I did not use anaconda, instead, I used python virtual environment and pip installed the libraries.
```bash
sudo apt update -y
sudo apt install python3-pip -y
sudo apt install python3.10-venv -y
sudo apt-get install libpq-dev -y
sudo apt install awscli -y
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
pip install sqlalchemy
```
- install docker by referencing [this link](https://docs.docker.com/engine/install/ubuntu/)
- run `sudo apt install docker-compose -y`
- on the EC2 terminal, clone this repo or if you have a version of the code base, you can clone from your own repo as well.

## 🧰Remote Host Configuration

To be able to connect to the host VM via VS Code, below is the configuration:

```markdown
Host <name-of-instance>
    HostName <public-ip-address-of-ec2-instance>
    User ubuntu
    IdentityFile <full-path-to-the-key-pair-file>.pem
```
🔴**Note**: the `HostName` will have to be updated is the instance is being stopped and restarted.

## 🏃Try Running Docker on EC2 Instance
- `cd` into the week1 folder that contains the `docker-compose.yaml` file
- build the image first
- then run the container in detach mode
- once ensuring the containers are up and running, run `data-ingest.py` using the commands above.
- ensure you also forward ports to allow accessing the PgAdmin UI from localhost, see reference below

## 🏗️Install Terraform on EC2 VM and Run Terraform Commands
- follow the reference in the Terraform section above to install
- go into the terraform folder and run the corresponding terraform commands to initialize backends and other AWS services (just like how it's down on the local machine!)
- 🚫Note: you must again configure your AWS credentials by running `aws configure` in the EC2 terminal
- ⚠️WARNING: if you have done the Terraform exercise on local machine you should not go into the Back end folder and initialize terraform again, assume you did not destroy the provinsioned S3 bucket and DynamoDB table in local machine exercise. So you can just initialize the terraform in the `/terraform` folder and run the data services!

# 📚Useful References

- pandas [documentation for IO Tools](https://pandas.pydata.org/pandas-docs/version/0.14.1/io.html#sql-queries)
- docker network create [documentation](https://docs.docker.com/engine/reference/commandline/network_create/)
- [argparse documentation](https://docs.python.org/3/library/argparse.html)
- list the docker networks [documentation](https://docs.docker.com/engine/reference/commandline/network_ls/)
- docker build command [documentation](https://docs.docker.com/engine/reference/commandline/build/)
- [this section of the zoomcamp video](https://youtu.be/ae-CV2KfoN0?feature=shared&t=1282) trouble shoots the issue when running `docker run` in the ec2 terminal; and here is [the docker reference](https://docs.docker.com/engine/install/linux-postinstall/) to run docker commands without `sudo`
- Forward port to local machine on VS Code [reference](https://code.visualstudio.com/docs/editor/port-forwarding#:~:text=How%20to%20use%20local%20port%20forwarding,-First%2C%20you%20need&text=Then%2C%20navigate%20to%20the%20Ports,above%20command%20is%20port%203000.), and it was explained in [this part of the zoomcamp video](https://youtu.be/ae-CV2KfoN0?feature=shared)