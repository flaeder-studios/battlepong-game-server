#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class LeaveGameHandler:
    
    expose = True
    
    @cherrypy.tools.json_out()
    def POST(self, gameId):
        
        playerName = cherrypy.session.get('playerName')
        
        game = cherrypy.engine.publish('mpong-leave-game', gameId, playerName).pop()
        
        if game is None:
            raise cherrypy.HTTPError(404, 'No game with id %s found' % gameId)
            
        return game.toDict()

