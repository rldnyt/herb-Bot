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
class Developer(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name="eval", help="eval를 실행합니다.", usage=f"{config.BotSettings.prefix}eval [실행하려는 코드]")
    async def eval(self, ctx, *, c=None):
        if not int(ctx.author.id) in config.BotSettings.developer: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')
        if c is None: return await ctx.message.reply(f'eval를 하실 코드도 알려주세요!')
        try: res = eval(str(c))
        except Exception as e:
            embed = discord.Embed(title='Eval',description=f'**📥 입력:**\n```py\n{c}\n```\n**📤 출력:**\n```py\n{e}\n```',color=tool.Color.red)
            return await ctx.channel.send(embed=embed)
        embed = discord.Embed(title='Eval', description=f'**📥 입력:**\n```py\n{c}\n```\n**📤 출력:**\n```py\n{res}\n```\n**type**\n```py\n{type(res)}\n```', color=tool.Color.green)
        await ctx.channel.send(embed=embed)

    @commands.command(name="공지", pass_context=True, help="봇이 접속된서버에 공지를 합니다.", usage=f"{config.BotSettings.prefix}공지 [제목]#[내용]")
    async def 공지(self, ctx):
        if int(ctx.author.id) in config.BotSettings.developer:
            oksv = 0
            msg = ctx.message.content[4:]
            if not msg.split('#')[0]:
                await ctx.channel.send("공지 제목을 입력하세요")
                return
            if not msg.split('#')[1]:
                await ctx.channel.send("공지 내용을 입력하세요")
                return
            embed = discord.Embed(title=msg.split('#')[0],description=msg.split('#')[1] + "\n\nQ. 왜 이곳에 공지가 뜨나요?\nA. 공지채널이 없으면 자동으로 올라감니다. `봇-공지` 이름을 가진 채널을 만들어주세요!\n[[봇 디스코드]](https://discord.gg/TeGYtPc)",colour=tool.Color.yellow, timestamp=ctx.message.created_at)\
                .set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author} | 인증됨 |').set_thumbnail(url=self.app.user.avatar_url_as(format=None, static_format="png", size=1024))
            for i in self.app.guilds:
                arr = [0]
                alla = False
                flag = True
                z = 0
                for j in i.channels:
                    arr.append(j.id)
                    z += 1
                    if "봇-공지" in j.name or "봇_공지" in j.name or "봇공지" in j.name or "bot_announcement" in j.name or "봇-공지사항" in j.name or "봇공지사항" in j.name or "봇_공지사항" in j.name:
                        if str(j.type) == 'text':
                            try:
                                oksv += 1
                                await j.send(embed=embed)
                                alla = True
                            except: pass
                            break
                if alla == False:
                    try:
                        chan = i.channels[1]
                    except: pass
                    if str(chan.type) == 'text':
                        try:
                            oksv += 1
                            await chan.send(embed=embed)
                        except: pass
            await ctx.channel.send(f"**공지 발신결과**\n\n{len(self.app.guilds)}개의 서버 중 {oksv}개의 서버에 발신 완료\n{len(self.app.guilds) - oksv}개의 서버에 발신 실패")
        else: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')

    @commands.command(name="exec", pass_context=True)
    async def exec(self, ctx, *, c=None):
        if not int(ctx.author.id) in config.BotSettings.developer: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')
        if c is None: return await ctx.message.reply(f'eval를 하실 코드도 알려주세요!')
        try: res = exec(str(c))
        except Exception as e:
            embed = discord.Embed(title='Exec',description=f'**📥 입력:**\n```py\n{c}\n```\n**📤 출력:**\n```py\n{e}\n```',color=tool.Color.red)
            return await ctx.channel.send(embed=embed)
        embed = discord.Embed(title='Exec', description=f'**📥 입력:**\n```py\n{c}\n```\n**📤 출력:**\n```py\n{res}\n```\n**type**\n```py\n{type(res)}\n```', color=tool.Color.green)
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True, aliases=["reload"], name="리로드", help="COGS 리로드합니다.", usage=f"{config.BotSettings.prefix}리로드 <리로드 하려는 COG의 이름>")
    async def reload(self, ctx, cog=None):
        if not int(ctx.author.id) in config.BotSettings.developer: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')
        if cog is None:
            v = 0
            try:
                for filename in os.listdir("Cogs"):
                    if filename.endswith(".py"):
                        self.app.reload_extension(f"Cogs.{filename[:-3]}")
                        v += 1
                embed = discord.Embed(title="리로드", description=f"{v}개의 Cog를 리로드 했습니다.", color=tool.Color.green)
                await ctx.channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="리로드", description=f"전체 리로드에 실패하였습니다\n\n**에러내용**```py\n{str(e)}\n```", color=tool.Color.red)
                await ctx.channel.send(embed=embed)
        else:
            try:
                coglist = []
                for filename in os.listdir("Cogs"):
                    if filename.endswith(".py"): coglist.append(str(filename[:-3]))
                if not cog in coglist: return await ctx.message.reply(f'해당 Cog 이름은 없는 Cog 입니다.')
                self.app.reload_extension(f"Cogs.{str(cog)}")
                embed = discord.Embed(title="리로드", description=f"{cog}를 리로드 했습니다.", color=tool.Color.green)
                await ctx.channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="리로드", description=f"{cog} 리로드에 실패하였습니다\n\n**에러 내용**```py\n{str(e)}\n```", color=tool.Color.red)
                await ctx.channel.send(embed=embed)

    @commands.command(name="cmd", pass_context=True)
    async def cmd(self, ctx, *, command:str=None):
        if not int(ctx.author.id) in config.BotSettings.updeveloper: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')
        if command is None: return await ctx.message.reply(f'cmd에서 실행하시려는 것을 입력해주세요!')
        msgs = await ctx.channel.send(embed=discord.Embed(description=f"<a:loing:757075839350341763> 잠시만 기다려주세요!", color=tool.Color.green))
        output = os.popen(command).read()
        embed = discord.Embed(title='CMD',description=f'**📥 입력:**\n```py\n{str(command)}\n```\n**📤 출력:**\n```py\n{str(output)}\n```',color=tool.Color.green)
        await msgs.edit(embed=embed)


    @commands.command(name="pip", aliases=["라이브러리", "모듈"], pass_context=True)
    async def pip(self, ctx, command:str=None,*,command2:str=None):
        if not int(ctx.author.id) in config.BotSettings.updeveloper: return await ctx.message.reply(f'이런! 권한이 없으신것같아요.. 이 명령어는 개발자 명령어 인것같아요.')
        if command is None: return await ctx.message.reply(f'cmd에서 실행하시려는 것을 입력해주세요!')
        if command == "설치" or command == "install":
            if command2 is None: return await ctx.message.reply(f'설치하려는 라이브러리의 이름을 입력해주세요.')
            msg = await ctx.channel.send(embed=discord.Embed(description=f"<a:loing:757075839350341763> 잠시만 기다려주세요! 설치중입니다.", color=tool.Color.green))
            output = os.system(f"pip install {command2}")
            if output == 1: await msg.edit(embed=discord.Embed(title='라이브러리 설치',description=f'`{command2}` 라이브러리 설치에 실패 하였습니다.\n**실패이유**\n```없는 라이브러리 이거나 권한이 없습니다.```',color=tool.Color.green))
            else: await msg.edit(embed=discord.Embed(title='라이브러리 설치',description=f'`{command2}` 라이브러리 설치에 성공 하였습니다.',color=tool.Color.green))
        if command == "info" or command == "list" or command == "정보" or command == "찾기":
            if command2 is None: return await ctx.message.reply(f'찾으려는 라이브러리으 이름을 알려주세요!')
            msg = await ctx.channel.send(embed=discord.Embed(description=f"<a:loing:757075839350341763> 잠시만 기다려주세요! 찾는중입니다.",color=tool.Color.green))
            output = os.popen(f"pip list").read()
            lists = output.split("\n")
            contess = ""
            v2 = 0
            for i in lists:
                if command2 in i:
                    contess += f"{i}\n"
                    v2 += 1
            if len(contess) <= 0: return await msg.edit(embed=discord.Embed(title='라이브러리 찾기',description=f'`{command2}`의 관련된 라이브러리를 찾지 못했습니다.\n대소문자 확인후 다시시도 해보세요!',color=tool.Color.green))
            await msg.edit(embed=discord.Embed(title='라이브러리 찾기',description=f'```py\n{contess}\n```',color=tool.Color.green).set_footer(text=f"{v2}개의 라이브러리가 검색됨."))
        else: await ctx.message.reply(embed=discord.Embed(description=f"`{command}` 라는 모드는 없습니다. 있는 모드는 `정보, 설치`만 있습니다.",color=tool.Color.green))



def setup(app):
    app.add_cog(Developer(app))
    print("Cogs.Developer Load")