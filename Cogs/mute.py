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
tool.database.add.table(self=None, dbfile=config.BotSettings.dbname, tablename="mute",tabledata="guild INTEGER PRLMARY KEY, user INTEGER PRLMARY KEY, role TEXT PRLMARY KEY, code TEXT PRLMARY KEY, reason TEXT PRLMARY KEY")

import utils.db.herb_mute_db as herbdb_mute


class Mute(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="뮤트", aliases=["mute"], pass_context=True)
    async def mute(self, ctx, user: discord.User = None, *,reason=None):
        role = discord.utils.find(lambda r: r.name == "[ Mute_Role ]", ctx.guild.roles)
        if role is None: return await ctx.message.reply(f"이런! `[ Mute_Role ]` 역활이 없습니다! `{config.BotSettings.prefix}뮤트생성` 을 입력해주세요!")
        giverole = discord.utils.get(ctx.guild.roles, id=role.id)
        if user is None: await ctx.message.reply("뮤트하려는 유저를 입력해주세요!")
        usrss = ctx.guild.get_member(user.id)
        if giverole in usrss.roles: return await ctx.message.reply(f"{user.mention}님은 이미 뮤트되어있습니다!")
        if herbdb_mute.Check_Mute(ctx, int(user.id)) is True and not giverole in usrss.roles:
            conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
            cur = conn.cursor()
            table = list(cur.execute('SELECT * FROM mute WHERE guild=? and user=?', (int(ctx.guild.id), int(user.id),)))
            cur.execute(f"DELETE FROM mute WHERE code=?", (str(table[0][3]),))
            conn.commit()
            cur.close()
            conn.close()
        usrms = herbdb_mute.mute(int(user.id), ctx, self.app)
        if reason is None: reason = "사유가 없습니다!"
        lists = await usrms.add(reason)
        await usrss.add_roles(giverole)
        embed = discord.Embed(color=tool.Color.green, title="뮤트", description=f"{user.mention}님이 뮤트처리가 되었습니다.\n\n사유 : {reason}", timestamp=ctx.message.created_at)
        lists1 = lists[0]
        lists2 = lists[2]
        if len(lists[0]) <= 0: lists1 = "(없습니다)"
        if len(lists[2]) <= 0: lists2 = "(없습니다)"
        embed.add_field(name="빼앗긴에 성공한 역활", value=str(lists1), inline=False)
        embed.add_field(name="빼앗기에 실패한 역활", value=str(lists2), inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="뮤트생성", aliases=["mutecreate"], pass_context=True)
    async def mutecreate(self, ctx):
        role = discord.utils.find(lambda r: r.name == "[ Mute_Role ]", ctx.guild.roles)
        if not role is None:
            return await ctx.message.reply(f"이미 `[ Mute_Role ]` 이름의 역활이 생성되어있습니다!")
        msg = await ctx.channel.send(embed=discord.Embed(description="<a:loading8:813962183239139341> `[ Mute_Role ]` 역활를 생성중입니다!", color=tool.Color.green))
        roles = await ctx.guild.create_role(name='[ Mute_Role ]', permissions=discord.Permissions(send_messages=False, read_messages=True))
        v1, v2 = 0, 0
        for i in ctx.guild.channels:
            try:
                await i.set_permissions(roles, send_messages=False)
                v1 += 1
            except: v2 += 1
        await msg.edit(embed=discord.Embed(description=f"뮤트 세팅이 완료되었습니다.\n\n성공적으로 세팅된 채널 : {v1}개\n세팅에 실패한 채널 : {v2}개\n\n**안내사항**\n> `[ Mute_Role ]`의 이름을 가진 역활을 더이상 만들지 마세요. 만들경우 뮤트가 적용되지 않습니다. 이름수정도 하지마세요.", color=tool.Color.green))

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="언뮤트", aliases=["unmute", "뮤트해제"], pass_context=True)
    async def unmute(self, ctx, user: discord.User = None):
        role = discord.utils.find(lambda r: r.name == "[ Mute_Role ]", ctx.guild.roles)
        if role is None: return await ctx.message.reply(f"이런! `[ Mute_Role ]` 역활이 없습니다! `{config.BotSettings.prefix}뮤트생성` 을 입력해주세요!")
        removerole = discord.utils.get(ctx.guild.roles, id=role.id)
        if user is None: await ctx.message.reply("언뮤트하려는 유저를 입력해주세요!")
        usrss = ctx.guild.get_member(user.id)
        if not removerole in usrss.roles:
            if herbdb_mute.Check_Mute(ctx, int(user.id)) is True:
                conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
                cur = conn.cursor()
                table = list(cur.execute('SELECT * FROM mute WHERE guild=? and user=?', (int(ctx.guild.id), int(user.id),)))
                cur.execute(f"DELETE FROM mute WHERE code=?", (str(table[0][3]),))
                conn.commit()
                cur.close()
                conn.close()
            return await ctx.message.reply(f"{user.mention}님은 뮤트 상태가 아님니다!")
        usrms = herbdb_mute.mute(int(user.id), ctx, self.app)
        lists = await usrms.removal()
        if lists is False: return await ctx.message.reply(f"{user.mention}님의 뮤트 기록을 찾을수 없습니다!")
        await usrss.remove_roles(removerole)
        embed = discord.Embed(color=tool.Color.green, title="언뮤트",description=f"{user.mention}님이 언뮤트처리가 되었습니다.",timestamp=ctx.message.created_at)
        lists1 = lists
        if len(lists) <= 0: lists1 = "(없습니다)"
        embed.add_field(name="다시 지급된 역활", value=str(lists1), inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)




def setup(app):
    app.add_cog(Mute(app))
    print("Cogs.Mute Load")