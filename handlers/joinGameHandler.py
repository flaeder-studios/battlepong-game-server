#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class JoinGameHandler:
    
    exposed = True
    
    def POST(self):
        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws. 
        playerName = cherrypy.session.get('playerName')
        
        joined = cherrypy.engine.publish('mpong-join-game', gameId, cherrypy.session.get('name')).pop()
        
        if not joined:
            raise cherrypy.HTTPError(401, '%s could not join game with id %s' % (playerName, gameId))
            
        return game.toDict()

    def GET(self, gameId):
        
        playerName = cherrypy.session.get('playerName')
        
        game = cherrypy.engine.publish('mpong-get-game', gameId).pop()
        
        if playerName not in game.players:
            raise cherrypy.HTTPError(401, '%s has not joined game %s' % (playerName, gameId))
            
        return "%s has joined game %s" % (playerName, gameId)
        