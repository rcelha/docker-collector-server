#!/usr/bin/env python2
#!coding=utf-8

import json
import click
from flask import Flask, request, render_template
import logging
from model import connect, record, get_containers, get_stats
from pprint import pprint, pformat

app = Flask(__name__)


@app.route("/container_stat", methods=['GET', 'POST'])
def stat():
    logging.error("foo")
    if request.method == 'POST':
        data = request.get_json(force=True)
        record(data)
        return 'ok'
    else:
        ret = {}
        containers = get_containers()
        return render_template('index.html', data=ret, containers=containers)

@app.route("/container_stat/<container_id>", methods=['GET'])
def ones_stat(container_id):
    ret = get_stats(container_id)
    return render_template('ones_stat.html', data=ret)

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
