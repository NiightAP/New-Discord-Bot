import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class Discord_Info(commands.Cog, name='Discord_Info'):
    def __init__(self, client):
        self.client = client

    # Avatar
    @commands.slash_command(name='avatar', description='Displays a users discord avatar.')
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(f"Avatar to **{user.name}** \n{user.avatar_url_as(size=1024)}")

def setup(client):
    client.add_cog(Discord_Info(client))