# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Run to start server"""


# from app import app

# app.run(debug=True)
# app.run()

import logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options
from app import app


def main():
    options.parse_command_line()
    logging.info('[BSP] bsp is starting...')
    http_server=HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


# DEBUG = True
DEBUG = False

if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        main()
