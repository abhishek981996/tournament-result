-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (name Text,
			id serial primary key, 
			UNIQUE(id)
			);
-- Table players contains column name (text) ,id (serial). id is use as a primary key inorder to establish foreign key 
--relationship			
			
CREATE TABLE matches(player_won int,
			player_lost int,
			NUM serial,
			FOREIGN KEY(player_won) REFERENCES players(id),
			FOREIGN KEY(player_lost) REFERENCES players(id)
			);

--A view is a virtual table based on the result-set of an SQL statement.
-- A view of players standing containing id ,name ,no of matches won , toatal matches played column are listed 
CREATE OR REPLACE VIEW standing AS
	SELECT players.id, players.name,
	sum(CASE WHEN players.id = matches.player_won THEN 1 ELSE 0 END) as won,
	sum(CASE WHEN players.id = matches.player_won OR players.id = matches.player_lost THEN 1 ELSE 0 END ) as match_play
	FROM players, matches
	GROUP BY players.id
	ORDER BY won DESC;
