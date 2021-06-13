CREATE TABLE IF NOT EXISTS CLDATA(
	MATCHID integer PRIMARY KEY,
	MATCHDATE DATE,
	COUNTRY varchar(30),
	LEAGUE varchar(20),
	MTYPE varchar(20),
    SEASON TEXT,
    HOME_TEAM TEXT,
    AWAY_TEAM TEXT,
    FTR CHAR(1),
    FTHG INT,
    FTAG INT,
    A_COR INT,
    H_COR INT,
    A_FL varchar(3),
    H_FL varchar(3),
    A_RC INT,
    H_RC INT
);