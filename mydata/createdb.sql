CREATE TABLE IF NOT EXISTS airports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icao TEXT NOT NULL,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    subd TEXT NOT NULL,
    country TEXT NOT NULL,
    elv INTEGER NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    depart_icao TEXT NOT NULL,
    arrive_icao TEXT NOT NULL,
    FOREIGN KEY (depart_icao) REFERENCES airports(icao),
    FOREIGN KEY (arrive_icao) REFERENCES airports(icao)
)
