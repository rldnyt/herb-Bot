import asyncio

import discord
from discord.ext import commands
import datetime
import random
from random import choice
import time
import sqlite3
import tool
import threading
import matplotlib.pyplot as plt
import utils.db.herb_bank_db as bank_db
import config

from discord import Webhook, RequestsWebhookAdapter
tool.database.add.table(self=None, dbfile=config.BotSettings.dbname, tablename="bank", tabledata="money INTEGER NOT NULL, id INTEGER PRIMARY KEY, time INTEGER NOT NULL, bankbook INTEGER NOT NULL")

logwebhook = Webhook.partial(config.BankSettings.logwebid, config.BankSettings.logwebtoken, adapter=RequestsWebhookAdapter())


class Bank(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    @commands.command(name="돈", pass_context=True)
    async def money(self, ctx, name: discord.User=None):
        if name is None:
            monb = bank_db.bank(ctx.author.id).get_money()
            if monb == None:
                embed = discord.Embed(description=f"{ctx.author.mention}님은 0원을 소유 중이십니다.", color=tool.Color.green, timestamp=ctx.message.created_at).set_author(name=f"돈")
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(description=f"{ctx.author.mention}님은 {str(monb)}원을 소유 중이십니다.", color=tool.Color.green, timestamp=ctx.message.created_at).set_author(name=f"돈")
                await ctx.channel.send(embed=embed)
        else:
            monb = bank_db.bank(name.id).get_money()
            if monb == None:
                embed = discord.Embed(description=f"{name.mention}님은 0원을 소유 중이십니다.", color=tool.Color.green, timestamp=ctx.message.created_at).set_author(name=f"돈")
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(description=f"{name.mention}님은 {str(monb)}원을 소유 중이십니다.", color=tool.Color.green, timestamp=ctx.message.created_at).set_author(name=f"돈")
                await ctx.channel.send(embed=embed)

    @commands.command(name="돈받기", aliases=["돈지급"], pass_context=True)
    async def give_money(self, ctx):
        if ctx.author.bot is True: return
        TIME = int(time.time())
        time2 = bank_db.bank(ctx.author.id).get_time()
        if time2 is None:
            bank_db.bank(ctx.author.id).update_time(0)
            time2 = 0
        if TIME - time2 < 1800: return await ctx.message.reply(embed=discord.Embed(description=f"{tool.calculation_time(1800 - (TIME - time2))[2]}분 {tool.calculation_time(1800 - (TIME - time2))[3]}초 후에 다시 돈을 받을실수 있습니다!", color=tool.Color.green))
        elif TIME - time2 >= 1800: time2 = int(time.time())
        if bank_db.bank(ctx.author.id).get_money() is None: money = 0
        else: money = bank_db.bank(ctx.author.id).get_money()
        give = random.randrange(1, 2) * random.randrange(1000, 1500)
        money2 = money
        money += give
        await ctx.message.reply(embed=discord.Embed(description=f"{money}원의 돈을 받으셨습니다! 30분후 다시 돈을 받으실수 있습니다!", color=tool.Color.green, timestamp=ctx.message.created_at))
        bank_db.bank(ctx.author.id).update_money(money)
        bank_db.bank(ctx.author.id).update_time(int(time.time()))
        embed = discord.Embed(description=f"{ctx.author.mention}({ctx.author.id})님의 money가 변경되었습니다.\n\n**정보**\n> 변경전 : {money2}원\n> 변경후 : {money}원", color=tool.Color.green).set_author(name="돈 변경/지급", icon_url="https://cdn.discordapp.com/emojis/814717301114798080.png?v=1")
        logwebhook.send(embed=embed)

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    @commands.command(name="송금", pass_context=True)
    async def 송금(self, ctx, name: discord.User=None, msg=None):
        if ctx.author.bot == True: return
        if name is None: return ctx.message.reply(f"보내려는 유저를 입력해주세요!")
        if msg is None: return ctx.message.reply(f"보내려는 유저를 입력해주세요!")
        if name.bot is True: return ctx.message.reply(f"이런! 해당유저는 봇입니다! 봇에게 송금을 할수 없습니다.")
        if name.id == ctx.author.id: return await ctx.message.reply("자기자신에게 송금을 할수없습니다!")
        if msg.isdecimal() is False: return await ctx.message.reply("송금 하려는 금액에는 숫자만 입력할수 있습니다!")
        money_to = bank_db.bank(name.id).get_money()
        money_from = bank_db.bank(ctx.author.id).get_money()
        if money_from is None: return await ctx.message.reply(embed=discord.Embed(description="현재 소유중이신 돈이 없어. 송금할수 없습니다.").set_author(name="송금 실패"))
        msg = int(msg)
        if money_from - msg < 0: return await ctx.message.reply(embed=discord.Embed(description=f"현재 소유중이신 돈이 부족합니다.\n\n현재 잔액 : {str(money_from)}원 입니다.").set_author(name="송금 실패"))
        bank_db.bank(ctx.author.id).update_money(msg, False)
        bank_db.bank(name.id).update_money(msg)
        money_from2 = bank_db.bank(ctx.author.id).get_money()
        money_to2 = bank_db.bank(ctx.author.id).get_money()
        await ctx.channel.send(embed=discord.Embed(description=f"{name.mention}님에게 {str(msg)}송금이 완료되었습니다.\n\n{ctx.author.mention}님의 현재 잔액은 {str(money_from2)}원 입니다.").set_author(name="송금 완료"))
        embed = discord.Embed(description=f"{ctx.author.mention}({ctx.author.id})님의 money가 변경되었습니다.\n\n**정보**\n> 변경 전 : {str(money_from)}원\n> 변경 후 : {str(money_from2)}원\n\n{ctx.author.mention}({ctx.author.id})님의 money가 변경되었습니다.\n\n**정보**\n> 변경 전 : {str(money_to)}원\n> 변경 후 : {str(money_to2)}원", color=tool.Color.green).set_author(name="돈 변경/지급", icon_url="https://cdn.discordapp.com/emojis/814717301114798080.png?v=1")
        logwebhook.send(embed=embed)

def setup(app):
    app.add_cog(Bank(app))
    print("Cogs.Bank Load")