FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet

WORKDIR /app

COPY data_ingest.py data_ingest.py

ENTRYPOINT [ "python", "data_ingest.py" ]