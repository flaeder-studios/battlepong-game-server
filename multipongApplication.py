import handlers
import cherrypy


def handleError():
    cherrypy.response.status = 500
    cherrypy.response.body = ["An error occurred..."]


class Root:
    _cp_config = {'request.error_response': handleError}

players = {}
gameData = {}
root = Root()

root.game = Root()
#root.game.state = handlers.GameState(gameData)
root.game.paddle = handlers.PaddleHandler(players)

root.lobby = Root()
root.lobby.game = handlers.GameHandler(players, gameData)
root.lobby.player = handlers.PlayerHandler(players)

root.lobby.method = Root()
root.lobby.method.join = handlers.JoinGameHandler(players, gameData)
root.lobby.method.leave = handlers.LeaveGameHandler(players, gameData)
root.lobby.method.start = handlers.StartHandler(players, gameData)
root.lobby.method.quit = handlers.StopHandler(players, gameData)

root.ws = handlers.WebSocketHandler()
