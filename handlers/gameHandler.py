#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class GameHandler:

    exposed = True

    games = []

    def getAllGames(self):
        games = cherrypy.engine.publish('mpong-get-all-games') #.pop()

        return {'games': GameHandler.games}

    def getGame(self, gameId):
        game = cherrypy.engine.publish('mpong-get-game', gameId) #.pop()

        for g in GameHandler.games:
            if g.get('id') == gameId:
                return {'games': [g]}

        raise cherrypy.HTTPError(404, 'No game with id %s found' % gameId)

    @cherrypy.tools.json_out()
    def GET(self, gameId=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401)
        
        if gameId is None:
            return self.getAllGames()
        else:
            return self.getGame(gameId)
    
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameId=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        
        game = cherrypy.request.json
        
        if gameId:
            game['id'] = gameId
        else:
            raise cherrypy.HTTPError(400, 'game id not set')
        
        if 'maxPlayers' not in game:
            raise cherrypy.HTTPError(400, 'game maxPlayers not set')

        for g in GameHandler.games:
            if g.get('id') == game['id']:
                raise cherrypy.HTTPError(400, 'game with id %s already exists' % gameId)
            
        #createdGame = cherrypy.engine.publish('mpong-create-game', game) #.pop()
        
        game['joinedPlayers'] = [str(cherrypy.session.get('name'))]
        game['createdBy'] = str(cherrypy.session.get('name'))
        game['name'] = 'mpong'
        game['gameStarted'] = False
        
        GameHandler.games.append(game)
        masterGame.createGame(game['id'], game['createdBy'], int(game['maxPlayers']))
        cherrypy.session['currentGame'] = game
        
        cherrypy.log("created game %s" % game)
        
        return { 'games': [game] }
    
    @cherrypy.tools.json_out()
    def DELETE(self, gameId):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        
        #removedGame = cherrypy.engine.publish('mpong-remove-game', gameId) #.pop()
        removedGame = None
        
        for g in GameHandler.games:
            if g['id'] == gameId:
                if g['createdBy'] == cherrypy.session.get('name'):
                    removedGame = g
                    GameHandler.games.remove(g)
                    break
                else:
                    raise cherrypy.HTTPError(401, '%s could not remove game created by %s' % (cherrypy.session.get('name'), g['createdBy']))
        
        
        if 'currentGame' in cherrypy.session and removedGame == cherrypy.session['currentGame']:
            cherrypy.session['currentGame'] = None
        
        if removedGame is None:
            raise cherrypy.HTTPError(404, 'could not remove game with id %s' % gameId)
            
        cherrypy.log("removed game %s" % removedGame)
            
        return { 'games': [removedGame] }

