#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler

class JoinGameHandler:
    
    exposed = True
    
    def GET(self, gameId):
        
        playerName = cherrypy.session.get('playerName')
        
        game = cherrypy.engine.publish('mpong-get-game', gameId).pop()
        
        if playerName not in game.players:
            raise cherrypy.HTTPError(401, '%s has not joined game %s' % (playerName, gameId))
            
        return "%s has joined game %s" % (playerName, gameId)

    @cherrypy.tools.json_out()
    def POST(self, gameId):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401)
            
        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws. 
        playerName = cherrypy.session.get('name')
        
        #joined = cherrypy.engine.publish('mpong-join-game', gameId, playerName).pop()
        
        for g in GameHandler.games:
            if g['id'] == gameId:
                if len(g['joinedPlayers']) == 2 or playerName in g['joinedPlayers']:
                    raise cherrypy.HTTPError(401, '%s could not join game with id %s' % (playerName, gameId))
                g['joinedPlayers'].append(playerName)
                cherrypy.session.get('currentGame') = g
                break
        else:
            raise cherrypy.HTTPError(404)
        
        return {'games': [g]}


