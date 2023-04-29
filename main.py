import discord
import os
import dotenv
import logging
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
from setuptools import Command



client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

status = cycle(['https://github.com/niightap', '?help for help'])

#bot status
@tasks.loop(seconds=30)
async def change_status(): 
    await client.change_presence(activity=discord.Game(next(status)))
@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} has connected to Discord!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Event
@client.event
async def on_message(message):
    if message.author.bot:
        return
    await client.process_commands(message)
        
        
#cogs
@client.slash_command(pass_context = True, name='load_extension', description='Loads cog')
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.slash_command(pass_context = True, name='unload_extension', description='Unloads cog')
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#asyncio.run(load())
client.run(TOKEN)