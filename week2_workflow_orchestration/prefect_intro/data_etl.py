import pandas as pd
from sqlalchemy import create_engine
from time import time
import os
# import prefect modules with flow and task decorators
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
# import prefect-sqlalchemy
from prefect_sqlalchemy import SqlAlchemyConnector, DatabaseCredentials

## added a task for data extraction
@task(log_prints=True, retries=3, tags="zoomcamp", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url:str):
    """
    To download data from source.
    """
    file_name = 'yellow_tripdata.parquet'
    parquet_file_path = os.path.join(".", file_name)
    csv_file_path = './yellow_tripdata.csv'
    # download raw data from source
    os.system(f"wget {url} -O {file_name}")
    n_lines = 100000
    raw_data = pd.read_parquet(path=parquet_file_path)
    raw_data.head(n_lines).to_csv(csv_file_path, index=False)
    
    # this chunk loads the whole parquet
    # raw_data.to_csv(csv_file_path, index=False)
    # raw_data = pd.read_parquet(path=parquet_file_path)

    # b.c the number of records is so large, so will only take 20000 lines here
    chunk_size=20000

    # slice the df into smaller chunks
    # although here we only have 100 rows, in the actual data, we have 3M rows
    df_iter = pd.read_csv(csv_file_path, iterator=True, chunksize=chunk_size)
    df = next(df_iter)

    return df


@task(log_prints=True)
def transform_data(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")

    return df

@task(log_prints=True, retries=3)
def ingest_data(df, table_name):
    # the database block copied from the Prefect block section
    # Code below no longer works as there is an issue with pandas.to_sql() and SQLAlchemy
    # database_block = SqlAlchemyConnector.load("postgres-connector")

    # Ensure a DatabaseCredentials Block has been created
    database_block = DatabaseCredentials.load("postgres-credentials")

    # engine_path = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    # create an engine to connect to PostgreSQL database
    # before running this, ensure the PostgreSQL database is up and running in the container
    # engine = create_engine(engine_path)
    # engine.connect()
    # with database_block as engine:
    engine = database_block.get_engine()
        # insert the headers
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
        
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

# subflow demonstration
@flow(name="Subflow", log_prints=True)
def log_subflow(table_name:str):
    print(f"Logging Subflow for {table_name}.")

@flow(name="Ingest Flow")
def main_flow(table_name:str):
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet"

    log_subflow(table_name)
    raw_data = extract_data(url)
    data = transform_data(raw_data)
    ingest_data(data, table_name)

if __name__ == '__main__':
    main_flow(table_name="yellow_taxi")