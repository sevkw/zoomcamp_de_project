FROM prefecthq/prefect:2.14.10-python3.8

ENV PREFECT_API_URL=http://host.docker.internal:4200/api

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY extraction_aws/parameterized_extract_to_s3.py /opt/prefect/flows
COPY extraction_aws/data /opt/prefect/data
