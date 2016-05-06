#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cherrypy
import json
import handlers
import mpong.controlUnit
from ws4py.websocket import EchoWebSocket

if __name__ == "__main__":
    def handleError():
        cherrypy.response.status = 500
        cherrypy.response.body = ["An error occurred..."]
    
    def standardErrorMessage(status, message, traceback, version):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})
    
    
    class Root:
        _cp_config = {'request.error_response': handleError}
    
    
    root = Root()
    root.game = handlers.GameHandler()
    root.game.method = Root()
    root.game.method.join = handlers.JoinGameHandler()
    root.game.method.leave = handlers.LeaveGameHandler()
    root.game.method.start = handlers.StartHandler()
    root.game.method.quit = handlers.StopHandler()
    root.game.state = handlers.GameState()
    root.game.paddle = handlers.PaddleHandler()
    root.player = handlers.PlayerHandler()
    root.ws = handlers.WebSocketHandler()
    
    cherrypy.config.update({'error_page.default': standardErrorMessage})
    cherrypy.config.update({'log.screen': True,
                            'log.access_file': '',
                            'log.error_file': '',
                            'server.thread_pool': 30,
                            'server.socket_host': "0.0.0.0",
                            'server.socket_port': 8080})
    
    
    
    cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
    cherrypy.quickstart(root, '/', cfgFile)
