#!/usr/bin/env python2
#!coding=utf-8

import click
from flask import Flask, request
import logging
from model import connect, record

app = Flask(__name__)


@app.route("/container_stat", methods=['GET', 'POST'])
def stat():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # logging.warn('data received')
        # logging.warn(data)
        record(data)
        return 'ok'
    return "ahn?"

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
