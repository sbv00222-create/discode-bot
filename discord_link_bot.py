import discord
from discord.ext import commands
import re
import os

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 링크만 허용할 채널 ID
LINK_ONLY_CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))

# URL 패턴 정규식
URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 준비되었습니다!')
    print(f'링크 전용 채널 ID: {LINK_ONLY_CHANNEL_ID}')

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author.bot:
        return

    # 지정된 채널인지 확인
    if message.channel.id == LINK_ONLY_CHANNEL_ID:
        # 메시지에 URL이 있는지 확인
        if not URL_PATTERN.search(message.content):
            # URL이 없으면 메시지 삭제
            await message.delete()

    # 다른 명령어 처리
    await bot.process_commands(message)

# 봇 실행
if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)
