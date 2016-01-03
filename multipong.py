import os

import cherrypy

class Root:
    pass

cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
cherrypy.quickstart(Root(), '/', cfgFile)
