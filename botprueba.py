import discord
from google.cloud import compute_v1
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext import tasks
import randomGifs as rg
import pytz

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve variables from environment
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GCP_PROJECT = os.getenv('GCP_PROJECT')
GCP_ZONE = os.getenv('GCP_ZONE') 
GCP_INSTANCE_NAME = os.getenv('GCP_INSTANCE_NAME')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
colombia_tz = pytz.timezone("America/Bogota")

# Initialize the Discord Bot
bot = commands.Bot(command_prefix='!' , intents=discord.Intents.all())

# VM tracking variables
vm_start_time = datetime.now(colombia_tz)  # To track when the VM was last started

has_vm_been_8_hours = False

instance_client = compute_v1.InstancesClient()

# Start and stop instance functions
@bot.command(name='start')
async def start_instance(ctx):
    global vm_start_time
    global has_vm_been_8_hours
    await ctx.send("Encendiendo el servidor. Esto puede tardar unos minutos. Si en 10 minutos no responde, escribale al mk de Agui")
    try:
        # Send the request to start the instance
        if has_vm_been_8_hours and datetime.now(colombia_tz).weekday() < 5:
            await ctx.send("El servidor ha estado corriendo por más de 8 horas. No se puede encender.")
            return
        request = instance_client.start(project=GCP_PROJECT, zone=GCP_ZONE, instance=GCP_INSTANCE_NAME)
        request.result()
        await ctx.send("El servidor fue encendido correctamente.")
        vm_start_time = datetime.now(colombia_tz)
        
    except Exception as e:
        # Catch any errors in starting the instance
        await ctx.send(f"Error al encender el servidor. Intenta más tarde o escríbele a Agui. Error: {str(e)}")

@bot.command(name='stop')
async def stop_instance(ctx):
    await ctx.send("Apagando el servidor. Esto puede tardar unos minutos...")
    request = instance_client.stop(project=GCP_PROJECT, zone=GCP_ZONE, instance=GCP_INSTANCE_NAME)
    request.result()
    
# Function to check and stop VM if it has been running too long
@tasks.loop(hours=1.1)
async def check_vm_uptime():
    global vm_start_time
    await bot.wait_until_ready()
    channel = discord.utils.get(bot.get_all_channels(), name='general')  # Adjust to your channel
    # Initialize counter
    attempts = 0
    while not bot.is_closed() and attempts < 3:
        now = datetime.now(colombia_tz)
        elapsed_time = now - vm_start_time
        if elapsed_time > timedelta(hours=8.4) and now.weekday() < 5:  # Only check Monday to Friday
            await stop_instance(channel)
            vm_start_time = None  # Reset start time after stopping
            await channel.send("El servidor fue apagado debido a que se excedieron las 8 horas.")
            await channel.send(rg.randomGifUrl())
        # Increment counter
        attempts += 1

# Discord bot events
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    
    check_vm_uptime.start()

@bot.command(name='uptime')
async def uptime(ctx):
    global vm_start_time
    if vm_start_time:
        now = datetime.now(colombia_tz)
        elapsed_time = now - vm_start_time
        await ctx.send(f"El servidor ha estado corriendo por {elapsed_time}.")
        await ctx.send(rg.randomGifUrl())
    else:
        await ctx.send("El servidor se encuentra apagado en este momento.")
        await ctx.send(rg.randomGifUrl())

@bot.command(name='gif')
async def gif(ctx):
    await ctx.send(rg.randomGifUrl())


# Run the bot
bot.run(DISCORD_TOKEN)
