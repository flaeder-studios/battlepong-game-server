#!/Users/svedvall/Documents/Programmering/Projects/flaeder-studios/battlepong-game-server/venv/bin/python

import cherrypy
import os
import json
from multipongApplication import root


def standardErrorMessage(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})

cherrypy.config.update({'error_page.default': standardErrorMessage})
#cherrypy.config.update({'log.screen': True,
#                        'log.access_file': '',
#                        'log.error_file': '',
#                        'server.thread_pool': 30,
#                        'server.socket_file': '/Users/svedvall/Documents/Programmering/Projects/flaeder-studios/socket'})
cherrypy.config.update({'log.screen': True,
                        'log.access_file': '',
                        'log.error_file': '',
                        'server.socket_host': '127.0.0.1',
                        'tools.encode.on': True,
                        'tools.encode.encoding': 'utf-8',
                        'server.socket_port': 8080,
                        'server.thread_pool': 30})
cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
cherrypy.quickstart(root, '/', cfgFile)
