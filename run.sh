#!/bin/bash

STATIONLOG_HOME="$(pwd)"
VENV_HOME="${STATIONLOG_HOME}/venv"

PATH="${VENV_HOME}/bin:${PATH}"

python3 \
    ./odoo/odoo-bin \
    --addons-path=odoo/odoo/addons,odoo/addons,web,server-ux,hnt-tools,hamutility,stationlog,repeaters \
    --db_host=127.0.0.1 \
    --db_port=5432 \
    --db_user=stationlog \
    --db_password=stationlog \
    --database=stationlog \
    --db-filter=stationlog \
    --http-port=8069
