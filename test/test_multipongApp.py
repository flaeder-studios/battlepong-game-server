import cherrypy
from cherrypy.test import helper
from multipongApplication import root
import os
from ws4py.websocket import EchoWebSocket


if __name__ == '__main__':
    print('Starting test of multipongApplication.py')
    class SimpleCPTest(helper.CPWebCase):
        def setup_server():
            def standardErrorMessage(status, message, traceback, version):
                response = cherrypy.response
                response.headers['Content-Type'] = 'application/json'
                return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'version': version})

            cherrypy.config.update({'error_page.default': standardErrorMessage})
            cherrypy.config.update({'log.screen': True,
                                    'log.access_file': '',
                                    'log.error_file': '',
                                    'server.thread_pool': 30,
                                    'server.socket_host': "127.0.0.1",
                                    'server.socket_port': 8080})
            cfgFile = os.path.dirname(os.path.realpath(__file__)) + '/multipong.conf'
            cherrypy.tree.mount(root)
        setup_server = staticmethod(setup_server)

        def test_simple_thing(self):
            self.getPage("http://127.0.0.1:8080/")
            self.assertStatus('200 OK')

    c = SimpleCPTest()
    c.test_simple_thing()