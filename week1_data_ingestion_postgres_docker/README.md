# :artificial_satellite: Week 1 Summary 
Course content Reference [link](https://dezoomcamp.streamlit.app/Week_1_Introduction_&_Prerequisites) from Zoomcamp.

Yellow Taxi data [source here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

- Use Docker container and docker-compose to host postgres and pgadmin
- Use Jupyter notebook when drafting the scripts
- Divide the original data into chunks and load them chunk by chunk
  
# 🏗️Content Structure Explained

The `script_drafts` folder contains all the contents used when drafting the scripts to insert data. Before working with the Python Notebook, the docker containers configured in the `docker-compose.yaml` should be run:

`docker compose up -d`

If all work has been done, the docker containers should be stopped, by running:

`docker compose stop -d`

[This Stack Overflow thread](https://stackoverflow.com/questions/46428420/docker-compose-up-down-stop-start-difference) discusses the difference between different `docker compose` commands.

# Useful References

- pandas [documentation for IO Tools](https://pandas.pydata.org/pandas-docs/version/0.14.1/io.html#sql-queries)
- docker network create [documentation](https://docs.docker.com/engine/reference/commandline/network_create/)