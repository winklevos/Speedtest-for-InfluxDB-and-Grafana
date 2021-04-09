import sys
import time

import speedtest
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests import ConnectTimeout, ConnectionError

from influxspeedtest.common import log
from influxspeedtest.config import config


class InfluxdbSpeedtest():

    def __init__(self):

        self.influx_client = self._get_influx_connection()
        self.speedtest = None

    def _get_influx_connection(self):
        """
        Create an InfluxDB connection and test to make sure it works.
        We test with the get all users command.  If the address is bad it fails
        with a 404.  If the user doesn't have permission it fails with 401
        :return:
        """

        influx = InfluxDBClient(
            config.influx_address,
            config.influx_port,
            database=config.influx_database,
            ssl=config.influx_ssl,
            verify_ssl=config.influx_verify_ssl,
            username=config.influx_user,
            password=config.influx_password,
            timeout=5
        )
        try:
            log.debug('Testing connection to InfluxDb using provided credentials')
            influx.get_list_users()  # TODO - Find better way to test connection and permissions
            log.debug('Successful connection to InfluxDb')
        except (ConnectTimeout, InfluxDBClientError, ConnectionError) as e:
            if isinstance(e, ConnectTimeout):
                log.critical('Unable to connect to InfluxDB at the provided address (%s)', config.influx_address)
            elif e.code == 401:
                log.critical('Unable to connect to InfluxDB with provided credentials')
            else:
                log.critical('Failed to connect to InfluxDB for unknown reason')

            sys.exit(1)

        return influx

    def setup_speedtest(self, servers=None, mode='select'):
        """
        Initializes the Speed Test client with the provided server
        :param server: Int
        :return: None
        """
        speedtest.build_user_agent()

        log.debug('Setting up Speedtest.net client')

        if servers:
            log.info(f"Selecting server {('excluding','from')[mode!='exclude']}: {servers}")

        try:
            self.speedtest = speedtest.Speedtest(secure=config.secure)
        except speedtest.ConfigRetrievalError:
            log.critical('Failed to get speedtest.net configuration.  Aborting')
            sys.exit(1)

        
        servers_in = None
        servers_ex = None

        if mode == 'select':
            servers_in = servers
        else:
            servers_ex = servers

        self.speedtest.get_servers(servers_in,servers_ex)

        # log.debug(self.speedtest.servers)

        if len(self.speedtest.servers) != 1:
            log.debug('Selecting the closest server')
            self.speedtest.get_best_server()

            log.info(f"Selected server {self.speedtest.best['name']} (id:{self.speedtest.best['id']})")

    def send_results(self):
        """
        Formats the payload to send to InfluxDB
        :rtype: None
        """
        result_dict = self.speedtest.results.dict()

        input_points = [
            {
                'measurement': 'speed_test_results',
                'fields': {
                    'download': result_dict['download'],
                    'bytes_received': result_dict['bytes_received'],
                    'upload': result_dict['upload'],
                    'bytes_sent': result_dict['bytes_sent'],
                    'ping': result_dict['ping']
                },
                'tags': {
                    'server': result_dict['server']['id'],
                    'server_name': result_dict['server']['name'],
                    'server_country': result_dict['server']['country'],
                    'server_sponsor': result_dict['server']['sponsor'],
                    'isp': result_dict['client']['isp'],
                    'result_url': result_dict['share']
                }
            }
        ]

        self.write_influx_data(input_points)

    def run_speed_test(self, servers=None, share=False, mode='select'):
        """
        Performs the speed test with the provided server
        :param server: Server to test against
        """
        log.info('Starting Speedtest')
        #ensure previous results are removed
        self.speedtest = None

        try:
            self.setup_speedtest(servers, mode)
        except speedtest.NoMatchedServers:
            log.error(f'No servers matched: {servers}')
            return
        except speedtest.ServersRetrievalError:
            log.critical('Cannot retrieve speedtest.net server list. Aborting')
            return
        except speedtest.InvalidServerIDType:
            log.error(f'{servers} is an invalid server type, must be int')
            return

        log.info('Starting download test')
        self.speedtest.download()
        log.info('Starting upload test')
        self.speedtest.upload()
        

        if(share):
            self.speedtest.results.share()
        
        self.send_results()

        results = self.speedtest.results.dict()
        log.info('Download: %sMbps - Upload: %sMbps - Latency: %sms - Share: %s',
                 round(results['download'] / 1000000, 2),
                 round(results['upload'] / 1000000, 2),
                 results['ping'],
                 results['share']
                 )

    def write_influx_data(self, json_data):
        """
        Writes the provided JSON to the database
        :param json_data:
        :return: None
        """
        log.debug(json_data)

        try:
            self.influx_client.write_points(json_data)
        except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
            if hasattr(e, 'code') and e.code == 404:
                log.error('Database %s Does Not Exist.  Attempting To Create', config.influx_database)
                self.influx_client.create_database(config.influx_database)
                self.influx_client.write_points(json_data)
                return

            log.error('Failed To Write To InfluxDB')
            print(e)

        log.debug('Data written to InfluxDB')

    def run(self):
        
        while True:
            if config.mode != 'all' or not config.servers:
                self.run_speed_test(config.servers, config.share, config.mode)
            
            elif config.mode == 'all' and config.servers:
                for server in config.servers:
                    self.run_speed_test([server], config.share, 'select')
            
            log.info(f'Waiting {config.delay} seconds until next test')
            time.sleep(config.delay)
