-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( name TEXT,
                       id SERIAL primary key);

CREATE TABLE matches ( playerL integer references players (id),
                       playerR integer references players (id),
                       winner integer);
