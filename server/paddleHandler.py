#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy


class PaddleHandler:

    exposed = True

    def POST(self, paddleId, spd):

        # string -> float

        spd = float(spd)
        cherrypy.log('Set paddle speed to %f' % spd)


