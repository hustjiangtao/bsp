#!/bin/bash
# deploy for bsp include nginx conf & supervisord conf

# pipenv run /home/jiangtao/bsp/run.py
gunicorn -b 127.0.0.1:5000 app:app
