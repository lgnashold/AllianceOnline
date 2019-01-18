DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS lobby;

CREATE TABLE game (
	join_code TEXT PRIMARY KEY,
	game_data TEXT,
	player1 TEXT,
	player2 TEXT,
	player3 TEXT,
	player4 TEXT,
	turn INTEGER,
	connections TEXT
);

CREATE TABLE lobby (
	join_code TEXT PRIMARY KEY,
	players TEXT
);
