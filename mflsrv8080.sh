#!/bin/sh

sh +x ./CLEANUP
pip install -r requirements.txt

export FLASK_APP=mflsrv
export FLASK_ENV=development
flask init-db
flask run --host=0.0.0.0 --port=8080
