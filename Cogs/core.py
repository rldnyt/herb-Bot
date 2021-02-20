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
class Core(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name="도움말", aliases=["help", "명령어", "ㅗ디ㅔ", "ehdnaakf", "audfuddj"], help="허브 봇의 모든 명령어들을 확인해요!", usage=f"{config.BotSettings.prefix}도움말 <명령어>\n\n으로 특정 명령어의 사용방법를 알수있습니다.")
    async def help_command(self, ctx, c:str=None):
        if c is None:
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="기본", value="도움말", inline=True)
            embed.add_field(name="개발자", value="eval, 공지, exec, reload, cmd, pip", inline=True)
        elif c == "기본":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 기본",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="도움말 <카테고리 또는 명령어>", value="해당 카테고리의 명령어로를 확인하거나 명령어의 자세한 정보를 확인합니다.", inline=False)
        elif c == "개발자":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 개발자",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="eval [실행하려는 코드]", value="eval 실행합니다.", inline=False)
            embed.add_field(name="exec [실행하려는 코드]", value="exec 실행합니다.", inline=False)
            embed.add_field(name="리로드 <cog파일 이름>", value="cog를 전체 또는 일부를 리로드합니다.", inline=False)
            embed.add_field(name="공지 [제목]#[내용]", value="봇이 접속한 서버에 공지합니다.", inline=False)

        elif c == "도움말" or c == "명령어": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 도움말",description=f"**설명**\n> {self.app.user.name}의 모든 명령어들을 확인할수 있는 명령어 입니다. 특정 카테고리또는 명령어의 자세한 정보를 알수있습니다.\n\n**사용방법**\n> {config.BotSettings.prefix}도움말 <카테고리 또는 명령어>\n\n**필요권한**\n> 없음.", timestamp=ctx.message.created_at, color=tool.Color.green)

        elif c == "eval": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - eval",description=f"**설명**\n> 코드를 실행(테스트)하는 명령어 입니다.\n\n**사용방법**\n> {config.BotSettings.prefix}eval [실행하려는 코드]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "exec": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - exec",description=f"**설명**\n> 코드를 실행(테스트)하는 명령어 입니다.\n\n**사용방법**\n> {config.BotSettings.prefix}exec [실행하려는 코드]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "리로드": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 리로드 <",description=f"**설명**\n> cog을 전체를 리로드하거나 아니면 특정 파일을 리로드합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}리로드 <cog파일 이름>\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "공지": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 공지",description=f"**설명**\n> {self.app.user.name}가 접속된 모든 서버에 공지 메시지를 보냄니다.\n\n**사용방법**\n> {config.BotSettings.prefix}공지 [제목]#[내용]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "cmd": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - cmd",description=f"**설명**\n> {self.app.user.name}의 호스팅에서 cmd 명령어를 실행합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}cmd [명령어]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "모듈" or c == "pip" or c == "라이브러리": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - pip",description=f"**설명**\n> {self.app.user.name}의 파이썬에서 라이브러리를 관리합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}라이브러리 [모드] [모드의 따라 다름]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)

        else: return await ctx.message.reply(f"`{c}` 카테고리 또는 명령어가 존제 하지 않습니다.")
        await ctx.channel.send(embed=embed.set_footer(text=f"{config.BotSettings.prefix}도움말 <카테고리 또는 명령어> 로 자세하게 알수 있어요!").set_footer(text="[]는 필수, <>는 선택 입니다.").set_thumbnail(url=self.app.user.avatar_url))

    @commands.command(name="봇정보", aliases=["봇 정보" , "botinfo" ,"BotInfo"], help="봇의 정보를 확인합니다.")
    async def botinfo(self, ctx):
        developers = ""
        for i in config.BotSettings.developer:
            users = self.app.get_user(i)
            developers += f"> {users}({users.mention})\n"
        embed = discord.Embed(title=f"{self.app.user.name}의 정보", color=tool.Color.green)
        embed.set_thumbnail(url=self.app.user.avatar_url)
        embed.add_field(name="🛠️ 개발자", value=developers, inline=False)
        embed.add_field(name="📝 봇 이름", value=self.app.user.name, inline=True)
        embed.add_field(name="📃 봇 버전", value="Bata 1.0.0 - 2021 02 20 release", inline=True)
        embed.add_field(name="🔗 봇 링크", value="준비중입니다!", inline=False)
        await ctx.channel.send(embed=embed)


def setup(app):
    app.add_cog(Core(app))
    print("Cogs.Core Load")