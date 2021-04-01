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

<!-- ## Direct Usage

Before the first use run pip3 install -r requirements.txt

Enter your desired information in config.ini 

Run influxspeedtest.py -->

<!-- **Custom Config File Name**

If you wish to use a config file by a different name set an ENV Variable called influxspeedtest.  The value you set will be the config file that's used. 
   -->

<!-- ***Requirements***

Python 3+

You will need the influxdb library installed to use this - [Found Here](https://github.com/influxdata/influxdb-python)
You will need the speedtest-cli library installed to use this - [Found Here](https://github.com/sivel/speedtest-cli) -->

<!-- ## Docker Setup

1. Install [Docker](https://www.docker.com/)

2. Make a directory to hold the config.ini file. Navigate to that directory and download the sample config.ini in this repo.
```bash
mkdir speedtest
curl -O https://raw.githubusercontent.com/barrycarey/Speedtest-for-InfluxDB-and-Grafana/master/config.ini speedtest/config.ini
cd speedtest
```

3. Modify the config file with your influxdb settings.
```bash
nano config.ini
```
Modify the 'Address =' line include the ip or hostname of your influxdb instance.
Example:
```bash
Address = 10.13.14.200
```

4. Run the container, pointing to the directory with the config file. This should now pull the image from Docker hub. You can do this by either running docker run or by using docker-compose.
 1. The docker run option.
```bash
docker run -d \
--name="speedtest" \
-v config.ini:/src/config.ini \
--restart="always" \
atribe/speedtest-for-influxdb-and-grafana
```
 2. The docker-compose option
 ```bash
 curl -O https://raw.githubusercontent.com/barrycarey/Speedtest-for-InfluxDB-and-Grafana/master/docker-compose.yml docker-compose.yml
 docker-compose up -d
 ``` -->
