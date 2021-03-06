#!coding=utf-8

import requests
from influxdb import InfluxDBClient
from time import sleep
import logging


def connect(retry=0, retry_wait=1):
    while retry >= 0:
        retry -= 1
        try:
            logging.info('trying connect to influx')
            influx = InfluxDBClient('influxdb')
            
            if len(influx.get_list_database()) == 0:
                influx.create_database("my_db")

            influx.switch_database('my_db')
            return influx

        except requests.exceptions.ConnectionError, err:
            logging.error("conn problem, trying again")
            sleep(retry_wait)
            continue
    raise err

def get_stats(container_id):
    conn = connect()
    Q = ("SELECT  mean(value) FROM /.*/ "
         "WHERE time > now() - 24h AND container = '%s' "
         "GROUP BY time(10m),container")
    Q = Q % container_id
    return conn.query(Q)


def get_containers():
    conn = connect()
    Q = ("select count(value) from memory group by image, container, command")

    ret = {}

    for i in conn.query(Q).keys():
        data = i[1]
        ret.setdefault(data['container'], {})
        ret[data['container']]['image'] = data['image']
        ret[data['container']].setdefault("commands", [])
        ret[data['container']]["commands"].append(data['command'])

    return ret




def record(data):

    common = {
        'tags': {
            'container': data['container']['Id'],
            'image': data['container']['Image'],
            'command' : data['container']['Command']
        },
        'time': data['stats']['read']
    }

    measure_getter = {
        'memory' : lambda x: x['stats']['memory_stats']['max_usage'],
        'rx_bytes' : lambda x: x['stats']['network']['rx_bytes'],
        'tx_bytes' : lambda x: x['stats']['network']['tx_bytes'],
        'cpu' : lambda x: x['stats']['cpu_stats']['cpu_usage']['total_usage']
    }

    influx_data = []

    for measurement in measure_getter:
        tmp = {}
        tmp.update(common)
        tmp['measurement'] = measurement
        tmp['fields'] = {
            'value': measure_getter[measurement](data)
        }
        influx_data.append(tmp)

    from pprint import pformat
    from time import sleep

    # logging.warn(pformat(influx_data))

    conn = connect()
    conn.write_points(influx_data)

