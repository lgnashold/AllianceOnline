DROP TABLE IF EXISTS game;

CREATE TABLE game (
	join_code TEXT PRIMARY KEY,
	game_data TEXT,
	player1 TEXT,
	player2 TEXT,
	player3 TEXT,
	player4 TEXT,
	turn TEXT
);
