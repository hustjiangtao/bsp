# bsp
Bookmarks Share Plan

This project build for sharing our's Bookmarks,
and Google Chrome Bookmarks will be supported first.

## Directory Structure

- `.venv`: Python Interpreter for pipenv
- `app`: source code for bsp
- `migrations & app.db`: db for sqlite
- `deploy`: deploy config for remote server
- `third`: the third module which modified from pip files
- `tmp`: temporary fold
- `config.py`: config for app
- `run.py`: script for run bsp server
- `tests.py`: test module for bsp server
- `Pipfile & Pipfile.lock`: pipenv requirements
- `LICENSE`: the license file

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
$ pipenv run flask db init
$ pipenv run flask db migrate -m "first migration"
$ pipenv run flask db upgrade
```

- update db

```shell
$ pipenv run flask db migrate -m "update db"
$ pipenv run flask db upgrade
```

- start/restart bsp server

```shell
$ supervisorctl start bsp-server
or
$ supervisorctl restart bsp-server
```