CREATE TABLE IF NOT EXISTS Response (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    header varchar(255) NOT NULL,
    directory varchar(255) NOT NULL,
    body TEXT NOT NULL,
    status_code INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS logs(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NOT NULL,
    message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS redirect_url (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    url varchar(255) NOT NULL 
);