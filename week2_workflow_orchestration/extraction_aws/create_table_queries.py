# This file contains SQL queries to be imported to prefect flow files to create table in redshift before loading data.
create_yellow_trips_data = """
CREATE TABLE IF NOT EXISTS trips_data (
"VendorID" BIGINT, 
tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE, 
tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE, 
passenger_count FLOAT(53), 
trip_distance FLOAT(53), 
"RatecodeID" FLOAT(53), 
store_and_fwd_flag TEXT, 
"PULocationID" BIGINT, 
"DOLocationID" BIGINT, 
payment_type BIGINT, 
fare_amount FLOAT(53), 
extra FLOAT(53), 
mta_tax FLOAT(53), 
tip_amount FLOAT(53), 
tolls_amount FLOAT(53), 
improvement_surcharge FLOAT(53), 
total_amount FLOAT(53), 
congestion_surcharge FLOAT(53), 
airport_fee FLOAT(53)
)
"""