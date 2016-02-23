# -*- coding: utf-8 -*-

import cherrypy
from mpong import Game, Vector

class GameState:

    exposed = True
    states = {}

    @cherrypy.tools.json_out()
    def GET(self):
        currentGame = cherrypy.session['currentGame']
        return GameState.states[currentGame['id']].get_state()
        

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        stateIn = cherrypy.request.json()
        currentGame = cherrypy.session['currentGame']
        game_state = GameState.states.get(currentGame['id'], False)
        g_state = {}
        player1 = Vector(stateIn['player1'][0], stateIn['player1'][1])
        player2 = Vector(stateIn['player2'][0], stateIn['player2'][1])
        ball = Vector(stateIn['ball'][0], stateIn['ball'][1])
        g_state['player1'] = player1
        g_state['player2'] = player2
        g_state['ball'] = ball
        game_state.update(g_state)

        return self.GET()

    def PUT(self):
        currentGame = cherrypy.session['currentGame']
        GameState.states[currentGame['id']] = Game(100, joinedPlayers[0], joinedPlayers[1], 3)

    def DELETE(self):
        currentGame = cherrypy.session['currentGame']
        GameState.states.pop(currentGame['id'], None)

