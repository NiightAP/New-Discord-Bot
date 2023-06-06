import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import MissingPermissions

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class on_load(commands.Cog):
    def __init__(self, client):
        self.client = client
     
     
    @client.event   
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions, commands.MissingRequiredArgument):
            await ctx.send("Missing permission(s) or Argument(s)")
    
    
def setup(client):
    client.add_cog(on_load(client))