import requests
import os


root = 'http://localhost:8080'
s = requests.Session()

url_player = os.path.join(root, 'lobby','player')
url_game = os.path.join(root, 'lobby', 'game')
url_join = os.path.join(root, 'lobby', 'join')
url_leave = os.path.join(root, 'lobby', 'leave')
url_start = os.path.join(root, 'lobby', 'start')
url_quit = os.path.join(root, 'lobby', 'quit')

# tests for one player
def test_Player():
    r = s.post(url_player, json={'player': {'name': 'Leibnitz'}})

    assert r['player']['name'] == 'Leibnitz'


def testPlayerAgain():
    r = s.post(url_player, json={'player': {'name': 'Leibnitz'}})
    assert r.json().get('player') == None


def testCreateGame():
    r = s.post(url_game, json={'id': 'TerminatorDaniel', 'maxPlayers': 2})
    assert r.json()['games'][0]['id'] == 'TerminatorDaniel'


def testJoin():
    r = s.post(os.path.join(url_join, '1'))
    assert r.json()['games'][0]['joinedPlayers'][0] == 'Leibnitz'


def testJoinAgain():
    r = s.post(ps.path.join(url_join, '1'))
    assert r.status_code == 401


def testLeave():
    r = s.post(url_leave)
    assert len(r.json()['games'][0]['joinedPlayers']) == 0 


def testDeleteGame():
    r = s.delete(os.path.join(url_game, '1'))
    assert r.json()['games'][0]['id'] == 'TerminatorDaniel'


# Add one more player to test start and stop game
s2 = requests.Session()

#def testStart():
    #r = s2.post(url_player, json={'player': {'name': 'Newton'}})
    #r = s2.post(url_game, json={'id': 'ChuckNorris', 'maxPlayers': 2})
    #r = s2.post(root + 'game/method/join/ChuckNorris')
    #r = s.post(root + 'game/method/join/ChuckNorris')
    #r = s.post(root + 'game/method/start')
    #assert r.json()['games'][0]['gameStarted']

#def testStop():
 #   r = s2.post(root + 'game/method/quit')
 #   assert r.status_code
