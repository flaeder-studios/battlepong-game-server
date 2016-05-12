#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cherrypy
import json
from multipongApplication import root
from ws4py.websocket import EchoWebSocket


if __name__ == "__main__":
    def standardErrorMessage(status, message, traceback, version):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})

    cherrypy.config.update({'error_page.default': standardErrorMessage})
    cherrypy.config.update({'log.screen': True,
                            'log.access_file': '',
                            'log.error_file': '',
                            'server.thread_pool': 30,
                            'server.socket_host': "0.0.0.0",
                            'server.socket_port': 8080})
    cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
    cherrypy.quickstart(root, '/', cfgFile)
