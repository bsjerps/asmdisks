import os, sqlite3
from pkgutil import get_data
from collections import namedtuple

"""
sqlitedb.py - SQLite database functions for ASMDisks
Copyright (c) 2023 - Bart Sjerps <bart@dirty-cache.com>
License: GPLv3+
"""

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

def _where(**kwargs):
    if not kwargs:
        return '1=1'
    conditions = map(lambda x: '{} = ?'.format(x,x), kwargs)
    where      = ' AND '.join(conditions)
    return where

class Table():
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
    
    def get(self, **kwargs):
        where  = _where(**kwargs)
        values = list(kwargs.values())
        q = f'SELECT * FROM {self.table_name} WHERE {where}'
        cur = self.db.conn.execute(q, values)
        return cur.fetchone()

    def select(self, columns, orderby=None, **kwargs):
        columns = ', '.join(columns.split(','))
        where   = _where(**kwargs)
        q = f'SELECT {columns} FROM {self.table_name} WHERE {where}'
        if orderby:
            q += f' ORDER BY {orderby}'
        cur = self.db.conn.execute(q)
        return cur.fetchall()

    def report(self, columns, orderby=None, **kwargs):
        columns = ', '.join(columns.split(','))
        where   = _where(**kwargs)
        q = f'SELECT {columns} FROM {self.table_name} WHERE {where}'
        if orderby:
            q += f' ORDER BY {orderby}'
        cur = self.db.conn.execute(q)
        header = [x[0] for x in cur.description]
        return header, cur.fetchall()

    def insert(self, **kwargs):
        columns    = ', '.join(kwargs)
        parameters = ','.join(['?'] * len(kwargs))
        values     = list(kwargs.values())
        q = f'INSERT INTO {self.table_name} ({columns}) VALUES ({parameters})'
        try:
            #print(q, kwargs.values())
            cur = self.db.conn.execute(q, values)
            self.db.conn.commit()
            print(f'{cur.rowcount} rows inserted')
        except sqlite3.IntegrityError:
            print(f'Item already exists')

    def update(self, data={}, **kwargs):
        where      = _where(**kwargs)
        values     = list(data.values()) + list(kwargs.values())
        parameters = ', '.join(f'{x} = ?' for x in data)
        q = f'UPDATE {self.table_name} SET {parameters} WHERE {where}'
        try:
            cur = self.db.conn.execute(q, values)
            self.db.conn.commit()
            print(f'{cur.rowcount} rows updated')
        except sqlite3.IntegrityError:
            print(f'{self.table_name} update error')

    def delete(self, **kwargs):
        where  = _where(**kwargs)
        values = list(kwargs.values())
        q = f'DELETE FROM {self.table_name} WHERE {where}'
        try:
            cur = self.db.conn.execute(q, values)
            self.db.conn.commit()
            print(f'{cur.rowcount} rows deleted')
        except sqlite3.IntegrityError:
            print(f'{self.table_name} delete error')

class Database():
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = namedtuple_factory
        cur = self.conn.execute("select name from sqlite_master where type='table'")
        self.tablelist = [x[0] for x in cur.fetchall()]

    def destroy(self):
        self.conn.close()
        os.unlink(self.path)

    def schema(self):
        sql = get_data('sql', 'schema.sql').decode()
        self.conn.executescript(sql)
        self.conn.commit()

    def __getattr__(self, name):
        try:
            self.conn.execute("select * from metadata")
        except sqlite3.OperationalError:
            raise ValueError('Database not initialized, run setup')
        if name in self.tablelist:
            return Table(self, name)
        else:
            raise AttributeError(f'No such table: {name}')

