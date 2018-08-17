#!/bin/bash
# deploy for bsp include nginx conf & supervisord conf

cp /home/jiangtao/bsp/deploy/nginx/bsp.conf /etc/nginx/conf.d/bsp.conf
cp /home/jiangtao/bsp/deploy/supervisord/bsp.ini /etc/supervisord.d/bsp.ini
nginx -s reload
supervisorctl update
