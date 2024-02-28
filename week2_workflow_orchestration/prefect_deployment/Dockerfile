FROM prefecthq/prefect:2.14.10-python3.8

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY . /opt/prefect/flows

CMD ["python", "flows/data_etl.py"]
