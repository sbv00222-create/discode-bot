import discord
from discord.ext import commands
import re
import os
from threading import Thread
from flask import Flask

# Flask 웹서버 (UptimeRobot용)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def parse_channel_ids():
    channel_ids = set()

    single_channel_id = os.getenv('LINK_ONLY_CHANNEL_ID', '').strip()
    if single_channel_id:
        channel_ids.add(int(single_channel_id))

    multiple_channel_ids = os.getenv('LINK_ONLY_CHANNEL_IDS', '')
    for channel_id in multiple_channel_ids.split(','):
        channel_id = channel_id.strip()
        if channel_id:
            channel_ids.add(int(channel_id))

    return channel_ids

# 링크만 허용할 채널 ID 목록
LINK_ONLY_CHANNEL_IDS = parse_channel_ids()

# URL 패턴 정규식
URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 준비되었습니다!')
    print(f'링크 전용 채널 IDs: {sorted(LINK_ONLY_CHANNEL_IDS)}')

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author.bot:
        return

    # 지정된 채널인지 확인
    if message.channel.id in LINK_ONLY_CHANNEL_IDS:
        # 메시지에 URL이 있는지 확인
        if not URL_PATTERN.search(message.content):
            # URL이 없으면 메시지 삭제
            await message.delete()

    # 다른 명령어 처리
    await bot.process_commands(message)

# 봇 실행
if __name__ == '__main__':
    keep_alive()  # 웹서버 시작
    TOKEN = os.getenv('DISCORD_BOT_TOKEN') or os.getenv('TOKEN')
    bot.run(TOKEN)
