from pathlib import Path
import pandas as pd
from prefect import flow, task
# You will need an AWS account and credentials in order to use prefect-aws
from prefect_aws import AwsCredentials

aws_credentials_block = AwsCredentials.load("aws-credential")

