import discord
from discord.ext import commands
import os
import traceback
import random

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
    activity = discord.Game(name="Netflix", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    
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
        text = message.author.mention+"ちゃん、おはゆ！" #message.author.mentionでメンション、nameで名前のみ
        await message.channel.send(text)
  
    # コマンドに対応するデータを取得して表示
    print(get_data(message))



# Botの起動とDiscordサーバーへの接続
client.run(token)
