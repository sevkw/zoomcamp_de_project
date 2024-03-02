FROM prefecthq/prefect:2.14.10-python3.8

ADD ./extraction_aws/parameterized_extract_to_s3_docker.py /opt/prefect/flows/
ADD ./extraction_aws/data /opt/prefect/data/

COPY docker-requirements.txt /tmp/
RUN pip install -r /tmp/docker-requirements.txt --no-cache-dir

ENV PREFECT_API_URL=<your-prefect-api-url>
ENV PREFECT_API_KEY=<your-prefectAPI-key>
