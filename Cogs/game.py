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
class Game(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name="타자", aliases=["typewriter", "타자게임"], pass_context=True)
    async def typewriter(self, ctx, mode:str=None, language:str=None):
        if mode is None or language is None: return await ctx.message.reply(embed=discord.Embed(color=tool.Color.green,description=f"사용방법 : {config.BotSettings.prefix}타자 [모드] [언어]\n\n모드 : 멀티, 솔로\n언어 : 한국어, 영어\n\n```모드 설명\n멀티 : 명령어를 사용한 채널에 메시지를 입력할수 있는 모든 대상이 타자게임을 할수있습니다.\n솔로 : 자기 자신만 타자게임만 합니다.```\n```언어 설명\n한국어 : 한국어 타자게임를 합니다.\n영어 : 영어로 타자게임를 합니다.```"))
        if mode == "솔로":
            if language == "한국어" or language == "Korean" or language == "korean":
                embed = discord.Embed(title="⌨ 타자게임", description=f"타자게임을 시작합니다! 5초후 나오는 사진의 글을 입력해주세요!",color=tool.Color.green)
                msg = await ctx.channel.send(embed=embed)
                src = 5
                for i in range(5):
                    await asyncio.sleep(1)
                    src -= 1
                    embed = discord.Embed(title="⌨ 타자게임", description=f"타자게임을 시작합니다! {src}초후 나오는 사진의 글을 입력해주세요!", color=tool.Color.green)
                    await msg.edit(embed=embed)
                    if src <= 0: break
                korean_list = ["참새도 땅이 없으면 못 산다.", "나의 집이 비록 작더라도 진정한 친구로 채울 수만 있다면 만족하겠노라.", "범도 제 새끼 사랑할 줄 안다.",
                               "오랜 친구보다 나은 거울은 없다.", "사람은 자기 일보다 남의 일을 더 잘 알고 더 잘 판단한다.", "바늘 가는 데 실 간다", "태끌 모아 태산",
                               "가까운 데를 가도 점심밥을 싸 가지고 가거라", "계란으로 바위치기", "고래 싸움에 새우 등 터진다.", "고인 물은 썩는다", "고양이 목에 방울 달기",
                               "나는 새도 떨어뜨린다", "나는 새에게 여기 앉아라 저기 앉아라 할 수 없다.", "나무를 잘 오르는 놈은 떨어져 죽고 헤엄을 잘 치는 놈은 빠져 죽는다.",
                               "나무에서 물고기를 구한다.", "다 된 죽에 코 풀기", "사공이 많으면 배가 산으로 간다","식은 죽 먹기", "천리길도 한 걸음부터", "짧은 밤에 긴 노래 부르랴",
                               "처음이 나쁘면 끝도 나쁘다", "천 리 길도 십 리", "소 잃고 외양간 고친다", "사람이 많으면 하늘도 이긴다", "사촌이 땅을 사면 배가 아프다",
                               "마당 터진 데 솔뿌리 걱정한다", "말 한마디에 천냥 빚을 갚는다", "매도 먼저 맞는 놈이 낫다", "똥 밭에 굴러도 이승이 낫다", "똥이 무서워서 피하나 더러워서 피하지",
                               "뛰는 놈 위에 나는 놈 있다", "뛰어 봤자 벼룩이다", "다람쥐 쳇바퀴 돌리듯", "느린 소도 성낼 적이 있다", "구르는 돌에는 이끼가 끼지 않는다", "개팔자가 상팔자"]
                contentss = random.choice(korean_list)
                files = contentss.replace(".", "")
                file = discord.File(f'./typewriter/korean/{files}.png', filename=f'{files}.png')
                await ctx.channel.send(file=file)
                begin = time.time()
                while True:
                    try:
                        answer = (await self.app.wait_for('message', timeout=60, check=(lambda m: m.channel == ctx.channel and m.author == ctx.author))).content
                        if str(answer.replace(".", "")) == str(contentss.replace(".", "")):
                            timess = time.time() - begin
                            tapbe = len(contentss) / timess * 60
                            if tapbe > 100 and not tapbe > 200: tapbe += 100
                            elif tapbe > 200: tapbe += 50
                            et = format(timess, ".2f")
                            embed = discord.Embed(title="⌨ 타자 게임 결과", description=f"출제 문장 : `{contentss}`\n\n{round(tapbe)}타, {et}초",color=tool.Color.green)
                            await ctx.channel.send(embed=embed)
                            break
                        else:
                            continue
                    except TimeoutError:
                        await ctx.channel.send(embed=discord.Embed(description="이런! 60초나 타자를 치시지 않으셨네요.. 타자 게임을 종료합니다!", color=tool.Color.green))
                        break
            else: return await ctx.channel.send(embed=discord.Embed(description=f"`{language}`언어는 없습니다! 현재는 `한국어` 만 있습니다."))

























def setup(app):
    app.add_cog(Game(app))
    print("Cogs.Game Load")