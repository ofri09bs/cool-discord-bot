import discord
from pathlib import Path
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='MK', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')


@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server... MEGA KNIGHTTT, {member.name}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'clash royale' in message.content.lower():
        await message.channel.send('Clash Royale is awesome!')

    if 'hello' in message.content.lower():
        await message.channel.send(f'Hello, {message.author.name}!')

    if 'pipi' in message.content.lower():
        await message.channel.send('poopoo!')

    if 'mega knight' in message.content.lower():
        await message.channel.send('MEGA KNIGHTTTTT!')

    if 'shit' in message.content.lower():
        await message.channel.send(f'{message.author.mention} NO curses here! its not mega knight of you')

    if 'beeri' in message.content.lower():
        await message.channle.send('beeri epstin?')
        

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}! This is a command response.')

@bot.command()
async def mega(ctx):
    await ctx.send(f'{ctx.author.mention} MEGA KNIGHT COMMAND ACTIVATED! RAHHHHHHHHHH!')





bot.run(token, log_handler=handler, log_level=logging.DEBUG)




