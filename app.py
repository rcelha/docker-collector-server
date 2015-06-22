#!/usr/bin/env python2
#!coding=utf-8

import json
import click
from flask import Flask, request, render_template
import logging
from model import connect, record
from pprint import pprint, pformat

app = Flask(__name__)


@app.route("/container_stat", methods=['GET', 'POST'])
def stat():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # logging.warn('data received')
        # logging.warn(data)
        record(data)
        return 'ok'
    else:

        ret = {}

        conn = connect()
        conn.switch_database('my_db')
        Q = ("SELECT "
             "  mean(value) "
             "FROM memory  "
             "WHERE "
             "  time > now() - 24h "
             "GROUP BY time(5m),container")
        result = conn.query(Q)
        for k, v in result.items():
            measurement = k[0]
            container_id = k[1]['container']
            ret.setdefault(container_id, {})
            ret[container_id].setdefault(measurement, {
                'labels': [],
                'values': []
            })
            for i in v:
                ret[container_id][measurement]['labels'].append(i['time'])
                ret[container_id][measurement]['values'].append(i['mean'])
        return render_template('index.html', data=ret)
@click.group()
def cli():
    pass


@click.command()
def run():
    app.run(host='0.0.0.0',
            debug=True)

cli.add_command(run)

if __name__ == '__main__':
    cli()
