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
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    """get first col of first row from aggregate results."""
    num = c.fetchall()[0][0]
    db.close()
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c. execute("insert into players (name) values (%s);", (name,))
    db.commit()
    db.close()

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
    db = connect()
    c = db.cursor()
    """create view for record wins of each players"""
    win_query = '''create view win_num as 
                   select players.id, players.name, count(matches.winner) as wins 
                   from players left join matches 
                   on players.id = matches.winner 
                   group by players.id 
                   order by wins desc;'''

    """create view for record matches of each players"""
    match_query = '''create view match_num as 
                     select players.id, players.name, count(matches.winner) as matches 
                     from players left join matches 
                     on players.id = matches.playerl or players.id = matches.playerr 
                     group by players.id 
                     order by matches desc;'''

    """join two views to get final tuples"""
    stand_query = '''select win_num.id, win_num.name, win_num.wins, match_num.matches 
                     from win_num join match_num 
                     on win_num.id = match_num.id 
                     order by win_num.wins desc;'''

    c.execute(win_query)
    c.execute(match_query)
    c.execute(stand_query)
    rows = c.fetchall()
    c.execute("drop view win_num;")
    c.execute("drop view match_num;")
    db.close()
    return rows
    
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (playerl, playerr, winner) values (%s, %s, %s);", (winner, loser, winner))
    db.commit()
    db.close()
 
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
    standings = playerStandings()
    parings = []

    for i in range(0, len(standings) / 2):
        tup1 = (standings[i * 2][0], standings[i * 2][1])
        tup2 = (standings[i * 2 + 1][0], standings[i * 2 + 1][1])
        parings.append(tup1 + tup2)

    return parings
        
 
    
 


