CREATE TABLE accounting_entry (
    uid INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    date INTEGER NOT NULL,
    desc TEXT,
    deleted INTEGER DEFAULT 0);


CREATE TABLE tag (
    uid INTEGER PRIMARY KEY,
    value TEXT UNIQUE NOT NULL,
    deleted INTEGER DEFAULT 0);


CREATE TABLE tag_mm(
    uid_local INTEGER NOT NULL,
    uid_foreign INTEGER NOT NULL,
    FOREIGN KEY (uid_local) REFERENCES tags(uid));
