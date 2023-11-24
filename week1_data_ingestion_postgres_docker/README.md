# :artificial_satellite: Week 1 Summary 
Course content Reference [link](https://dezoomcamp.streamlit.app/Week_1_Introduction_&_Prerequisites) from Zoomcamp.

Yellow Taxi data [source here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

- Use Docker container and docker-compose to host postgres and pgadmin
- Use Jupyter notebook when drafting the scripts
- Divide the original data into chunks and load them chunk by chunk

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


# 📚Useful References

- pandas [documentation for IO Tools](https://pandas.pydata.org/pandas-docs/version/0.14.1/io.html#sql-queries)
- docker network create [documentation](https://docs.docker.com/engine/reference/commandline/network_create/)
- [argparse documentation](https://docs.python.org/3/library/argparse.html)