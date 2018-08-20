# bsp
Bookmarks Share Plan

This project build for sharing our's Bookmarks,
and Google Chrome Bookmarks will be supported first.

## Directory Structure

- `.venv`: Python Interpreter for pipenv
- `app`: source code for bsp
- `db_repository & app.db`: db for sqlite
- `deploy`: deploy config for remote server
- `third`: the third module which modified from pip files
- `tmp`: temporary fold
- `whoosh_index`: whoosh full text search
- `config.py`: config for app
- `db_create.py`: script for creating sqlite tables
- `db_migrate.py`: script for migrating sqlite tables
- `db_upgrade.py`: script for upgrading sqlite tables
- `db_downgrade.py`: script for downgrading sqlite tables
- `Pipfile & Pipfile.lock`: pipenv requirements
- `run.py`: script for run bsp server
- `tests.py`: test module for bsp server

## Run this server

```shell
$ pipenv run python run.py
```

## Deploy for remote server

- Git sync for local & remote
- execute ./deploy/deploy.sh to update nginx conf & supervisord conf

```shell
$ cd $PATH_FOR_BSP
$ git fetch
$ git pull
$ . ./deploy/deploy.sh
```

- create db

```shell
$ pipenv run python db_create.py
```

- start/restart bsp server

```shell
$ supervisorctl start bsp-server
or
$ supervisorctl restart bsp-server
```