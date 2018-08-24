# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Run to start server"""


import logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options
from app import create_app


app = create_app()


def main():
    """start tornado app server"""
    options.parse_command_line()
    logging.info('[BSP] bsp is starting...')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


# DEBUG = True
DEBUG = False

if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        main()
