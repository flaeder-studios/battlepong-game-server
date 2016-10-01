#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class JoinGameHandler:
    exposed = True

    def __init__(self, players, gameData):
        self.players = players
        self.gameData = gameData

    def GET(self, gameID):
        playerName = cherrypy.session.get('name')
        game = self.players[playerName]['currentGame']
        cherrypy.log("JoinGameHandler: Player %s joined game %s" % (playerName, game))
        return {'games': [game]}

    @cherrypy.tools.json_out()
    def POST(self, gameID):
        # Add player to game. This allows him to pick up a websocket to the game. Return adress to ws.
        try:
            playerName = cherrypy.session.get('name')
            player = self.players[playerName]
            joinGame = self.gameData[gameID]
            if 'currentPlayers' in joinGame.keys():
                joinGame['currentPlayers'].append(player)
            else:
                joinGame['currentPlayers'] = [player]
            player['currentGame'] = joinGame
            return self.GET(gameID)
        except KeyError as e:
            raise cherrypy.HTTPError('No game with id {}'.format(e))
