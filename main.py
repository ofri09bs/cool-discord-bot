import asyncio
import discord
import random
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
        

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}! This is a command response.')

@bot.command()
async def mega(ctx):
    await ctx.send(f'{ctx.author.mention} MEGA KNIGHT COMMAND ACTIVATED! RAHHHHHHHHHH!')


async def get_user_response(ctx, question, timeout=30):
    await ctx.send(question)

    try:
        msg = await bot.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            timeout=timeout
        )
        return msg.content

    except asyncio.TimeoutError:
        await ctx.send("timeout! No response received.")
        return None  
    
    
async def check_bal(ctx,bal):
    if bal <= 0:
        await ctx.send(f'{ctx.author.mention} You have run out of money! Game over.')
        return False
    return True
    
@bot.command()
async def gamble(ctx):
    bal = 100
    game = True
    await ctx.send(f'{ctx.author.mention} Hello! welcome to Mega Gamble!\n your current balance is {bal}$\n reply stop any time to stop.')
    while(game):
        bet = await get_user_response(ctx,f'{ctx.author.mention} How much do you want to gamble:')

        if bet is None or bet.lower() == 'stop':
            game = False
            await ctx.send(f'{ctx.author.mention} Thanks for playing! Your final balance is {bal}$.')
            break

        if not bet.isdigit() or int(bet) <= 0:
            await ctx.send(f'{ctx.author.mention} Invalid bet amount. Please enter a positive number.')
            continue

        bet = int(bet)
        if bet > bal:
            await ctx.send(f'{ctx.author.mention} You cannot bet more than your current balance of {bal}$.')
            continue

        roll = random.randint(1, 10)
        match roll:
            case 1: # lose
                bal -= bet
                await ctx.send(f'{ctx.author.mention} You lost {bet}$. Your new balance is {bal}$.')
                game = await check_bal(ctx,bal)
            case 2: # win double
                bal += bet * 2 
                await ctx.send(f'{ctx.author.mention} You won {bet * 2}$! Your new balance is {bal}$.')
            case 3: # win half
                bal += bet // 2
                await ctx.send(f'{ctx.author.mention} You won {bet // 2}$! Your new balance is {bal}$.')
            case 4: # lose half
                bal -= bet // 2 
                await ctx.send(f'{ctx.author.mention} You lost {bet // 2}$. Your new balance is {bal}$.')
                game = await check_bal(ctx,bal)
            case 5: # win triple
                bal += bet * 3
                await ctx.send(f'{ctx.author.mention} You won {bet * 3}$! Your new balance is {bal}$.')
            case 6: # lose triple
                bal -= bet * 3
                await ctx.send(f'{ctx.author.mention} You lost {bet * 3}$. Your new balance is {bal}$.')
                game = await check_bal(ctx,bal)
            case 7: # win nothing
                await ctx.send(f'{ctx.author.mention} You won nothing! Your balance remains {bal}$.')
            case 8: #jackpot
                bal += bet * 10
                await ctx.send(f'{ctx.author.mention} JACKPOT! You won {bet * 10}$! Your new balance is {bal}$.')
            case 9: #double or nothing
                response = await get_user_response(ctx,f'{ctx.author.mention} Double or nothing! Do you want to proceed? (yes/no)')
                if response and response.lower() == 'yes':
                    if random.choice([True, False]):
                        bal += bet * 2
                        await ctx.send(f'{ctx.author.mention} You won {bet * 2}$! Your new balance is {bal}$.')
                    else:
                        bal -= bet
                        await ctx.send(f'{ctx.author.mention} You lost {bet}$. Your new balance is {bal}$.')
                        game = await check_bal(ctx,bal)
            case 10: #win 670$
                bal += 670
                await ctx.send(f'{ctx.author.mention} You won 670$! Your new balance is {bal}$.')
            case _:
                await ctx.send(f'{ctx.author.mention} An error occurred with the roll. Please try again.')
            
@bot.command()
async def calc(ctx):
    await ctx.send(f'{ctx.author.mention} Welcome to Mega Calculator! Type "exit" to leave.')
    while True:
        expr = await get_user_response(ctx, f'{ctx.author.mention} Enter a mathematical expression to evaluate:')
        if expr is None or expr.lower() == 'exit':
            await ctx.send(f'{ctx.author.mention} Exiting Mega Calculator. Goodbye!')
            break
        try:
            result = eval(expr, {"__builtins__": None}, {})
            await ctx.send(f'{ctx.author.mention} The result of {expr} is {result}.')
        except Exception as e:
            await ctx.send(f'{ctx.author.mention} Error evaluating expression: {e}')

@bot.command()
async def remindme(ctx):
    await ctx.send(f'{ctx.author.mention} Welcome to Mega Reminder!')
    await ctx.send(f'{ctx.author.mention} what do you want me to remind you about?')

    reminder_text = await get_user_response(ctx, f'{ctx.author.mention} Please enter the reminder text:')
    if reminder_text is None:
        return
    
    question_time = f'{ctx.author.mention} In how many minutes should I remind you?'
    time_str = await get_user_response(ctx, question_time)
    if time_str is None:
        return

    if not time_str.isdigit() or int(time_str) <= 0:
        await ctx.send(f'{ctx.author.mention} Please enter a valid positive number for minutes.')
        return

    minutes = int(time_str)
    await ctx.send(f'{ctx.author.mention} Reminder set for {minutes} minutes from now.')

    await asyncio.sleep(minutes * 60)

    await ctx.send(f'{ctx.author.mention} Reminder: {reminder_text}')
            
bot.run(token, log_handler=handler, log_level=logging.DEBUG)





