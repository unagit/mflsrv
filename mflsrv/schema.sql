-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS tuser;
DROP TABLE IF EXISTS tprops;

CREATE TABLE tuser (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE tprops (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
--  prop_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ppin TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
