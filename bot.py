# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='z' , intents=discord.Intents.all())

@bot.command(name='1', help='Responds with truth')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'zelda is the best game'
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

bot.run(TOKEN)