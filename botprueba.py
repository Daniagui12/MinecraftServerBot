# bot.py
import datetime
import os
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from randomGifs import randomGifUrl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
USER_ID = int(os.getenv('DISCORD_USER_ID'))
USER_ID2 = int(os.getenv('DISCORD_USER_ID2'))

bot = commands.Bot(command_prefix='z' , intents=discord.Intents.all())

def calculate_days_left():
    #calculate days left
    days_left = 0
    dateOfTotk = datetime.datetime(2023, 5, 12)
    today = datetime.datetime.now()
    days_left = dateOfTotk - today
    days_left = days_left.days
    print("Days left to Tears of the Kingdom: " + str(days_left))
    return days_left

@tasks.loop(hours=24.0) # runs every 24 hours
async def send_message():
    # send message to channel
    channel = bot.get_channel(CHANNEL)
    users = [bot.get_user(USER_ID), bot.get_user(USER_ID2)]

    for user in users:
        await user.send("Days left to Tears of the Kingdom: " + str(calculate_days_left()))
        await user.send(randomGifUrl())

    await channel.send("Days left to Tears of the Kingdom: " + str(calculate_days_left()))
    await channel.send(randomGifUrl())


@bot.command(name='days', help='Responds with days left to Tears of the Kingdom')
async def days_left(ctx):
    await ctx.send("Days left to Tears of the Kingdom: " + str(calculate_days_left()))
    await ctx.send(randomGifUrl())

@bot.command(name='gif', help='Responds with a random gif')
async def gif(ctx):
    await ctx.send("Here is a random Zelda gif")
    await ctx.send(randomGifUrl())


@bot.event
async def on_ready():
    botname = bot.user.name
    print(f'{botname} has connected to Discord!')
    send_message.start()

bot.run(TOKEN)