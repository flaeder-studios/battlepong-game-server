#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy

class GameState:

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):

        # Get representation of game (paddles and ball positions)

        game = {
            'balls': [
                {'xpos': 0.0, 'ypos': -0.1, 'radius': 0.05},
                {'xpos': 0.8, 'ypos': -0.2, 'radius': 0.02}
            ],
            'paddles': [
                {
                    'xpos': 0.9,
                    'ypos': 0.0,
                    'length': 0.25,
                    'width': 0.05
                }, 
                {
                    'xpos': 0.9,
                    'ypos': 0.0,
                    'length': 0.25,
                    'width': 0.05,
                }
            ]
        }

        return game
