# 🤖Week2 Summary

## Pre-requests
To be able to run the local python codes and load the data to the postgres database, the docker containers created from Week1 must be up and running. Simply start the two containers from the application or run the following commands **from the week1's folder**:

```bash
docker compose up -d
```

## Prefect Tutorial
I personally felt a bit nervous when just learning about Prefect from scratch through the zoomcamp. Therefore, before I started, I studied the basic concepts via Prefect's guide. I highly recommend following the official website to learn the basic, because the zoomcamp contents will make more sense afterwards.

- Learn Prefect basic [from here](https://docs.prefect.io/latest/getting-started/quickstart/)
- After the Prefect Quickstart, also follow [the Tutorials section](https://docs.prefect.io/latest/tutorial/)

# 📹Intro to Prefect Concepts
Note that the starting code from the original repo and the demo video looks slightly different from the week 1 python code for data ingest. The different part was in the part where argparse was used to allow users to define parameters via cli when running thr commands below:

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

Instead, the starting file had the `main()` function taking the inputs as variables. The `data_ingest.py` in this week starts from here.
The `data_ingest_prefect.py` is the version with prefect module.

## 🏃Running Prefect Flow
The video seems to not demonstrate that, before running a prefect flow, the self-hosted prefect server (for the UI) should be started. After adjusting the data_ingest.py with `@flow` and `@task` decorators, please ensure you run:
```bash
prefect server start
```
After running, you should be able to open the self-hosted Prefect UI via your [local host](http://127.0.0.1:4200).
Note that once this is run, the terminal will be listening to the API, so please start a new terminal to run new commands there. In the new terminal window, run:

```bash
python data_ingest_prefect.py
```
After that you should be able to see this flow being completed in the self-hosted UI.

## python file explanation
- `data_ingest.py`: the original data ingest code without any prefect decorators
- `data_ingest_prefect.py`: original data ingest code with simple `@flow` and `@task` decorators for concept demonstration
- `data_etl.py`: improves upon the `data_ingest_prefect.py` by breaking down the big `main_flow()` function into task components to demonstrate the concept of tasks in Prefect



# 📚References

- Original source code from the zoomcamp demo can be found [here](https://github.com/discdiver/prefect-zoomcamp)