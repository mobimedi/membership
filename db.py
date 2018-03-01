#!/usr/bin/env python
# -*- coding:utf-8 -*-
# nagexiucai.com


import sqlite3 as DB


class Database:
    CONNECT = None

    def __init__(self):
        if Database.CONNECT is None:
            Database.CONNECT = DB.connect("aio.dll")

    def __del__(self):
        if Database.CONNECT is not None:
            Database.CONNECT.close()

    def Execute(self, sql):  # TODO: make many
        assert isinstance(sql, basestring)
        cursor = Database.CONNECT.cursor()
        cursor.execute(sql)
        if sql.upper().startswith("SELECT "):
            return cursor.fetchall()
        else:
            Database.CONNECT.commit()
        cursor.close()
        return []
