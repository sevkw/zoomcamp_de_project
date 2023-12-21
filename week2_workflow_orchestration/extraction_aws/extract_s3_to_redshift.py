from pathlib import Path
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
# You will need an AWS account and credentials in order to use prefect-aws
from prefect_aws import AwsCredentials, S3Bucket
# from create_table_queries import create_yellow_trips_data
import redshift_connector
from create_table_queries import *


load_dotenv('../aws_wrangler_tutorial/.env.aws_credentials')
AWS_REGION = os.getenv('AWS_REGION')
REDSHIFT_DATABASE = os.getenv('REDSHIFT_DATABASE')
AWS_ROLE_ARN_REDSHIFT = os.getenv('AWS_ROLE_ARN_REDSHIFT')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')

# establish Redshift connection
con = redshift_connector.connect(
        iam=True,
        host=REDSHIFT_HOST,
        port=5439,
        database=REDSHIFT_DATABASE,
        is_serverless=True,
        serverless_work_group='zoomcamp-redshift-workgroup',
    )

@task(log_prints=True)
def download_from_s3(bucket:str, file_name:str) -> Path:
    """
        Download Data from S3 bucket to local path.
        Returns the local path where the raw data copy was temporarily saved.
    """
    aws_credentials = AwsCredentials.load("aws-credential")
    s3_bucket = S3Bucket(
        bucket_name=bucket,
        aws_credentials=aws_credentials
    )

    s3_path = f"extracted_raw/{file_name}.parquet"

    local_path = f"{file_name}.parquet"

    print(s3_path, local_path)

    s3_bucket.download_object_to_path(from_path=s3_path, to_path=local_path)

    return Path(f"{local_path}")


@task(log_prints=True, retries=3)
def transform_data(file_path:str) -> pd.DataFrame:
    """
        Cleaning data that contains 0 passengers but has a charge.
    """
    df = pd.read_parquet(path=file_path)
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")

    return df

@task(log_prints=True, retries=3)
def upload_transformed_df_to_s3(df:pd.DataFrame, file_name:str, bucket:str) -> str:
    """
        Uploads the transformed df as a parquet file to s3 bucket's transformed/ path.
    """
    local_path = f"./data/{file_name}.parquet"
    
    df.to_parquet(local_path, compression="gzip", index=False)
    
    #upload from local to s3 bucket
    aws_credentials = AwsCredentials.load("aws-credential")
    s3_bucket = S3Bucket(
        bucket_name=bucket,
        aws_credentials=aws_credentials
    )
    base_path = "transformed"
    upload_to_s3_path = f"{base_path}/data/{file_name}.parquet"
    s3_bucket.upload_from_path(from_path=local_path, to_path=upload_to_s3_path)
        
    print(f"Transformed dataframe saved to {local_path} has been uploaded to s3: {bucket}/{upload_to_s3_path}.")

    return f"{bucket}/{upload_to_s3_path}"


@flow(name="Subflow to Create Redshift Table")
def create_table(create_table_name:str, create_table_sql:str) -> None:
    """
        Execute SQL CREATE TABLE query to create table in Redshift.
    """
    with con.cursor() as cursor:
        cursor.execute(create_table_sql)
        con.commit()
        print(f"Table {create_table_name} has been created in redshift.")
        cursor.execute(f"SELECT COUNT(*) FROM {create_table_name};")
        result = cursor.fetchone()
        print(f"Table {create_table_name} currently contains {result} records.")

@task(log_prints=True, retries=3)
def write_redshift(table_name:str, s3_path:str) -> None:
    """
        Write data from S3 bucket to Redshift table.
    """
    sql_copy_command = f"""
    COPY {table_name}
    FROM '{s3_path}'
    FORMAT PARQUET
    IAM_ROLE '{AWS_ROLE_ARN_REDSHIFT}'
    REGION '{AWS_REGION}';
    """

    with con.cursor() as cursor:
        cursor.execute(sql_copy_command)
        print(f"Data from S3 has been copied over to Redshift database: {REDSHIFT_DATABASE}")
        con.commit()
        cursor.execute("SELECT COUNT(*) FROM trips_data;")
        result = cursor.fetchone()
        print(f"Number of rows in 'trips_data' table: {result}")

    con.close()


@flow
def extract_s3_to_redshift():
    """
        Main flow to load data from s3 to Redshift.
    """
    color = "yellow"
    year = 2023
    month = 9
    data_partition_name = f"{color}_tripdata_{year}-{month:02}"
    bucket_name = "datalake-bucket-zoomcamp-2023"

    # path to download the extracted raw from s3
    s3_path = f"data/{color}/{data_partition_name}"

    redshift_table_name = "trips_data"
    # running the tasks
    local_path = download_from_s3(bucket_name, s3_path)
    transformed_df = transform_data(local_path)
    transformed_s3_path = upload_transformed_df_to_s3(df=transformed_df, file_name=data_partition_name, bucket=bucket_name)
    full_transformed_s3_path = f"s3:{'//'}{transformed_s3_path}"
    # running subflow to create table in Redshift
    create_table(create_table_name=redshift_table_name, create_table_sql=create_yellow_trips_data)

    # running final task to upload data to newly created table
    write_redshift(table_name=redshift_table_name, s3_path=full_transformed_s3_path)

if __name__ == "__main__":
    extract_s3_to_redshift()
