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
import ast
import sqlite3
class Log(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True: return
        if not message.attachments: return
        conn = sqlite3.connect(f"{config.BotSettings.dbname}.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (message.guild.id,)))
        conn.close()
        if not table: return
        if ".png" in message.attachments[0].filename:
            im = message.attachments[0]
            channel = self.app.get_channel(table[0][0])
            embed = discord.Embed(title="이미지 업로드", description=f"{message.author.mention}님이 {message.channel.mention}에 사진을 올리셨습니다.\n[[ 해당글 바로가기 ]]({message.jump_url})\n\n**업로드된 사진**", color=tool.Color.green, timestamp=message.created_at).set_footer(text=f"{message.author}").set_image(url=im.url)
        else: embed = discord.Embed(title="이미지 업로드",description=f"{message.author.mention}님이 {message.channel.mention}에 파일을 올리셨습니다.\n\n[[ 해당글 바로가기 ]]({message.jump_url})",color=tool.Color.green, timestamp=message.created_at).set_footer(text=f"{message.author}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (message.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        ct2 = 0
        if not message.attachments: pass
        else: ct2, im = 1, message.attachments[0]
        channel = self.app.get_channel(channelid)
        codea = random.randint(1, 9999999999999999)
        html_file = open(f'./txt/{codea}.txt', 'w', encoding='utf-8')
        html_file.write(message.content)
        html_file.close()
        if ct2 == 0:
            if len(message.content) >= 1024:
                file = discord.File(f'./txt/{codea}.txt', filename=f'{codea}.txt')
                embed = discord.Embed(file=file, title="메시지 삭제",description=f"{message.channel.mention}에서 {message.author.mention} 님이 보내신 메시지가 삭제되었습니다!\n채널 : {message.channel.mention}({message.channel.id})",color=tool.Color.red, timestamp=message.created_at).set_footer(text=f"{message.author}").set_thumbnail(url=message.author.avatar_url).add_field(name="삭제된 메시지", value="(너무 길어 가져올수 없습니다. 아래의 txt파일을 확인해주세요.)", inline=True)
                os.remove(f'./txt/{codea}.txt')
            else: embed = discord.Embed(title="메시지 삭제",description=f"{message.channel.mention}에서 {message.author.mention} 님이 보내신 메시지가 삭제되었습니다!\n채널 : {message.channel.mention}({message.channel.id})",color=tool.Color.red, timestamp=message.created_at).set_footer(text=f"{message.author}").set_thumbnail(url=message.author.avatar_url).add_field(name="삭제된 메시지",value=message.content,inline=True)
        else: embed = discord.Embed(title="메시지 삭제",description=f"{message.channel.mention}에서 {message.author.mention} 님이 보내신 이미지가 삭제되었습니다!\n채널 : {message.channel.mention}({message.channel.id})\n**삭제된 이미지**",color=tool.Color.red, timestamp=message.created_at).set_footer(text=f"{message.author}").set_thumbnail(url=message.author.avatar_url).set_image(url=im.url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot == True: return
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (before.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        filess = []
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="메세지 수정", description=f"{before.channel.mention}에서 {before.author.mention} 님이 메시지을 수정하셨습니다!\n[[ 이동하기 ]](https://discordapp.com/channels/{before.guild.id}/{before.channel.id}/{before.id})", color=tool.Color.yellow, timestamp=before.created_at).set_footer(text=f"{before.author}").set_thumbnail(url=before.author.avatar_url)
        if len(before.content) <= 1024: embed.add_field(name="전(Before)", value=before.content, inline=False)
        else: embed.add_field(name="전(Before)", value="(너무 길어요!)", inline=False)
        if len(after.content) <= 1024:
            codea = random.randint(1, 9999999999999999)
            html_file = open(f'./txt/Before_{codea}.txt', 'w', encoding='utf-8')
            html_file.write(before.content)
            html_file.close()
            file = discord.File(f'./txt/Before_{codea}.txt', filename=f'Before_{codea}.txt')
            filess.append(file)
            embed.add_field(name="전(Before)", value="(너무 길어요! 아래의 txt를 확인하세요!)", inline=False)
            os.remove(f'./txt/Before_{codea}.txt')
        else:
            codea = random.randint(1, 9999999999999999)
            html_file = open(f'./txt/After_{codea}.txt', 'w', encoding='utf-8')
            html_file.write(after.content)
            html_file.close()
            file = discord.File(f'./txt/After_{codea}.txt', filename=f'After_{codea}.txt')
            filess.append(file)
            embed.add_field(name="후(After)", value="(너무 길어요! 아래의 txt를 확인하세요!)", inline=False)
            os.remove(f'./txt/After_{codea}.txt')
        await channel.send(files=filess, embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (before.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="멤버 수정",description=f"{before.mention}님의 이름또는 역활이 수정되었습니다!",color=tool.Color.yellow, timestamp=before.created_at).set_footer(text=f"{before}").set_thumbnail(url=before.avatar_url)
        if not before.display_name == after.display_name:
            embed.add_field(name="서버이름변경 전(Before)", value=before.display_name, inline=True)
            embed.add_field(name="서버이름변경 후(After)", value=after.display_name, inline=True)
        if not before.roles == after.roles:
            b,a = '',''
            if len(before.roles) <= 1: b = "역활이 없어요"
            if len(after.roles) <= 1: a = "역활이 없어요"
            if len(before.roles) > 1:
                for i in before.roles:
                    if str(i) == "@everyone":
                        continue
                    b += f"{i.mention}\n"
            if len(after.roles) > 1:
                for i in after.roles:
                    if str(i) == "@everyone":
                        continue
                    a += f"{i.mention}\n"
            embed.add_field(name="역활 전(Before)", value=b, inline=True)
            embed.add_field(name="역활 후(After)", value=a, inline=True)

        if not before.roles == after.roles or not before.display_name == after.display_name:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (role.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="역활 생성",description=f"{role.mention}역활이 생성되었습니다.",color=tool.Color.green, timestamp=role.created_at)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (before.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        gid = f[1]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="역활 수정",description=f"역활이름 : {before.mention}",color=tool.Color.yellow, timestamp=before.created_at).set_footer(text=f"{before}")
        if not before.name == after.name:
            embed.add_field(name="이름변경 전(Before)", value=before.name, inline=False)
            embed.add_field(name="이름변경 후(After)", value=after.name, inline=False)
        if not before.permissions == after.permissions:
            embed.add_field(name="변경된점", value="역활의 권한이 수정됨.", inline=False)
        if not before.color == after.color:
            embed.add_field(name="역활색변경 전(Before)", value=before.color, inline=False)
            embed.add_field(name="역활색변경 후(After)", value=after.color, inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="서버 차단", description=f"{user.mention}님이 {guild.name}에서 차단당했습니다.", color=tool.Color.red, timestamp=user.created_at).set_footer(text=f"{user}").set_thumbnail(url=user.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="서버 차단 해제", description=f"{user.mention}님의 차단이 해제되었습니다.", color=tool.Color.red, timestamp=user.created_at).set_footer(text=f"{user}").set_thumbnail(url=user.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (invite.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        if invite.temporary == True: apaqj = "⭕"
        else: apaqj = "❌"
        if invite.max_age == 0: asdf = "만료되지 않음"
        else: asdf = f"{invite.max_age}초후 만료됨"
        if invite.max_uses == 0: adfa = "무한"
        else: adfa = f"{invite.max_uses}번"
        embed = discord.Embed(title="서버 초대링크 생성", description=f"{invite.inviter.mention}님이 초대 링크를 생성했습니다.\n\n초대 채널 : {invite.channel.mention}\n사용가능횟수 : {adfa}\n임시 멤버 자격 : {apaqj}\n만료되는시간 : {asdf}", color=tool.Color.green, timestamp=invite.created_at).set_footer(text=f"{invite}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        conn = sqlite3.connect("databass.db")
        cur = conn.cursor()
        table = list(cur.execute('SELECT * FROM logchannel WHERE guildid=?', (invite.guild.id,)))
        conn.close()
        if not table: return
        f = table[0]
        channelid = f[0]
        channel = self.app.get_channel(channelid)  # 시스템 건의
        embed = discord.Embed(title="서버 초대링크 삭제", description=f"`{invite}` 초대링크가 삭제되었습니다.", color=tool.Color.red, timestamp=invite.created_at).set_footer(text=f"{invite}")
        await channel.send(embed=embed)

def setup(app):
    app.add_cog(Log(app))
    print("Cogs.Log Load")