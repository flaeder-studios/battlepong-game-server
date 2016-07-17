#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
This module contains a simple database class, DatabaseSimple. To use this database class for your objects
your object class only needs to inherit class DatabaseObject. DatabaseObject give your class a key to be
used when stored in DatabaseSimple.

This module also contain two classes to store in DatabaseSimple. That is Player and GameData.

Classes to be found here
    DatabaseObject
    Player(DatabaseObject)
    GameData(DatabaseObject)
    DatabaseSimple
"""

class DatabaseObject(object):
    """To store an object in DatabaseSimple inherit this class. An object is stored with a key which is an int"""
    i = 0
    def __init__(self):
        """Set databaseObject key. Key is set to an int"""
        DatabaseObject.i += 1
        self.key = DatabaseObject.i

    def getKey(self):
        """Return key for object"""
        return self.key


class Player(DatabaseObject):
    """First create player(). Then set player data with setPlayer()"""
    def __init__(self, name):
        """Initialize player"""
        super(Player, self).__init__()
        self.name = name
        self.currentGame = 0
        self.createdGames = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setCurrentGame(self, key):
        self.currentGame = key

    def getCurrentGame(self):
        return self.currentGame

    def setCreatedGames(self, key):
        for k in self.createdGames:
            if key == k:
                return None
        else:
            self.createdGames.append(key)
            return key

    def getCreatedGames(self):
        return self.createdGames[:]

    def copy(self):
        tmp = Player(self.name)
        tmp.currentGame = self.currentGame
        tmp.createdGames = self.createdGames[:]
        return tmp

class GameData(DatabaseObject):
    """First create GameData(). Then set gameData with setGameData."""
    def __init__(self, createdByPlayer, maxPlayers):
        """Create GameData(). Use setGameData() to set attributes"""
        super(GameData, self).__init__()
        self.createdBy = createdByPlayer
        self.maxPlayers = maxPlayers
        self.currentPlayers = [createdByPlayer]
        self.game = None

    def setCurrentPlayers(self, player):
        """set game data"""
        if self.maxPlayers < 2 and player not in self.currentPlayers:
            self.currentPlayers.append(player)
            return player
        else:
            return None

    def getCurrentPlayers(self):
        if len(self.currentPlayers) < 2:
            return [self.createdBy.copy()]
        else:
            return [self.currentPlayers[0].copy(), self.currentPlayers[1].copy()]

    def startGame(self):
        # start game. Add mpong.newModel.Game() to self.game.
        pass

    def copy(self):
        tmp = GameData(self.createdBy.copy(), self.maxPlayers)
        if len(self.currentPlayers) > 1:
            tmp.setCurrentPlayers(self.currentPlayers[1].copy())
        return tmp


class Database(object):
    """Stores object that inherit class DatabaseObject"""
    def __init__(self):
        self.data = []

    def add(self, obj):
        """Add object to database. If object is added object is returned, otherwise returns None"""
        for elem in self.data:
            if obj.getKey() == elem.getKey():
                return None
        else:
            self.data.append(obj)
            return obj

    def search(self, key):
        """Search database for object with key, key. If found returns object otherwise returns None"""
        for elem in self.data:
            if key == elem.getKey():
                return elem
        else:
            return None

    def deleteObj(self, key):
        """Delete object with key, key. If found returns object otherwise returns None"""
        obj = self.search(key)
        if obj is not None:
            self.data.remove(obj)
            return obj
        else:
            return None


if __name__ == "__main__":
    playerDatabase = DatabaseSimple()
    p = Player('Erik')
    p1 = Player('Malin')
    print p.getKey(), p1.getKey()
    p.setCurrentGame(1)
    p1.setCurrentGame(2)
    playerDatabase.add(p)
    playerDatabase.add(p1)
    print playerDatabase.data
    playerDatabase.deleteObj(1)
    print playerDatabase.data

