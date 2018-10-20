
# influx

## youtube tutorial
1. enter into influxdb container and download dataset
- curl https://s3-us-west-1.amazonaws.com/noaa.water.database.0.9/NOAA_data.txt > NOAA_data.txt
- curl https://s3.amazonaws.com/noaa.water-database/NOAA_data.txt -o NOAA_data.txt
- head -n 15 NOAA_data.txt

2. enter into CLI and run some commands
- influx -h
- influx
* explore the databases
	- show databases
	- show measurements
	- show tag keys
	- show field keys

	- show servers
		- nodes, clusters
	- show shards
		- replicas

	- show stats
	- show diagnostics

	- show series
		- defines the hardware requirements
* SQL commands
	- use NOAA_water_database
	- SELECT * FROM h2o_quality LIMIT 10
* timestamps
	- precision rfc3339
	- precision h
* format
	- json
		- pretty
	- csv
	- column
* delete db
	- drop database rahul_test_ts_db
* measurements
	- select count(*) from cpu_load_short

## Get the total number measurements and display the number of rows
- `influx -database telegraf -execute "show series" | tail -n +3 | awk -F, '{print $1}' | uniq | wc -l`
