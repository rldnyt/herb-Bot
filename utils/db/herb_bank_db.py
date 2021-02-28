import sqlite3
import config
import tool
import discord
import asyncio
from discord.ext import commands
import random

tool.database.add.table(self=None, dbfile=config.BotSettings.dbname, tablename="bank", tabledata="money INTEGER NOT NULL, id INTEGER PRIMARY KEY, time INTEGER NOT NULL, bankbook INTEGER NOT NULL")

class bank():
    def __init__(self, id:int, dbname=config.BotSettings.dbname):
        self.id = id
        self.dbname = dbname

    def get_money(self):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table or table is None: return None
        return table[0][0]

    def get_bankbook(self):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table or table is None: return None
        return table[0][3]

    def get_time(self):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table or table is None: return None
        return table[0][2]

    def get_all(self):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table or table is None: return None
        return table[0][0], table[0][2], table[0][3] # 돈, 시간, 통장

    def update_money(self, money:int, mode:bool=True):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table:
            if mode is False: return None
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (money, self.id, 0, 0))
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM bank WHERE id=?", (self.id,))
            if mode is False: asdf = int(table[0][0]) - money
            else: asdf = int(table[0][0]) + money
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (asdf, self.id, table[0][2], table[0][3]))
            conn.commit()
            cur.close()
            conn.close()
            return True

    def update_bankbook(self, money: int, mode:bool=True):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table:
            if mode is False: return None
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (0, self.id, 0, money))
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM bank WHERE id=?", (self.id,))
            if mode is False: asdf = int(table[0][0]) - money
            else: asdf = int(table[0][0]) + money
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (table[0][0], self.id, table[0][2], asdf))
            conn.commit()
            cur.close()
            conn.close()
            return True

    def update_time(self, time: int):
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM bank WHERE id=?', (self.id,)))
        conn.close()
        if not table:
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (0, self.id, time, 0))
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            conn = sqlite3.connect(f"{self.dbname}.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM bank WHERE id=?", (self.id,))
            asdf = int(table[0][2]) + time
            cur.execute(f'''INSERT INTO bank VALUES(?,?,?,?)''', (table[0][0], self.id, asdf, table[0][3]))
            conn.commit()
            cur.close()
            conn.close()
            return True
