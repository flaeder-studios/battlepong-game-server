#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import cherrypy

import server


class Root:

    pass


root = Root()
root.game = server.GameState()
root.game.paddle = server.PaddleHandler()

cfgFile = os.path.dirname(os.path.realpath(__file__)) \
    + '/multipong.conf'
cherrypy.quickstart(root, '/', cfgFile)
