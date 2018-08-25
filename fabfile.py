# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""deploy with fabric"""


import os
from dotenv import load_dotenv
from fabric.api import env, run, cd


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
env.hosts = os.environ.get('DEPLOY_HOST')
env.user = os.environ.get('DEPLOY_USER')
basedir = os.environ.get('DEPLOY_DIR')


def sync():
    with cd(basedir):
        run('git fetch;git pull')


def restart():
    run('supervisorctl restart bsp-server')


def deploy():
    sync()
    restart()
