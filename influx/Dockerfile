FROM buildpack-deps:jessie

RUN wget http://influxdb.s3.amazonaws.com/influxdb_0.9.0_amd64.deb
RUN dpkg -i influxdb_0.9.0_amd64.deb

EXPOSE 8083 8086

ENV INFLUX /opt/influxdb/influxd
ENV INFLUX_CFG /opt/influxdb/influx.conf
RUN groupadd -r influx && useradd -r -m -g influx influx

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["influxd"]
