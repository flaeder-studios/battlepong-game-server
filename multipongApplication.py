
import handlers

def handleError():
    cherrypy.response.status = 500
    cherrypy.response.body = ["An error occurred..."]


class Root:
    _cp_config = {'request.error_response': handleError}


root = Root()
root.game = handlers.GameHandler()
root.game.method = Root()
root.game.method.join = handlers.JoinGameHandler()
root.game.method.leave = handlers.LeaveGameHandler()
root.game.method.start = handlers.StartHandler()
root.game.method.quit = handlers.StopHandler()
root.game.state = handlers.GameState()
root.game.paddle = handlers.PaddleHandler()
root.player = handlers.PlayerHandler()
root.ws = handlers.WebSocketHandler()