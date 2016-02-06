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
        creatorName = str(cherrypy.session['name'])
        gameState = GameState.states.get(creatorName, False)
        if not gameState:
            for g in GameHandler.games:
                if g['createdBy'] == creatorName:
                    joinedPlayers = g['joinedPlayers']
                    if not len(joinedPlayers) == 2:
                        raise cherrypy.HTTPError(404, 'To few players' )
                    states[creatorName] = Game(100, joinedPlayers[0], joinedPlayers[1], 3)
                    break
            else:
                raise cherrypy.HTTPError(404, 'Game %s not found' % (creatorName))

        # TODO change state of game
