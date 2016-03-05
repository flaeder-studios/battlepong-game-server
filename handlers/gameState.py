# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame

class GameState:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, gameID):
        return masterGame.gameState(gameID)
        

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, gameID):
        masterGame.startGame(gameID)
        return self.GET(gameID)
