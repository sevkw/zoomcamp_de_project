import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
# import prefect modules with flow and task decorators
from prefect import flow, task

@task(log_prints=True, retries=3)
def ingest_data(user, password, host, port, db, table_name, url):
    file_name = 'yellow_tripdata.parquet'
    parquet_file_path = os.path.join(".", file_name)
    csv_file_path = './yellow_tripdata.csv'
    chunk_size=20000


    engine_path = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    # download raw data from source
    os.system(f"wget {url} -O {file_name}")

    # b.c the number of records is so large, so will only take 20000 lines here
    n_lines = 100000
    raw_data = pd.read_parquet(path=parquet_file_path)
    raw_data.head(n_lines).to_csv(csv_file_path, index=False)
    
    # this chunk loads the whole parquet
    # raw_data = pd.read_parquet(path=parquet_file_path)
    # raw_data.to_csv(csv_file_path, index=False)

    # create an engine to connect to PostgreSQL database
    # before running this, ensure the PostgreSQL database is up and running in the container
    engine = create_engine(engine_path)
    engine.connect()

    # slide the df into smaller chunks
    # although here we only have 100 rows, in the actual data, we have 3M rows
    df_iter = pd.read_csv(csv_file_path, iterator=True, chunksize=chunk_size)
    df = next(df_iter)
    # insert the headers
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    # # code to load data to database in chunks
    # need_data_insert = True

    # while need_data_insert:
    #     try:
    #         t_start = time()
    #         df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    #         t_end = time()
    #         print('Inserted another chunk..., took %.3f seconds' % (t_end - t_start))
            
    #         df = next(df_iter)

    #     except StopIteration:
    #         print(f"All data has been loaded to database: {db} and table_name:{table_name}.")
    #         need_data_insert = False  # Update the flag to exit the loop

@flow(name="Ingest Flow")
def main_flow():
    user = "admin"
    password = "admin"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = "yellow_taxi"
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet"

    ingest_data(user, password, host, port, db, table_name, url)

if __name__ == '__main__':
    main_flow()