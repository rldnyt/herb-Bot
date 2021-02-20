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
        nuasd = int(number) / 5
        if int(number) > 21600: return await ctx.message.reply(f'21600초(6시간) 이상으로는 설정할수 없습니다.')
        await ctx.channel.edit(slowmode_delay=int(number))
        if int(number) == 0: return  await ctx.message.reply(embed=discord.Embed(description=f"{ctx.channel.mention}의 딜레이를 제거 하였습니다.", colour=tool.Color.green, timestamp=ctx.message.created_at).set_footer(text=ctx.author, icon_url=ctx.author.avatar_url))
        await ctx.message.reply(embed=discord.Embed(description=f"{ctx.channel.mention}의 딜레이를 `{str(number)}s`으로 변경되었습니다.", colour=tool.Color.green, timestamp=ctx.message.created_at).set_footer(text=ctx.author, icon_url=ctx.author.avatar_url))

def setup(app):
    app.add_cog(Server(app))
    print("Cogs.Server Load")