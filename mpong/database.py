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
    Database
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
    def __init__(self, name):
        """Initialize player"""
        super(Player, self).__init__()
        self.name = name
        self.currentGame = 0    # key of currentGame

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setCurrentGame(self, key):
        self.currentGame = key

    def getCurrentGame(self):
        return self.currentGame

    def copy(self):
        tmp = Player(self.name)
        tmp.currentGame = self.currentGame
        return tmp

class GameData(DatabaseObject):
    """First create GameData(). Then set gameData with setGameData."""
    def __init__(self, createdByPlayer, maxPlayers):
        super(GameData, self).__init__()
        self.createdBy = createdByPlayer
        self.maxPlayers = maxPlayers
        self.currentPlayers = []
        self.game = None

    def setCurrentPlayers(self, player):
        """Throws ValueError."""
        if player in self.currentPlayers:
            raise ValueError('Player already in game.')
        if len(self.currentPlayers) == self.maxPlayers:
            raise ValueError('Game is full.')
        self.currentPlayers.append(player)
        return player

    def getCurrentPlayers(self):
        if len(self.currentPlayers) < 1:
            return []
        elif len(self.currentPlayers) < 2:
            return [self.currentPlayers[0].copy()]
        else:
            return [self.currentPlayers[0].copy(), self.currentPlayers[1].copy()]

    def leaveCurrentPlayers(self, player):
        """Throws ValueError."""
        if player not in self.currentPlayers:
            raise ValueError('Player not found in currentPlayers.')
        self.currentPlayers.remove(player)
        return player

    def startGame(self):
        # start game. Add mpong.newModel.Game() to self.game.
        pass

    def copy(self):
        tmp = GameData(self.createdBy.copy(), self.maxPlayers)
        tmp.currentPlayers = self.getCurrentPlayers()
        return tmp


class Database(object):
    """Stores object that inherit class DatabaseObject"""
    def __init__(self):
        self.data = []

    def add(self, obj):
        """Add object to database. Throws ValueError."""
        if  obj in self.data:
            raise ValueError("Object alread in databasase.")
        self.data.append(obj)
        return obj

    def search(self, key):
        """Search database for object with key, key. Throws ValueError."""
        for elem in self.data:
            if key == elem.getKey():
                return elem
        else:
            raise ValueError("Object not found")

    def deleteObj(self, key):
        """Delete object with key, key. Throws ValueError."""
        obj = self.search(key)
        self.data.remove(obj)
        return obj


if __name__ == "__main__":
    playerDatabase = Database()
    #p = Player('Erik')
    #p1 = Player('Malin')
    #print p.getKey(), p1.getKey()
    #p.setCurrentGame(1)
    #p1.setCurrentGame(2)
    #playerDatabase.add(p)
    #playerDatabase.add(p1)
    #print playerDatabase.data
    #playerDatabase.deleteObj(1)
    #print playerDatabase.data
    try:
        p = Player('Daniel')
        playerDatabase.add(p)
        playerDatabase.add(p)
        playerDatabase.search(5)
    except ValueError as e:
        print "Database error:", str(e)


