import asyncio

import discord
from discord.ext import commands
import datetime
import random
from random import choice
import time
import tool
import config
import os
import sqlite3

tool.database.add.table(self=None, dbfile=config.BotSettings.dbname, tablename="logchannel",tabledata="channelid INTEGER PRLMARY KEY, guildid INTEGER PRLMARY KEY")

class Server(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.has_permissions(manage_messages=True)
    @commands.command(name="clear", aliases=["채팅청소", "청소", "챗청"], pass_context=True)
    async def chatclear(self, ctx, number=None):
        if number is None: return await ctx.message.reply(f'채팅을 청소하시려는 수를 입력해주셔야 합니다!')
        if number.isdecimal() is False: return await ctx.message.reply(f'숫자만 입력할수 있습니다!')
        try: await ctx.message.delete()
        except: pass
        deleted = await ctx.channel.purge(limit=int(number))
        embed = discord.Embed(title="채팅 청소 완료", description=f"{str(len(deleted))}개의 메세지를 삭제했습니다.", color=tool.Color.green)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        try: await msg.delete()
        except: pass

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="슬로우모드", aliases=["slowmode", "슬로우", "딜레이"], pass_context=True)
    async def slowmode(self, ctx, number=None):
        if number is None: return await ctx.message.reply(f'채팅방에 설정 하려는 초를 입력해주세요.')
        if number.isdecimal() is False: return await ctx.message.reply(f'숫자만 입력할수 있습니다!')
        if int(number) > 21600: return await ctx.message.reply(f'21600초(6시간) 이상으로는 설정할수 없습니다.')
        await ctx.channel.edit(slowmode_delay=int(number))
        if int(number) == 0: return  await ctx.message.reply(embed=discord.Embed(description=f"{ctx.channel.mention}의 딜레이를 제거 하였습니다.", colour=tool.Color.green, timestamp=ctx.message.created_at).set_footer(text=ctx.author, icon_url=ctx.author.avatar_url))
        await ctx.message.reply(embed=discord.Embed(description=f"{ctx.channel.mention}의 딜레이를 `{str(number)}s`으로 변경되었습니다.", colour=tool.Color.green, timestamp=ctx.message.created_at).set_footer(text=ctx.author, icon_url=ctx.author.avatar_url))

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="로그", pass_context=True)
    async def logchannel(self, ctx, content:str=None):
        if content is None:
            conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
            cur = conn.cursor()
            table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (ctx.guild.id,)))
            conn.close()
            if not table: return await ctx.message.reply(embed=discord.Embed(title="로그", description=f"현재 `{ctx.guild.name}`은 로그채널이 설정되어있지 않습니다!", color=tool.Color.green))
            channelss = self.app.get_channel(table[0][0])
            if not channelss or channelss is None: chatssss = "없습니다!"
            else: chatssss = channelss.mention
            await ctx.message.reply(embed=discord.Embed(title="로그", description=f"현재 `{ctx.guild.name}`의 로그채널은 {chatssss} 입니다.\n\n로그를 끄시려면 `{config.BotSettings.prefix}로그 제거`를 입력하세요.", color=tool.Color.green))
            return
        if str(content) == "제거" or str(content) == "끄기":
            conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
            cur = conn.cursor()
            table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (ctx.guild.id,)))
            conn.close()
            if not table: return ctx.message.reply(f"{ctx.author.mention} 로그채널이 설정되어있지 않습니다.")
            tool.database.removal.data(self=None, dbfile=config.BotSettings.dbname, tablename="logchannel", dataname="guildid=?",data=ctx.guild.id)
            await ctx.message.reply(f"{ctx.author.mention} {ctx.guild.name}의 로그를 껏습니다.")
            return

        try: channelcontent = self.app.get_channel(int(content.replace("<#", "").replace("!", "").replace(">", "")))
        except Exception as e:
            if "invalid literal for int() with" in str(e): return await ctx.message.reply("이런! 채널에는 채널멘션또는 ID만 인식됩니다!")
        if channelcontent is None or not channelcontent: return await ctx.message.reply("채널을 찾을수 없습니다.")
        conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (ctx.guild.id,)))
        conn.close()
        channelid = channelcontent.id
        guildid = ctx.guild.id
        if not table:
            data = channelid, guildid
            tool.database.add.data(self=None, dbfile=config.BotSettings.dbname, tablename="logchannel", tabledata_the_number="?,?" ,data=data)
            await ctx.message.reply(embed=discord.Embed(description=f"{channelcontent.mention}으로 로그채널이 설정되었습니다!", timestamp=ctx.message.created_at, color=tool.Color.green))
        else:
            fa = table[0]
            logchannel = fa[0]
            if channelid == logchannel: return await ctx.message.reply(f"로그채널은 이미 <#{channelid}> 으로 설정되어있습니다.")
            data = channelid, guildid
            tool.database.update.data(self=None, dbfile=config.BotSettings.dbname, tablename="logchannel", dataname="guildid = ?", data=guildid, tabledata_the_number="?,?", tabledata=data)
            await ctx.message.reply(embed=discord.Embed(description=f"{channelcontent.mention}으로 로그채널이 설정되었습니다!", timestamp=ctx.message.created_at, color=tool.Color.green))




def setup(app):
    app.add_cog(Server(app))
    print("Cogs.Server Load")