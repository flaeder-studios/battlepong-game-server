# -*- coding: utf-8 -*-

import cherrypy
import mpong

class GameState:

    exposed = True
    states = {}

    @cherrypy.tools.json_out()
    def GET(self, gameId):
        game = cherrypy.engine.publish('mpong-get-game', gameId) #.pop()
        
        if not game:
            raise cherrypy.HTTPError(404, 'Game %s not found' % (gameId))

        return game.toDict()

    @cherrypy.tools.json_out()
    def POST(self):
        stateIn = cherrypy.request.json()
        currentGame = cherrypy.session['currentGame']
        gameState = GameState.states.get(currentGame['id'], False)
        if not gameState:
            joinedPlayers = currentGame['joinedPlayers']
            states[currentGame['id']] = Game(100, joinedPlayers[0], joinedPlayers[1], 3)

        # TODO change state of game
