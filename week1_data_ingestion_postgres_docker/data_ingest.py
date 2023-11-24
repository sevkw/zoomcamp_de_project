import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
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

    # code to load data to database in chunks
    need_data_insert = True

    while need_data_insert:
        try:
            t_start = time()
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

            t_end = time()
            print('Inserted another chunk..., took %.3f seconds' % (t_end - t_start))
            
            df = next(df_iter)

        except StopIteration:
            print(f"All data has been loaded to database: {db} and table_name:{table_name}.")
            need_data_insert = False  # Update the flag to exit the loop

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest taxi data into Postgres database.')

    parser.add_argument('--user', help='User name for Postgres.')
    parser.add_argument('--password', help='Password for Postgres.')
    parser.add_argument('--host', help='Host for Postgres.')
    parser.add_argument('--port', help='Port for Postgres.')
    parser.add_argument('--db', help='Database name for Postgres.')
    parser.add_argument('--table-name', help='The name of the table to load data to.')
    parser.add_argument('--url', help='URL of raw data.')

    args = parser.parse_args()
    
    # parser will pass arguments to the main function
    main(args)