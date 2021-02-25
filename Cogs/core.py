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
import json
class Core(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name="도움말", aliases=["help", "명령어", "ㅗ디ㅔ", "ehdnaakf", "audfuddj"], help="허브 봇의 모든 명령어들을 확인해요!", usage=f"{config.BotSettings.prefix}도움말 <명령어>\n\n으로 특정 명령어의 사용방법를 알수있습니다.")
    async def help_command(self, ctx, c:str=None):
        if c is None:
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="✨ 기본", value="도움말, 봇정보, 뉴스", inline=True)
            embed.add_field(name="🛠 개발자", value="eval, 공지, reload, cmd, pip", inline=True)
            embed.add_field(name="📔 서버", value="채팅청소, 슬로우, 로그", inline=True)
            embed.add_field(name="🎮 게임", value="타자", inline=True)
            embed.add_field(name="🎶 뮤직", value="재생, 반복, 랜덤, 스킵, 정지, 일시정지, 계속재생, 볼륨, 재생목록", inline=False)

        elif c == "서버":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 서버",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="채팅청소 [청소하려는 수]", value="명령어를 실행한 채널에 청소수 만큼 채팅을 삭제합니다.", inline=False)
            embed.add_field(name="슬로우 [설정하려는 딜레이]", value="명령어를 사용한 채널의 슬로우를 설정합니다.", inline=False)
            embed.add_field(name="로그 <채널>", value="로그 채널을 확인합니다.", inline=False)

        elif c == "게임":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 게임",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="타자 [모드] [언어]", value="타자게임을 실행합니다! 베타기능.", inline=False)

        elif c == "뮤직" or c == "음성" or c == "음악":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 재생",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="재생 [URL 또는 이름]", value="곡을 재생합니다!", inline=False)
            embed.add_field(name="반복", value="곡를 재생할때 해당 곡을 반복 재생합니다.", inline=False)
            embed.add_field(name="랜덤", value="곡를 등록한 재생목록중 곡들을 랜덤으로 재생합니다.", inline=False)
            embed.add_field(name="스킵", value="현재 재생중인 곡를 멈추고 다음곡을 재생합니다.", inline=False)
            embed.add_field(name="정지", value="현재 재생목록을 제거 곡재생을 종료합니다.", inline=False)
            embed.add_field(name="일시정지", value="현재 재생를 일시정지합니다.", inline=False)
            embed.add_field(name="계속재생", value="일시정지일때 다시 재생을 합니다.", inline=False)
            embed.add_field(name="볼륨", value="현재 재생중인 곡의 볼륨을 조정합니다.", inline=False)
            embed.add_field(name="재생목록", value="현재의 재생목록을 확인합니다.", inline=False)

        elif c == "기본":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 기본",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="도움말 <카테고리 또는 명령어>", value="해당 카테고리의 명령어로를 확인하거나 명령어의 자세한 정보를 확인합니다.", inline=False)
            embed.add_field(name="봇정보", value="봇의 정보를 확인해요.", inline=False)
            embed.add_field(name="뉴스", value="경제 시스템 뉴스나 봇의 업데이트 뉴스를 확인해요!", inline=False)

        elif c == "개발자":
            embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 개발자",description=f"접두사는 `{config.BotSettings.prefix}`입니다! 명령어 사용시 앞에 {config.BotSettings.prefix}를 붙혀주세요\n(예: {config.BotSettings.prefix}도움말)",  timestamp=ctx.message.created_at, color=tool.Color.green)
            embed.add_field(name="eval [실행하려는 코드]", value="eval 실행합니다.", inline=False)
            embed.add_field(name="exec [실행하려는 코드]", value="exec 실행합니다.", inline=False)
            embed.add_field(name="리로드 <cog파일 이름>", value="cog를 전체 또는 일부를 리로드합니다.", inline=False)
            embed.add_field(name="공지 [제목]#[내용]", value="봇이 접속한 서버에 공지합니다.", inline=False)

        elif c == "도움말" or c == "명령어": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 도움말",description=f"**설명**\n> {self.app.user.name}의 모든 명령어들을 확인할수 있는 명령어 입니다. 특정 카테고리또는 명령어의 자세한 정보를 알수있습니다.\n\n**사용방법**\n> {config.BotSettings.prefix}도움말 <카테고리 또는 명령어>\n\n**필요권한**\n> 없음.", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "봇정보" or c == "botinfo": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 봇정보",description=f"**설명**\n> {self.app.user.name}의 정보를 알수있습니다.\n\n**사용방법**\n> {config.BotSettings.prefix}봇정보\n\n**필요권한**\n> 없음.", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "뉴스" or c == "업데이트": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 뉴스",description=f"**설명**\n> 경제 시스템의 소식을 알거나 봇의 업데이트 정보를 확인할수 있어요!\n\n**사용방법**\n> {config.BotSettings.prefix}뉴스\n\n**필요권한**\n> 없음.", timestamp=ctx.message.created_at, color=tool.Color.green)

        elif c == "eval": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - eval",description=f"**설명**\n> 코드를 실행(테스트)하는 명령어 입니다.\n\n**사용방법**\n> {config.BotSettings.prefix}eval [실행하려는 코드]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "리로드": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 리로드 <",description=f"**설명**\n> cog을 전체를 리로드하거나 아니면 특정 파일을 리로드합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}리로드 <cog파일 이름>\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "공지": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 공지",description=f"**설명**\n> {self.app.user.name}가 접속된 모든 서버에 공지 메시지를 보냄니다.\n\n**사용방법**\n> {config.BotSettings.prefix}공지 [제목]#[내용]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "cmd": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - cmd",description=f"**설명**\n> {self.app.user.name}의 호스팅에서 cmd 명령어를 실행합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}cmd [명령어]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "모듈" or c == "pip" or c == "라이브러리": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - pip",description=f"**설명**\n> {self.app.user.name}의 파이썬에서 라이브러리를 관리합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}라이브러리 [모드] [모드의 따라 다름]\n\n**필요권한**\n> {self.app.user.name}의 개발자", timestamp=ctx.message.created_at, color=tool.Color.green)

        elif c == "채팅청소" or c == "clear": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 채팅청소",description=f"**설명**\n> 현재 채팅방의 원하는 수 만큼 채팅를 삭제합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}채팅청소 [삭제하려는 수]\n\n**필요권한**\n> 메시지 관리권한.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "슬로우" or c == "slowmode" or c == "슬로우모드" or c == "딜레이": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 슬로우",description=f"**설명**\n> 명령어를 사용한 채널에 슬로우 모드를 설정합니다. 설정한 시간은 초단위입니다.\n\n**사용방법**\n> {config.BotSettings.prefix}슬로우 [설정하려는 딜레이]\n\n**필요권한**\n> 메시지 관리권한.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "로그": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 로그",description=f"**설명**\n> 로그 채널을 설정합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}로그 <채널멘션 또는 채널의 ID 또는 삭제>\n\n`{config.BotSettings.prefix}로그 삭제`를 할경우 로그를 끌수있습니다.\n\n**필요권한**\n> 서버 관리권한.",timestamp=ctx.message.created_at, color=tool.Color.green)

        elif c == "재생" or c == "play": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 재생",description=f"**설명**\n> 접속된 음성채널에서 노래를 재생합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}재생 [URL 또는 이름]\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "루프" or c == "반복": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 반복",description=f"**설명**\n> 곡를 재생할때 해당 곡을 반복 재생합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}반복\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "셔플" or c == "랜덤": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 랜덤",description=f"**설명**\n> 곡를 등록한 재생목록중 곡들을 랜덤으로 재생합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}랜덤\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "스킵" or c == "skip": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 스킵",description=f"**설명**\n> 현재 재생중인 곡를 멈추고 다음곡을 재생합니다. 다음곡이 없으면 재생을 종료합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}스킵\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "정지" or c == "stop": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 정지",description=f"**설명**\n> 현재 재생목록을 제거 곡재생을 종료합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}정지\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "일시정지": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 일시정지",description=f"**설명**\n> 현재 재생를 일시정지합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}일시정지\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "계속재생": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 계속재생",description=f"**설명**\n> 일시정지일때 이어서 다시 재생을 합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}다시재생\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "볼륨": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 볼륨",description=f"**설명**\n> 현재 재생중인 곡의 볼륨을 조정합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}볼륨 [지정하려는 볼륨]\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)
        elif c == "재생목록": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 재생목록",description=f"**설명**\n> 현재의 재생목록을 확인합니다.\n\n**사용방법**\n> {config.BotSettings.prefix}재생목록\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)

        elif c == "타자": embed = discord.Embed(title=f"{self.app.user.name}의 도움말 - 타자",description=f"**설명**\n> 타자 게임을 실행합니다!\n\n**사용방법**\n> {config.BotSettings.prefix}타자 [모드] [언어]\n```모드 안내\n\n솔로: 명령어를 사용한 유저만 타자게임을 합니다.```\n```언어 안내\n한국어 : 한국어 타자를 합니다.```\n\n배타기능.\n\n**필요권한**\n> 없음.",timestamp=ctx.message.created_at, color=tool.Color.green)

        else: return await ctx.message.reply(f"`{c}` 카테고리 또는 명령어가 존제 하지 않습니다.")
        await ctx.channel.send(embed=embed.set_footer(text=f"{config.BotSettings.prefix}도움말 <카테고리 또는 명령어> 로 자세하게 알수 있어요!").set_footer(text="[]는 필수, <>는 선택 입니다.").set_thumbnail(url=self.app.user.avatar_url))

    @commands.command(name="봇정보", aliases=["봇 정보" , "botinfo" ,"BotInfo"], help="봇의 정보를 확인합니다.")
    async def botinfo(self, ctx):
        developers = ""
        for i in config.BotSettings.developer: developers += f"> {self.app.get_user(i)}({self.app.get_user(i).mention})\n"
        embed = discord.Embed(title=f"{self.app.user.name}의 정보", color=tool.Color.green)
        embed.set_thumbnail(url=self.app.user.avatar_url)
        embed.add_field(name="🛠️ 개발자", value=developers, inline=False)
        embed.add_field(name="📝 봇 이름", value=self.app.user.name, inline=True)
        embed.add_field(name="📃 봇 버전", value="Bata 0.8 - 2021 02 25 release", inline=True)
        embed.add_field(name="📡 접속 서버 수 / 유저 수", value=f"{len(self.app.guilds)}서버 / {len(self.app.users)}명", inline=True)
        embed.add_field(name="🔗 봇 링크", value="[<:github_icon:813986156819644497> <:github_1:813986156839698482><:github_2:813986156659081256><:github_3:813986156685033552>](https://github.com/rldnyt/herb-Bot)", inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command(name="뉴스", aliases=["News" , "news" ,"기사", "신문", "업데이트"])
    async def news(self, ctx):
        msg = await ctx.channel.send(embed=discord.Embed(description="<a:loading2:813962181699436554> 뉴스를 불러오는 중입니다.", color=tool.Color.green))
        with open('news.json', encoding='UTF8') as f: newsjson = json.load(f)
        page = []
        if not newsjson or len(newsjson) <= 0: return await msg.edit(embed=discord.Embed(description="뉴스가 없습니다.", color=tool.Color.green))
        for i in newsjson:
            pagsdata = newsjson[i]
            embed = discord.Embed(title=pagsdata["title"], description=pagsdata["content"], color=tool.Color.green).set_author(name=pagsdata["news_name"], icon_url=pagsdata["news_icon"])
            page.append(embed)

        page2 = int(len(page)) - 1
        await msg.edit(embed=page[0].set_footer(text=f"페이지 : 1/{len(page)}"))
        if len(page) > 1:
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            i = 0
            while True:
                try:
                    reaction, user = await self.app.wait_for('reaction_add',timeout=60.0)  # Gets the reaction and the user with a timeout of 30 seconds + new Syntax
                    if user == ctx.author:  # Test if the user is the author
                        emoji = str(reaction.emoji)
                        if emoji == '◀':
                            if i > 0:
                                i -= 1
                                await msg.edit(embed=page[i].set_footer(text=f"페이지 : {i + 1}/{len(page)}"))
                            await msg.remove_reaction(reaction, user)
                        elif emoji == '▶':
                            if i < page2:
                                i += 1
                                await msg.edit(embed=page[i].set_footer(text=f"페이지 : {i + 1}/{len(page)}"))
                            await msg.remove_reaction(reaction, user)
                except TimeoutError: break
            await msg.clear_reactions()


def setup(app):
    app.add_cog(Core(app))
    print("Cogs.Core Load")