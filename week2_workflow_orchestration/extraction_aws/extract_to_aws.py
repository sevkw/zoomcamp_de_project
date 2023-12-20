from pathlib import Path
import os
import pandas as pd
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
# You will need an AWS account and credentials in order to use prefect-aws
from prefect_aws import AwsCredentials, S3Bucket



@task(log_prints=True, retries=3, tags="zoomcamp", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url:str) -> pd.DataFrame:
    """
    To read taxi data from url into pandas DataFrame
    """
    file_name = 'yellow_tripdata.parquet'
    parquet_file_path = os.path.join(".", file_name)
    # download raw data from source
    os.system(f"wget {url} -O {file_name}")
    # reduce the data size to save resource
    # because the original file contains too many records
    n_lines = 100000
    # read data to a pandas DataFrame
    raw_data_df = pd.read_parquet(path=parquet_file_path).head(n_lines)

    return raw_data_df


@task(log_prints=True, retries=3)
def write_local(df:pd.DataFrame, color:str, dataset_file:str) -> Path:
    """
        Write DataFrame out locally as compressed parquet file.
    """
    path = Path(f"./data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")

    return path


@task(log_prints=True, retries=3)
def write_to_s3(path:Path, bucket: str) -> None:
    """
        Upload local parquet file to AWS S3.
    """
    aws_credentials = AwsCredentials.load("aws-credential")
    s3_bucket = S3Bucket(
        bucket_name=bucket,
        aws_credentials=aws_credentials
    )
    base_path = "extracted_raw"
    s3_bucket.upload_from_path(from_path=path, to_path=f"{base_path}/{path}")

    print(f"File from path {path} has been uploaded to bucket: {bucket}.")


@flow
def extract_data_to_s3() -> None:
    """
        The main flow function that extracts raw data from original source and save the cleaned data to AWS S3 bucket.
        The AWS S3 bucket to save the data is called datalake-bucket-zoomcamp-2023, this is provisioned by Terraform.
        Ensure that the s3 bucket has been provisioned by running:
        terraform apply -target=aws_s3_bucket.data-lake-bucket -target=aws_s3_bucket_versioning.datalake_versioning -target=aws_s3_bucket_lifecycle_configuration.datalake-lifecycle
    """
    color = "yellow"
    year = 2023
    month = 9
    data_partition_name = f"{color}_tripdata_{year}-{month:02}"
    data_source_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{data_partition_name}.parquet"
    bucket_name = "datalake-bucket-zoomcamp-2023"
    raw_df = extract_data(data_source_url)
    local_path = write_local(raw_df, color, data_partition_name)
    write_to_s3(local_path, bucket=f"{bucket_name}")

if __name__ == "__main__":
    extract_data_to_s3()