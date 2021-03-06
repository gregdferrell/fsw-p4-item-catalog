--
--  Table definitions for the Story Time project.
--

-- Delete
DROP TABLE IF EXISTS story_category;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS story;
DROP TABLE IF EXISTS file_upload;
DROP TABLE IF EXISTS sec_user;

-- Recreate
CREATE TABLE IF NOT EXISTS sec_user (
  id                    SERIAL PRIMARY KEY,
  name                  TEXT NOT NULL,
  email                 TEXT UNIQUE NOT NULL,
  active                BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS upload_file (
  id                    SERIAL PRIMARY KEY,
  filename              TEXT NOT NULL,
  url                   TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS story (
  id                    SERIAL PRIMARY KEY,
  user_id               INTEGER REFERENCES sec_user(id),
  upload_file_id        INTEGER REFERENCES upload_file(id),
  title                 TEXT NOT NULL,
  description           TEXT NOT NULL,
  story_text            TEXT NOT NULL,
  published             BOOLEAN NOT NULL,
  date_created          TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc'),
  date_last_modified    TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS category (
  id                    SERIAL PRIMARY KEY,
  label                 TEXT UNIQUE NOT NULL,
  description           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS story_category (
  story_id              INTEGER REFERENCES story(id),
  category_id           INTEGER REFERENCES category(id),
  UNIQUE (story_id, category_id)
);
