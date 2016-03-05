#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from gameHandler import GameHandler
from mpong.masterGameBuilder import masterGame

class JoinGameHandler:
    
    exposed = True
    
    def GET(self, gameId):
        
        playerName = cherrypy.session.get('name')
        
        game = cherrypy.engine.publish('mpong-get-game', gameId).pop()
            
        return "%s has joined game %s" % (playerName, gameId)

    @cherrypy.tools.json_out()
    def POST(self, gameId):
            
        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws. 
        playerName = cherrypy.session.get('name')
        
        #joined = cherrypy.engine.publish('mpong-join-game', gameId, playerName).pop()
        
        for g in GameHandler.games:
            if g['id'] == gameId:
                g['joinedPlayers'].append(playerName)
                cherrypy.session['currentGame'] = g
                masterGame.join(gameId, playerName)
                break
        
        return {'games': [g]}


