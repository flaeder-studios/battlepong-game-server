#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class GameHandler:

    exposed = True


    def getAllGames(self):
        games = cherrypy.engine.publish('mpong-get-all-games') #.pop()

        return {'games': masterGame.getMetadataAll()}

    def getGame(self, gameID):
        game = cherrypy.engine.publish('mpong-get-game', gameID) #.pop()

        return {'games': [ masterGame.getMetadata(gameID)]}

    @cherrypy.tools.json_out()
    def GET(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401)

        if gameID is None:
            return self.getAllGames()
        else:
            return self.getGame(gameID)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, gameID=None):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        playerName = cherrypy.session.get('name')

        game = cherrypy.request.json
        if 'id' not in game:
            if gameID:
                game[u'id'] = str(gameID)
            else:
                raise cherrypy.HTTPError(400, 'game id not set')
        if u'maxPlayers' not in game:
            raise cherrypy.HTTPError(400, 'game maxPlayers not set')
        game[u'maxPlayers'] = int(game[u'maxPlayers'])

        masterGame.createGame(game['id'], int(game['maxPlayers']), playerName)
        cherrypy.session['currentGame'] = masterGame.getMetadata(game['id'])

        game = masterGame.getMetadata(gameID)
        cherrypy.log("GameHandler: created game %s" % game)
        return {'games': [game]}

    @cherrypy.tools.json_out()
    def DELETE(self, gameID):
        if not cherrypy.session.get('name'):
            raise cherrypy.HTTPError(401, 'name not set')
        
        #removedGame = cherrypy.engine.publish('mpong-remove-game', gameID) #.pop()
        removedGame = masterGame.deleteGame(gameID)
        return { 'games': [removedGame] }

