from pathlib import Path
import os
import pandas as pd
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
# You will need an AWS account and credentials in order to use prefect-aws
from prefect_aws import AwsCredentials, S3Bucket
from create_table_queries import create_yellow_trips_data

@task(log_prints=True, retries=3)
def download_from_s3(bucket:str, file_name:str) -> Path:
    """
        Download Data from S3 bucket to local path.
    """
    aws_credentials = AwsCredentials.load("aws-credential")
    s3_bucket = S3Bucket(
        bucket_name=bucket,
        aws_credentials=aws_credentials
    )

    s3_path = f"{file_name}.parquet"

    s3_bucket.download_object_to_path(from_path=s3_path, to_path="./data/")

    return Path(f"./data/{s3_path}")


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
def write_redshift():
    """
        Write DataFrame to Redshift.
    """
    
    pass


@flow
def extract_s3_to_redshift():
    """
        Main flow to load data from s3 to Redshift.
    """
    pass