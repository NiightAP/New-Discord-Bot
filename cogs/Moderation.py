import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands

    # Kick
    @commands.slash_command(name='kick', description='Kicks a user')
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.message.delete()
        await ctx.channel.send("Member has been kicked")

    # Ban
    @commands.slash_command(name='ban', description='Bans a user')
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await ctx.channel.trigger_typing()
        await member.ban(reason = reason)
        await ctx.respone.send_message(f':boom: Member has been banned.')
        await ctx.message.delete()

    # Pardon
    @commands.slash_command(name='pardon', description='Unbans a user')
    @commands.has_permissions(administrator = True)
    async def pardon(self, ctx, *, member):
        await ctx.channel.trigger_typing()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.channel.trigger_typing()
                await ctx.guild.unban(user)
                await ctx.response.send_message(f'Unbanned {user.mention}')
                return

    # Clear
    @commands.slash_command(name='clear', description='Clears messages from text channel')
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        await ctx.response.send_message(amount + "messages have been cleared.")

    # Changenick
    @commands.slash_command(name='changenick', description='Changes a users nickname', pass_context=True)
    @commands.has_permissions(administrator = True)
    async def changenick(self, ctx, member: discord.Member, nick):
        await ctx.channel.trigger_typing()
        await member.edit(nick=nick)
        await ctx.response.send_message(f'Nickname was changed for {member.mention} ')

    # Lockdown
    @commands.slash_command(name='lockdown', description='Locks a text channel')
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
        await ctx.response.send_message(ctx.channel.mention + "is now locked.")
        await ctx.send( ctx.channel.mention + " ***Channel is now in lockdown.***")

    # Unlock
    @commands.slash_command(name='unlock', description='Unlocks a text channel')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, read_messages=True)
        await ctx.response.send_message(ctx.channel.mention + "is now unlocked.")
        await ctx.send( ctx.channel.mention + " ***Channel has been unlocked.***")

    # Shutdown
    @commands.slash_command(name='shutdown', description='shuts down the bot (Owner only)', pass_context = True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.send("Bot is shutting down.")
        await ctx.close()

def setup(client):
    client.add_cog(Moderation(client))
