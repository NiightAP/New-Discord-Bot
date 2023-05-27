import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        
         # Ping
    @commands.slash_command(name='ping', description='Responds with bot latency.')
    async def ping(self, ctx):
        await ctx.response.send_message(f'Pong! {round(self.client.latency * 1000)}ms')

    # Dev
    @commands.slash_command(name='developer_info', description='Lists dev info')
    async def dev(self, ctx):
        await ctx.response.send_message("**@NiightGamez#1009**" + " Developed by NiightAP: https://github.com/niightap")

    # Source
    @commands.slash_command(name='source', description='Link to bot source code.')
    async def source(self, ctx):
        await ctx.response.send_message(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/NiightAP/New-Discord-Bot")

    # Invite
    @commands.command(name='bot_invite', description='Bot invite link.')
    async def invite(self, ctx):
        invitelink = "Invite NiightAP to your server with this link: \nhttps://niightap.fanlink.to/botinv"
        await ctx.response.send_message(invitelink)
        
        
def setup(client):
    client.add_cog(Info(client))