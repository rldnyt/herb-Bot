import discord
import time
import asyncio
import random
from discord.ext import commands
from utils import get_youtube
from utils import page
from utils import confirm
import tool
from discord import Webhook, RequestsWebhookAdapter
import config

webhook = Webhook.partial(config.BotSettings.logwebid, config.BotSettings.logwebtoken, adapter=RequestsWebhookAdapter())

loop = asyncio.get_event_loop()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    async def queue_task(self, ctx: commands.Context, voice: discord.VoiceClient):
        bot = self.bot
        while True:
            if str(ctx.guild.id) not in self.queues.keys():
                await ctx.send(f"`{voice.channel}`채널에서 나갈게요!")
                await voice.disconnect(force=True)
                break
            queue = self.queues[str(ctx.guild.id)]
            if voice.is_playing() or voice.is_paused():
                await asyncio.sleep(1)
                continue
            elif not voice.is_playing() and len(queue.keys()) == 1 and queue["playing"]["loop"] is not True:
                await ctx.send(f"음.. 재생할곡이 없네요 `{voice.channel}`채널에서 나갈게요!")
                await voice.disconnect(force=True)
                break
            vol = queue["playing"]["vol"]
            if queue["playing"]["loop"] is True:
                tgt_url = queue["playing"]["tgt_url"]
                voice.play(discord.FFmpegPCMAudio(tgt_url, before_options=get_youtube.before_args))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = vol
                await asyncio.sleep(3)
                continue
            if queue["playing"]["random"]:
                queue_keys = [str(x) for x in queue.keys() if not x == "playing"]
                tgt_name = str(random.choice(queue_keys))
                tgt_queue = queue[tgt_name]
            else:
                tgt_name = list(queue.keys())[1]
                tgt_queue = queue[tgt_name]
            vid_url = tgt_queue["vid_url"]
            vid_title = tgt_queue["vid_title"]
            vid_author = tgt_queue["vid_author"]
            vid_channel_url = tgt_queue["vid_channel_url"]
            tgt_url = tgt_queue["tgt_url"]
            thumb = tgt_queue["thumb"]
            req_by = bot.get_user(int(tgt_queue["req_by"]))
            voice.play(discord.FFmpegPCMAudio(tgt_url, before_options=get_youtube.before_args))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = vol
            embed = discord.Embed(title="유튜브 음악 재생", color=tool.Color.yellow)
            embed.add_field(name="재생 시작",
                            value=f"업로더: [`{vid_author}`]({vid_channel_url})\n제목: [`{vid_title}`]({vid_url})",
                            inline=False)
            embed.add_field(name="재생 요청자", value=f"{req_by.mention}\n`{req_by}`)", inline=True)
            embed.set_image(url=str(thumb))
            queue["playing"]["vid_url"] = vid_url
            queue["playing"]["vid_title"] = vid_title
            queue["playing"]["vid_author"] = vid_author
            queue["playing"]["vid_channel_url"] = vid_channel_url
            queue["playing"]["thumb"] = thumb
            queue["playing"]["tgt_url"] = tgt_url
            queue["playing"]["req_by"] = tgt_queue["req_by"]
            await ctx.send(embed=embed)
            del queue[tgt_name]
            await asyncio.sleep(3)

    @staticmethod
    async def check_voice(ctx: commands.Context, resume=False):
        voice = ctx.voice_client
        user_voice = ctx.message.author.voice
        if user_voice is None:
            await ctx.send(f"{ctx.author.mention}님! 먼저 음성채널에 들어와주세요!")
            return False
        if voice is None:
            await ctx.send(f"{ctx.author.mention}님 재생을 먼저해주세요!")
            return False
        if not voice.is_playing():
            if resume is True:
                return True
            await ctx.send(f"{ctx.author.mention}님! 현재 재생중인 곡이 없습니다!")
            return None
        return True

    @commands.command(name="재생", description="음악을 재생합니다.", aliases=["play", "p", "ㅔ", "대기", "queue", "q", "ㅂ"])
    async def play(self, ctx, *, url):
        try:
            msg = await ctx.send(f"해당곡을 로드중이에요! 기다려주세요!")
            embed = discord.Embed(title="유튜브 음악 재생", color=tool.Color.yellow)
            user_voice = ctx.message.author.voice
            if user_voice is None:
                return await msg.edit(content=f"{ctx.author.mention} 먼저 음성채널에 들어와주세요!")
            voice_channel = user_voice.channel
            if voice_channel is None or voice_channel is False:
                return await msg.edit(content=f"{ctx.author.mention} 먼저 음성채널에 들어와주세요!")
            voice = ctx.voice_client
            if voice is None:
                await voice_channel.connect()
                voice = ctx.voice_client
            if not voice.is_playing() and not voice.is_paused():
                self.queues[str(ctx.guild.id)] = {}
            queue = self.queues[str(ctx.guild.id)]
            search_res = await get_youtube.get_youtube(url)
            vid_url = search_res["webpage_url"]
            vid_title = search_res["title"]
            vid_author = search_res["uploader"]
            vid_channel_url = search_res["uploader_url"]
            tgt_url = search_res["formats"][0]["url"]
            thumb = search_res["thumbnail"]
            default_vol = 0.3
            embed.set_thumbnail(url=str(thumb))
            if voice.is_playing():
                current_time = round(time.time())
                queue[str(current_time)] = {}
                queue[str(current_time)]["vid_url"] = vid_url
                queue[str(current_time)]["vid_title"] = vid_title
                queue[str(current_time)]["vid_author"] = vid_author
                queue[str(current_time)]["vid_channel_url"] = vid_channel_url
                queue[str(current_time)]["thumb"] = thumb
                queue[str(current_time)]["tgt_url"] = tgt_url
                queue[str(current_time)]["req_by"] = ctx.author.id
                embed.add_field(name="재생 목록에 추가",value=f"업로더: [`{vid_author}`]({vid_channel_url})\n제목: [`{vid_title}`]({vid_url})",inline=False)
                embed.add_field(name="재생 요청자", value=f"{ctx.author.mention}\n(`{ctx.author}`)", inline=True)
                return await msg.edit(content="", embed=embed)
            voice.play(discord.FFmpegPCMAudio(tgt_url, before_options=get_youtube.before_args))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = default_vol
            embed.add_field(name="재생 시작",
                            value=f"업로더: [`{vid_author}`]({vid_channel_url})\n제목: [`{vid_title}`]({vid_url})",
                            inline=False)
            embed.add_field(name="재생 요청자", value=f"{ctx.author.mention}\n(`{ctx.author}`)", inline=True)
            await msg.edit(content="", embed=embed)
            queue["playing"] = {}
            queue["playing"]["vid_url"] = vid_url
            queue["playing"]["vid_title"] = vid_title
            queue["playing"]["vid_author"] = vid_author
            queue["playing"]["vid_channel_url"] = vid_channel_url
            queue["playing"]["thumb"] = thumb
            queue["playing"]["tgt_url"] = tgt_url
            queue["playing"]["vol"] = default_vol
            queue["playing"]["req_by"] = ctx.author.id
            queue["playing"]["loop"] = False
            queue["playing"]["random"] = False
            await asyncio.create_task(self.queue_task(ctx, voice))
        except Exception as ex:
            if "Unable to extract video data" in str(ex):
                embed = discord.Embed(title="ERROR!", description="이런! 버그가 일어났어요! 무슨 버그인지 아래을 확인해보세요!", color=tool.Color.red)
                embed.add_field(name="이런! 유튜브에서 막혔어요!", value="이런! 이건 유튜브측에서 막은것이기에 개발자도 어떻게 할수가 없어요.. 다시한번 해보세요!", inline=False)
                webhook.send(embed=discord.Embed(color=tool.Color.red, title="⚠ ERROR!",description=f"**오류**\n> ```{str(ex)}```\n\n**정보**\n> 사용자 : {ctx.author}\n> └ {ctx.author.mention}\n> └ {ctx.author.id}\n> 서버 : {ctx.guild.name}"))
            else:
                embed = discord.Embed(title="ERROR!", description="이런! 버그가 일어났어요! 무슨 버그인지 아래을 확인해보세요!", color=tool.Color.red)
                embed.add_field(name="알수 없는 버그!", value="이런! 이건 유튜브측에서 막은것이기에 개발자도 어떻게 할수가 없어요.. 다시한번 해보세요!", inline=False)
                webhook.send(embed=discord.Embed(color=tool.Color.red, title="⚠ ERROR!",description=f"**오류**\n> ```{str(ex)}```\n\n**정보**\n> 사용자 : {ctx.author}\n> └ {ctx.author.mention}\n> └ {ctx.author.id}\n> 서버 : {ctx.guild.name}"))
            await ctx.channel.send(embed=embed)


    @commands.command(name='루프', description="현재 재생중인 곡을 루프해요!", aliases=["무한반복", "loop", "repeat", "반복"])
    async def music_loop(self, ctx):
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        queue = self.queues[str(ctx.guild.id)]
        if queue["playing"]["loop"] is not True:
            msg = await ctx.send(f"{ctx.author.mention} 🔁 이 곡을 무한반복을 활성화할까요?")
            res = await confirm.confirm(self.bot, ctx, msg)
            if res is not True:
                return await msg.edit(content=f"{ctx.author.mention} 무한반복을 취소했어요! 이노래을 무한반복 하지않을게요!")
            queue["playing"]["loop"] = True
            return await msg.edit(content=f"{ctx.author.mention} 🔁 이 곡을 무한반복을 할게요! 이제 이노래가 계속 재생될거에요!")
        elif queue["playing"]["loop"] is True:
            msg = await ctx.send(f"{ctx.author.mention} 🔁 이 곡을 무한반복을 비활성화할까요?")
            res = await confirm.confirm(self.bot, ctx, msg)
            if res is not True:
                return await msg.edit(content=f"{ctx.author.mention} 무한반복 비활성을 취소했어요! 노래을 계속 반복할게요!")
            queue["playing"]["loop"] = False
            return await msg.edit(content=f"{ctx.author.mention} 이곡을 무한반복을 비활성화했어요! 이제 다른곡들도 재생할게요!")

    @commands.command(name="셔플", description="대기 리스트에서 음악을 무작위로 재생합니다.", aliases=["랜덤", "random", "shuffle", "sf", "ㄶ", "ㄴㅎ"])
    async def shuffle(self, ctx):
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        queue = self.queues[str(ctx.guild.id)]
        if queue["playing"]["random"] is not True:
            msg = await ctx.send(f"{ctx.author.mention} 🔀랜덤기능을 활성화할까요?")
            res = await confirm.confirm(self.bot, ctx, msg)
            if res is not True:
                return await msg.edit(content=f"{ctx.author.mention} 랜덤 기능 활성화를 취소했어요! 재생목록순서대로 재생될거에요!")
            queue["playing"]["random"] = True
            return await msg.edit(content=f"{ctx.author.mention} 🔀랜덤기능을 활성화했어요! 이제노래가 랜덤으로 나올거에요!")
        elif queue["playing"]["random"] is True:
            msg = await ctx.send(f"{ctx.author.mention} 랜덤기능을 비활성화할까요?")
            res = await confirm.confirm(self.bot, ctx, msg)
            if res is not True:
                return await msg.edit(content=f"{ctx.author.mention} 렌덤기능 비활성화를 취소했어요! 랜덤으로 계속 재생될거에요!")
            queue["playing"]["random"] = False
            return await msg.edit(content=f"{ctx.author.mention} 랜덤기능이 비활성화되었어요! 이제 노래가 재생목록순서대로 재생될거에요!")

    @commands.command(name="스킵", description="재생중인 음악을 스킵합니다.", aliases=["s", "skip", "ㄴ"])
    async def skip(self, ctx):
        voice = ctx.voice_client
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        voice.stop()

    @commands.command(name="정지", description="음악 재생을 멈춥니다.", aliases=["stop", "ㄴ새ㅔ", "멈춰"])
    async def stop(self, ctx):
        voice = ctx.voice_client
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        del self.queues[str(ctx.guild.id)]
        voice.stop()

    @commands.command(name="일시정지", description="음악을 일시정지합니다.", aliases=["pause", "ps", "ㅔㄴ"])
    async def pause(self, ctx):
        voice = ctx.voice_client
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        voice.pause()
        await ctx.send(f"{ctx.author.mention} ⏸ 노래재생을 일시정지했어요! 다시 계속이어서 듣고싶으면 `!다시재생`을 입력해봐요!")

    @commands.command(name="계속재생", description="음악 일시정지를 해제합니다.", aliases=["resume", "r", "ㄱ", "다시재생"])
    async def resume(self, ctx):
        voice = ctx.voice_client
        voice_ok = await self.check_voice(ctx, resume=True)
        if voice_ok is None:
            pass
        elif not voice_ok:
            return
        voice.resume()
        await ctx.send(f"{ctx.author.mention} ▶ 일시정지인 노래재생을 이어서 다시 재생할게요!")

    @commands.command(name="강제연결해제", description="봇 오류로 음악 재생에 문제가 발생했을 때 강제로 접속을 해제합니다.", aliases=["나가", "제발나가", "quit", 'leave', 'l', "ㅣ", "dc"])
    async def force_quit(self, ctx):
        voice = ctx.voice_client
        await voice.disconnect(force=True)
        await ctx.send(f"🚫 {self.bot.user.name}을 강제로 음성채널에서 나갔습니다!")

    @commands.command(name="볼륨", description="음악의 볼륨을 조절합니다.", aliases=["volume", "vol", "v", "패ㅣㅕㅡㄷ", "ㅍ"])
    async def volume(self, ctx, vol: int = None):
        if vol > 100:
            return await ctx.send(f"숫자가 너무 작아요! {ctx.author}님의 귀를 보호하기 위해서 100이상으로는 볼륨을 조절하지못해요!")
        if vol <= 0:
            return await ctx.send("숫자가 너무 작아요! 노래을 듣고 싶으신건가요..?")
        queue = self.queues[str(ctx.guild.id)]
        voice_ok = await self.check_voice(ctx)
        if not voice_ok:
            return
        current_vol = float(queue["playing"]["vol"])
        if vol is None:
            return await ctx.send(f"{ctx.author.mention} 현재 볼륨은 `{current_vol * 100}%` 입니다!")
        queue["playing"]["vol"] = vol / 100
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"{ctx.author.mention} 볼륨을 `{vol}%` 으로 바꿔드렸어요!")

    @commands.command(name="대기리스트", description="현재 대기 리스트를 보여줍니다.", aliases=["재생목록","대기열", "재생리스트", "pl", "ql", "queuelist", "playlist", "비", "ㅔㅣ"])
    async def queue_list(self, ctx):
        if str(ctx.guild.id) not in self.queues.keys():
            return await ctx.send("현재 노래를 재생을 하지 않고있어요!")
        queue_list = self.queues[str(ctx.guild.id)]
        temp_ql_embed = discord.Embed(title="재생 목록", color=tool.Color.yellow)
        temp_ql_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        playing_vid_url = queue_list["playing"]["vid_url"]
        playing_vid_title = queue_list["playing"]["vid_title"]
        playing_vid_author = queue_list["playing"]["vid_author"]
        playing_vid_channel_url = queue_list["playing"]["vid_channel_url"]
        playing_thumb = queue_list["playing"]["thumb"]
        vol = queue_list["playing"]["vol"]
        one_embed = discord.Embed(title="현재 재생중", colour=tool.Color.yellow)
        one_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        one_embed.set_thumbnail(url=playing_thumb)
        req_by = self.bot.get_user(int(queue_list["playing"]["req_by"]))
        one_embed.add_field(name="정보",
                            value=f"업로더: [`{playing_vid_author}`]({playing_vid_channel_url})\n제목: [`{playing_vid_title}`]({playing_vid_url})",
                            inline=False)
        one_embed.add_field(name="재생 요청자", value=f"{req_by.mention} (`{req_by}`)", inline=True)
        one_embed.add_field(name="현재 볼륨", value=f"{float(vol) * 100}%", inline=True)
        one_embed.add_field(name="대기중인 음악 개수", value=f"{len([x for x in queue_list.keys() if not x == 'playing'])}개")
        if ctx.voice_client.is_paused():
            one_embed.add_field(name="재생 상태", value="⏸ 현재 일시정지상태에요!", inline=True)
        elif queue_list["playing"]["random"]:
            one_embed.add_field(name="재생 상태", value="🔀 랜덤 재생기능이 켜져있어요!", inline=True)
        if len(queue_list.keys()) == 1:
            return await ctx.send(embed=one_embed)
        ql_num = 1
        embed_list = [one_embed]
        ql_embed = None
        for x in queue_list.keys():
            if x == "playing":
                ql_embed = temp_ql_embed.copy()
                continue
            if ql_num != 1 and (ql_num - 1) % 5 == 0:
                embed_list.append(ql_embed)
                ql_embed = temp_ql_embed.copy()
            queue_vid_url = queue_list[x]["vid_url"]
            queue_vid_title = queue_list[x]["vid_title"]
            queue_req_by = self.bot.get_user(int(queue_list[x]["req_by"]))
            ql_embed.add_field(name="재생 목록" + str(ql_num),
                               value=f"제목: [`{queue_vid_title}`]({queue_vid_url})\n재생 요청자: {queue_req_by.mention}\n(`{queue_req_by}`)",
                               inline=True)
            ql_num += 1
        next_song = queue_list[list(queue_list.keys())[1]]
        next_embed = discord.Embed(title="다음곡", color=tool.Color.yellow)
        next_vid_url = next_song["vid_url"]
        next_vid_title = next_song["vid_title"]
        next_vid_author = next_song["vid_author"]
        next_vid_channel_url = next_song["vid_channel_url"]
        next_thumb = next_song["thumb"]
        next_req_by = self.bot.get_user(int(next_song["req_by"]))
        next_embed.add_field(name="정보",
                             value=f"업로더: [`{next_vid_author}`]({next_vid_channel_url})\n제목: [`{next_vid_title}`]({next_vid_url})",
                             inline=False)
        next_embed.add_field(name="재생 요청자", value=f"{next_req_by.mention}\n(`{next_req_by}`)", inline=True)
        next_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        next_embed.set_thumbnail(url=next_thumb)
        embed_list.append(ql_embed)
        embed_list.append(next_embed)
        await page.start_page(self.bot, ctx, embed_list, embed=True)


def setup(bot):
    bot.add_cog(Music(bot))
