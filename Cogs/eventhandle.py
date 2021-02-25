import discord
from discord.ext import commands
import aiohttp
import sqlite3
import string
import random
import tool
import requests
from discord import Webhook, RequestsWebhookAdapter
from config import *

webhook = Webhook.partial(BotSettings.logwebid, BotSettings.logwebtoken, adapter=RequestsWebhookAdapter())


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(color=discord.Color.red(), title="ERROR", timestamp=ctx.message.created_at)
        if isinstance(error, commands.CommandNotFound): return
        elif isinstance(error, commands.CommandOnCooldown): return
        elif isinstance(error, commands.MissingRequiredArgument): return
        elif isinstance(error, commands.MaxConcurrency): return
        elif isinstance(error, commands.CommandOnCooldown): return
        elif isinstance(error, commands.UserNotFound): await ctx.message.reply(embed=discord.Embed(description="해당 유저를 찾지 못했습니다.", color=tool.Color.red, timestamp=ctx.message.created_at))
        elif isinstance(error, commands.MissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages": p = "메시지 관리"
                elif str(p) == "kick_members": p = "멤버 추방"
                elif str(p) == "ban_members": p = "멤버 차단"
                elif str(p) == "administrator": p = "관리자"
                elif str(p) == "create_instant_invite": p = "초대링크 생성"
                elif str(p) == "manage_channels": p = "채널 관리"
                elif str(p) == "manage_guild": p = "서버 관리"
                elif str(p) == "add_reactions": p = "메시지 반응 추가"
                elif str(p) == "view_audit_log": p = "감사 로그 보기"
                elif str(p) == "read_messages": p = "메시지 읽기"
                elif str(p) == "send_messages": p = "메시지 보내기"
                elif str(p) == "read_message_history": p = "이전 메시지 읽기"
                elif str(p) == "mute_members": p = "멤버 음소거 시키기"
                elif str(p) == "move_members": p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname": p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames": p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles": p = "역활 관리하기"
                elif str(p) == "manage_webhooks": p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis": p = "이모지 관리하기"
                elif str(p) == "use_slash_commands": p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]: a += f"> {p}\n"
                else: a += f"> {p}"
            embed = discord.Embed(description=f"이런! 당신은 필요한 권한이 없습니다!\n\n**필요 하는 권한**\n{str(a)}", color=tool.Color.green)
        elif isinstance(error, commands.BotMissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages": p = "메시지 관리"
                elif str(p) == "kick_members": p = "멤버 추방"
                elif str(p) == "ban_members": p = "멤버 차단"
                elif str(p) == "administrator": p = "관리자"
                elif str(p) == "create_instant_invite": p = "초대링크 생성"
                elif str(p) == "manage_channels": p = "채널 관리"
                elif str(p) == "manage_guild": p = "서버 관리"
                elif str(p) == "add_reactions": p = "메시지 반응 추가"
                elif str(p) == "view_audit_log": p = "감사 로그 보기"
                elif str(p) == "read_messages": p = "메시지 읽기"
                elif str(p) == "send_messages": p = "메시지 보내기"
                elif str(p) == "read_message_history": p = "이전 메시지 읽기"
                elif str(p) == "mute_members": p = "멤버 음소거 시키기"
                elif str(p) == "move_members": p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname": p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames": p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles": p = "역활 관리하기"
                elif str(p) == "manage_webhooks": p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis": p = "이모지 관리하기"
                elif str(p) == "use_slash_commands": p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]: a += f"> {p}\n"
                else: a += f"> {p}"
            embed = discord.Embed(description=f"이런! 봇에게 권한이 부족합니다! 아래에 권한을 봇에게 지급 해주세요!\n\n**필요 하는 권한**\n{str(a)}", color=tool.Color.green)
        else:
            if "Unknown Message" in str(error): return
            if "Not connected to voice" in str(error): await ctx.message.reply(embed=discord.Embed(description=f"봇또는 사용자가 음성 채널에 접속이 안되어있는것같아요! 다시 시도해보시겠어요?", color=tool.Color.green))
            embed.add_field(name="버그가 발생했어요!", value="오류내용이 개발팀으로 전송되었습니다! 최대한 빨리 해결하겠습니다!", inline=False)
            webhook.send(f"<@{BotSettings.botowner}>",embed=discord.Embed(color=tool.Color.red, title="⚠ ERROR!",description=f"**오류**\n> ```{str(error)}```\n\n**정보**\n> 사용자 : {ctx.author}\n> └ {ctx.author.mention}\n> └ {ctx.author.id}\n메시지 : {ctx.message.content}"))
        await ctx.message.reply(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"접속한 봇 : {self.bot.user}\n접속한 봇 ID : {self.bot.user.id}")
        webhook.send(embed=discord.Embed(color=tool.Color.green,title="✅ 봇이 작동 되었습니다!", description=f"**디스코드 로그인**\n> 계정 : {self.bot.user}\n> └ {self.bot.user.mention}\n> └ ID : {self.bot.user.id}"))
def setup(bot):
    bot.add_cog(Events(bot))
    print("Cogs.Events Load")
