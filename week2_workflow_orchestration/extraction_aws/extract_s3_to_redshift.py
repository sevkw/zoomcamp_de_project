from pathlib import Path
import os
import pandas as pd
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
# You will need an AWS account and credentials in order to use prefect-aws
from prefect_aws import AwsCredentials, S3Bucket
# from create_table_queries import create_yellow_trips_data

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
def upload_transformed_df_to_s3(df:pd.DataFrame, file_name:str, bucket:str):
    """
        Uploads the transformed df as a parquet file to s3 bucket's transformed/ path.
    """
    local_path = f"./data/{file_name}.parquet"
    df.to_parquet(local_path, compression="gzip")
    
    #upload from local to s3 bucket
    aws_credentials = AwsCredentials.load("aws-credential")
    s3_bucket = S3Bucket(
        bucket_name=bucket,
        aws_credentials=aws_credentials
    )
    base_path = "transformed"
    s3_bucket.upload_from_path(from_path=local_path, to_path=f"{base_path}/{local_path}")
    
    print(f"Transformed dataframe saved to {local_path} has been uploaded to s3: {bucket}/{base_path}/{local_path}.")


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
    color = "yellow"
    year = 2023
    month = 9
    data_partition_name = f"{color}_tripdata_{year}-{month:02}"
    bucket_name = "datalake-bucket-zoomcamp-2023"

    # path to download the extracted raw from s3
    s3_path = f"data/{color}/{data_partition_name}"
    # running the tasks
    local_path = download_from_s3(bucket_name, s3_path)
    transformed_df = transform_data(local_path)
    upload_transformed_df_to_s3(df=transformed_df, file_name=data_partition_name, bucket=bucket_name)

if __name__ == "__main__":
    extract_s3_to_redshift()
