#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mpong.masterGameBuilder import masterGame


class PaddleHandler:

    exposed = True

    def POST(self,spd):
        """ str -> float """

        playerName = cherrypy.session.get('name')
        if playerName is None:
            raise cherrypy.HTTPError(400, 'No player with name %s' % playerName)

        masterGame.setPlayerSpeed(playerName, float(spd))
        cherrypy.log('Set paddle speed to %f' % spd)


