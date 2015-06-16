#!/usr/bin/env python2
#!coding=utf-8

import click
from flask import Flask, request
import logging

app = Flask(__name__)


@app.route("/container_stat", methods=['GET', 'POST'])
def stat():
    if request.method == 'POST':
        data = request.get_json(force=True)
        logging.warn('data received')
        logging.warn(data)
        return 'ok'
    return "ahn?"

@click.group()
def cli():
    pass


@click.command()
def run():
    
    from influxdb import InfluxDBClient
    import requests
    while True:
        try:
            logging.info('trying connect to influx')
            influx = InfluxDBClient('influxdb')
            ret = influx.query('SHOW databases')
        except requests.exceptions.ConnectionError:
            logging.error("conn problem, trying again")
            continue
        break

    app.run(host='0.0.0.0')

cli.add_command(run)

if __name__ == '__main__':
    cli()
