import sqlite3
import config
import tool
import discord
import asyncio
from discord.ext import commands
import random

tool.database.add.table(self=None, dbfile=config.BotSettings.dbname, tablename="mute",tabledata="guild INTEGER PRLMARY KEY, user INTEGER PRLMARY KEY, role TEXT PRLMARY KEY, code TEXT PRLMARY KEY, reason TEXT PRLMARY KEY")

def Check_Mute(ctx: commands.Context, id:int,dbname=config.BotSettings.dbname):
    conn = sqlite3.connect(f"{dbname}.db")
    cur = conn.cursor()
    table = list(cur.execute('SELECT * FROM mute WHERE guild=? and user=?', (int(ctx.guild.id), id,)))
    conn.close()
    if not table: return False
    else: return True

class mute():
    def __init__(self, id:int, ctx: commands.Context, bot: commands.Bot,dbname=config.BotSettings.dbname):
        self.id = id
        self.ctx = ctx
        self.bot = bot
        self.dbname = dbname

    async def add(self, reason=None):
        chake_mur = Check_Mute(self.ctx, self.id)
        role = discord.utils.find(lambda r: r.name == "Mute", self.ctx.guild.roles)
        msgasf = self.ctx.guild.get_member(self.id)

        users = self.ctx.guild.get_member(self.id)
        if users is None or not users: return None
        noreod = ""
        reod1 = ""
        reod2 = ""
        v2 = len(users.roles)
        for i in users.roles:
            v2 -= 1
            try:
                if "everyone" in i.name: continue
                await users.remove_roles(i, reason="뮤트로 인한 역활 압수.")
                print(v2)
                if v2 <= 1: reod1 += f"{i.mention}"
                else: reod1 += f"{i.mention}, "
                reod2 += f"{str(i.id)}#"
            except:
                if v2 <= 1: noreod += f"{i.mention}"
                else: noreod += f"{i.mention}, "
        code = random.randint(1,999999999999)
        if reason is None: reason = "사유가 없습니다!"
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO mute VALUES(?,?,?,?,?)''', (int(self.ctx.guild.id), self.id, str(reod2), code, reason))
        conn.commit()
        cur.close()
        conn.close()
        return reod1, reod2, noreod

    async def removal(self):
        users = self.ctx.guild.get_member(self.id)
        if users is None or not users: return None
        conn = sqlite3.connect(f"{self.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM mute WHERE guild=? and user=?', (int(self.ctx.guild.id), self.id,)))
        if not table:
            conn.commit()
            cur.close()
            conn.close()
            return False
        cur.execute(f"DELETE FROM mute WHERE code=?", (str(table[0][3]),))
        conn.commit()
        cur.close()
        conn.close()
        rolda = table[0][2].split('#')
        ssdfg = ""
        v2 = len(rolda)
        for i in rolda:
            v2 -= 1
            if len(i) <= 0: continue
            await users.add_roles(discord.utils.find(lambda r: r.id == int(i), self.ctx.guild.roles))
            if v2 <= 1: ssdfg += f"{discord.utils.find(lambda r: r.id == int(i), self.ctx.guild.roles).mention}"
            else: ssdfg += f"{discord.utils.find(lambda r: r.id == int(i), self.ctx.guild.roles).mention}, "
        return ssdfg


