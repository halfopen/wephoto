#!/usr/bin/env bash
rm db.sqlite3
rm wephoto/migrations/0*
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --username h --email ""

