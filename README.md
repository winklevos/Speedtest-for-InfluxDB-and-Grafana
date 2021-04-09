**Speedtest.net Collector For InfluxDB and Grafana**
------------------------------

![Screenshot](https://raw.githubusercontent.com/winklevos/Speedtest-for-InfluxDB-and-Grafana/master/dashboard-screenshot.PNG)

This tool is a wrapper for speedtest-cli which allows you to run periodic speedtets and save the results to Influxdb

## Configuration within config.ini

#### GENERAL
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Delay          |Seconds between speedtests (default 30 min)                                                                         |
#### INFLUXDB
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Address        |InfluxDB host or container name                                                                                     |
|Port           |InfluxDB port default 8086                                                                                          |
|Database       |Database to write collected stats to                                                                                |
|Username       |User that has access to the database                                                                                |
|Password       |Password for above user                                                                                             |
#### SPEEDTEST
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Servers        |Comma sperated list of servers 0001,0002.  Leave blank for auto                                    |
|Mode           |How list is treated, all - runs speedtest on all servers, select - selects best server from list, exclude - ensure listed servers are not used |
|Share          |Upload results to speedtest.net and retrieve url                                                   |
|Secure         |Runs speedtest over HTTPS                                                                          |
#### LOGGING
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Level          |Set how verbose the console output is                                                           |


## Requirements

[influxdb](https://hub.docker.com/_/influxdb) version 1.8.4 or before

[grafana](https://hub.docker.com/r/grafana/grafana)


## Usage 

**Docker Compose**
*[docker-compose.yml](https://raw.githubusercontent.com/winklevos/Speedtest-for-InfluxDB-and-Grafana/master/docker-compose.yml) example contains config including these requirements*

download and configure [config.ini](https://raw.githubusercontent.com/winklevos/Speedtest-for-InfluxDB-and-Grafana/master/config.ini-dist) in the same directory as your docker-compose file  


**Manual**
```docker run -d \
--name="speedtest" \
-v config.ini:/src/config.ini \
--restart="unless-stopped" \
winklevos/speedtest-for-influxdb-and-grafana
```

## Direct Python use or development

0. Clone repo https://github.com/winklevos/Speedtest-for-InfluxDB-and-Grafana.git
1. Install required Python modules `pip install -r requirements.txt`
2. Create config.ini `cp config.ini-dist config.ini` or rename if not developing
3. Configure `config.ini`
4. `./influxspeedtest.py`