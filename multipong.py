#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import cherrypy

import handlers


class Root:
    pass

root = Root()
root.game = handlers.GameHandler()
root.game.method = Root()
root.game.method.join = handlers.JoinGameHandler()
root.game.method.leave = handlers.LeaveGameHandler()
root.game.state = handlers.GameState()
root.game.paddle = handlers.PaddleHandler()
root.player = handlers.PlayerHandler()

cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
cherrypy.quickstart(root, '/', cfgFile)
