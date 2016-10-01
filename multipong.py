#!/usr/bin/python

import cherrypy
import os
import json
from multipongApplication import root


def standardErrorMessage(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})

cherrypy.config.update({'error_page.default': standardErrorMessage})
cherrypy.config.update({'log.screen': True,
                        'log.access_file': '',
                        'log.error_file': '',
                        'server.thread_pool': 30,
                        'server.socket_file': '/Users/svedvall/Documents/Programmering/Projects/flaeder-studios/socket'})
cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
cherrypy.quickstart(root, '/', cfgFile)
