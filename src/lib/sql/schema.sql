-----------------------------------------------------------------------------
-- Title       : schema.sql
-- Description : Simple SQLite schema for ASMdisks
-- Author      : Bart Sjerps <bart@dirty-cache.com>
-- License     : GPLv3+
-----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS metadata(id INTEGER PRIMARY KEY CHECK (id = 0), serial integer, diskstring TEXT NOT NULL, user TEXT NOT NULL, grp TEXT NOT NULL, mode INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS volumes(volname PRIMARY KEY, disktype TEXT NOT NULL, identifier TEXT UNIQUE);

INSERT OR IGNORE INTO metadata(id, serial, diskstring, user, grp, mode) VALUES (0, 1, 'oracleasm', 'grid', 'asmdba', 432);
