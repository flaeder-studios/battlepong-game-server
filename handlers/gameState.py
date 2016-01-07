#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class GameState:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, gameId):
        game = cherrypy.engine.publish('mpong-get-game', gameId) #.pop()
        
        if not game:
            raise cherrypy.HTTPError(404, 'Game %s not found' % gameId)

        return game.toDict()
