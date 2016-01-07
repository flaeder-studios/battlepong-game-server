#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class GameHandler:
    
    exposed = True
    
    def getAllGames(self):
        games = cherrypy.engine.publish('mpong-get-all-games') #.pop()
        
        uris = []
        for g in uris:
            uris.append({'uri': '/game/%s' % g.id })
            
        return { 'games': uris }
    
    def getGame(self, gameId):
        game = cherrypy.engine.publish('mpong-get-game', gameId) #.pop()
        
        if not game:
            raise cherrypy.HTTPError(404, 'No game with id %s found' % gameId)
            
        return game.toDict()
    
    @cherrypy.tools.json_out()
    def GET(self, gameId=None):
        if gameId is None:
            return self.getAllGames()
        else:
            return self.getGame(gameId)
    
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameId):
        game = cherrypy.engine.publish('mpong-create-game', gameId) #.pop()
        
        if game is None:
            raise cherrypy.HTTPError(404, 'Could not create game with id %s' % gameId)
            
        return game.toDict()
    
    @cherrypy.tools.json_out()
    def DELETE(self, gameId):
        game = cherrypy.engine.publish('mpong-remove-game', gameId) #.pop()
        
        if game is None:
            raise cherrypy.HTTPError(404, 'Could not remove game with id %s' % gameId)
            
        return game.toDict()

