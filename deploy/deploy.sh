#!/bin/bash
# deploy for bsp include nginx conf & supervisord conf

cp /home/jiangtao/bsp/deploy/nginx/bsp.conf /etc/nginx/conf.d/bsp.conf
# cp /home/jiangtao/bsp/deploy/supervisord/bsp.ini /etc/supervisord.d/bsp.ini
nginx -s reload
# supervisorctl update
# pipenv run /home/jiangtao/bsp/run.py
gunicorn -b 127.0.0.1:5000 app:app
