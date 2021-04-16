import discord
from discord.ext import commands
import os
import traceback
import random
import re #正規表現
import math #Zeller

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)
#bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

"""Bot起動時に実行されるイベントハンドラ"""
@client.event # イベントを受信するための構文（デコレータ）
async def on_ready():
    #botのステータス変更
    activity = discord.Activity(name='Netflix', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

    print('------Logged in as------')
    print(client.user.name)
    print(client.user.id)
    print('------------------------')



# コマンドに対応するリストデータを取得する関数を定義
def get_data(message):
    command = message.content
    data_table = {
        '/members': message.guild.members, # メンバーのリスト
        '/roles': message.guild.roles, # 役職のリスト
        '/text_channels': message.guild.text_channels, # テキストチャンネルのリスト
        '/voice_channels': message.guild.voice_channels, # ボイスチャンネルのリスト
        '/category_channels': message.guild.categories, # カテゴリチャンネルのリスト
    }
    return data_table.get(command, '対応するリストデータを取得するには、無効なコマンドです')

# ツェラーの公式 [Zeller]
def zeller(year, month, day):
    q = day
    m = month
    Y = year
    if m <= 2:
        m+= 12
    if month <= 2:
        Y -= 1
    h = (q + math.floor((13 * (m + 1)) / 5) + Y + math.floor(Y / 4) - math.floor(Y / 100) + math.floor(Y / 400)) % 7
    return h

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
    #if message.author == client.user:
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    # if message.content == '/neko':
    # if client.user in message.mentions: # 話しかけられたかの判定

    if 'おは' in message.content:
        text = message.author.mention+'ちゃん、おはゆ！:hatching_chick:' #message.author.mentionでメンション、nameで名前のみ
        await message.channel.send(text)

    # ツェラーの公式 [Zeller]
	# 年 + 年/4 - 年/100 + 年/400 + (13*月+8)/5 + 日 を7で割ったときの余り = [0-6]
	# ただし、1月、2月は前年の13月、14月として計算
	# 1582/10/15(金)以降に対応。閏年対応。
    if re.search('^[0-9]{4}\/[0-9]{2}\/[0-9]{2}$', message.content):# [yyyy/mm/dd]にマッチ
        ztext = message.content
        l = ztext.split('/')
        z_year  = int(l[0])
        z_month = int(l[1])
        z_date  = int(l[2])
        ws = ["日", "月", "日", "水", "木", "金", "土"]
        x = zeller(z_year, z_month, z_date)
        await message.channel.send(message.content + " は " + ws[x] + "曜日:turtle:")




    # コマンドに対応するデータを取得して表示
    print(get_data(message))



# Botの起動とDiscordサーバーへの接続
client.run(token)
