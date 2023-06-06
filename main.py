import discord
import os
import dotenv
import logging
import asyncio
import time
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
from itertools import cycle
from setuptools import Command



client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

status = cycle(['https://github.com/niightap'])

#bot status
@tasks.loop(seconds=30)
async def change_status(): 
    await client.change_presence(activity=discord.Game(next(status)))
@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} has connected to Discord!')
    print(f'Commands loading...')
    time.sleep(3)
    try:
        print('Bot fully loaded.')
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
    embed = discord.Embed(title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
    await ctx.response.send_message(embed=embed)

@load.error
async def load_error(ctx, interaction: discord.Interaction, error):
        await interaction.response.send_message(":exclamation: You are not owner.", ephemeral=True)

@client.slash_command(pass_context = True, name='unload_extension', description='Unloads cog')
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    embed = discord.Embed(title='Unload', description=f'{extension} successfully unloaded', color=0xff00c8)
    await ctx.response.send_message(embed=embed)

@unload.error
async def unload_error(ctx, interaction: discord.Interaction, error):
        await interaction.response.send_message(":exclamation: You are not owner.", ephemeral=True)
    
@client.slash_command(pass_context = True, name='reload_extension', description='Reloads cog')
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.response.send_message(embed=embed)

@reload.error
async def reload_error(ctx, interaction: discord.Interaction, error):
        await interaction.response.send_message(":exclamation: You are not owner.", ephemeral=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#asyncio.run(load())
client.run(TOKEN)