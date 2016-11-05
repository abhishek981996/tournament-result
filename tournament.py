#created by Abhishek Tiwari
#on date 4-11-2016
#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    #deleting matches from database using delete command
    DB.commit()
    #commiting the changes inorder to save the logs
    DB.close()

def deletePlayers():

    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM players")
    #similar to delete matches fuunction
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(*) as num FROM players")
    #using num as count row 
    DB.commit()
    #now the obtain row has to be returned this can be done by calling c.fetchall() constructor
    #c.fetchall returns a list of tuple containing each row simultaneously 
    for row in c.fetchall():
        p = (row[0])
    DB.close()
    #taking only the count value in variable p as count column is in row 1.then returning the value of variable p
    return p


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players VALUES (%s)",(name,))
    #inserting the name using a tuple .
    #As it is a single value tuple comma have to be used to differentiate it from a variable
    DB.commit()
    DB.close()
    #closing the connection using close constructor


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
 
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT * FROM STANDINGS")
    standing_player = []
    #empty list to store the values from the table as a tuple 
    standing_player = c.fetchall()
    DB.close()
    return standing_player

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    
    #taking out the name of the given id from players table
    win = c.execute("SELECT name FROM players WHERE players.id = (%s)",(winner,))
    loss = c.execute("SELECT name FROM players WHERE players.id = (%s)",(loser,))
    
    #reporting the win and loss of match by inserting name (which was obtain from above) and id of players in matches table
    c.execute("INSERT INTO matches VALUES (%s,%s)",(winner,loser))
    DB.commit()
    DB.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    #Inorder to pair list of player standing has to be obtained 
    #below command selects id, name from STANDINGS table created in tournament.sql file
    #This table is already sorted in wins and equal wins context 
    c.execute("SELECT id,name from STANDINGS ORDER BY STANDINGS.wins  DESC, STANDINGS.id  ASC")
    pair = c.fetchall()
    swiss_pair = []
    
    #the obtained list of pair varaible contain a list of tuple but in a format of [(id,name),(id,name)....]
 
    for i in range(0,len(pair)):
        if i%2 != 0:
            swiss_pair.append(pair[i-1] + pair[i])
    #the above code is a lot easy .. try to understand by urself .. It would be fu after knowing it :-)
    DB.close()
    return swiss_pair


