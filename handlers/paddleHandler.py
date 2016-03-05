#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class PaddleHandler:

    exposed = True

    def POST(self, playerName, spd):

        # string -> float

        masterGame.setPlayerSpeed(playerName, float(spd))
        cherrypy.log('Set paddle speed to %f' % spd)


