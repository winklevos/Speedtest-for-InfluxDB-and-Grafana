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
|Server         |Comma sperated list of servers.  Leave blank for auto                                                               |
|Share          |Upload results to speedtest.net and retrieve url                                                                    |
#### LOGGING
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Level          |Set how verbose the console output is                                                           |


## Requirements

[influxdb](https://hub.docker.com/_/influxdb) version 1.8.4 or before

[grafana](https://hub.docker.com/r/grafana/grafana)


## Usage 

**Docker Compose**
*[docker-compose.yml](https://github.com/winklevos/Speedtest-for-InfluxDB-and-Grafana/blob/master/docker-compose.yml) example contains config including these requirements*

download and configure [config.ini](https://github.com/winklevos/Speedtest-for-InfluxDB-and-Grafana/blob/master/config.ini) in the same directory as your docker-compose file  


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
2. Create config.ini `cp config.ini-dist config.ini`
3. Configure `config.ini`
4. `./influxspeedtest.py`