import discord
import os
import time
from numpy import genfromtxt
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

class Admin(commands.Cog):

    def __init__(self, client):
        self.blacklist = genfromtxt('./config/blacklist.csv', delimiter=',')
        self.client = client

    @commands.command()
    @commands.has_role(pass_context=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if reason == None:
            await ctx.send("you must enter a reason to kick.")
        else:
            try:
                if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.ban_members:
                    embed = discord.Embed(
                        colour=discord.Color.red()
                    )
                    embed.add_field(name="KICKED",
                                    value=f'You have been kicked from `` {ctx.guild.name} `` by  `` {ctx.message.author} `` for  `` {reason} ``',
                                    inline=False)
                    await member.send(embed=embed)
                    reason = reason
                    await ctx.guild.kick(member)
                    embed = discord.Embed(title="User kicked was kicked for {}".format(reason),
                                          description="**{}** has been kicked!".format(member),
                                          color=discord.Color.green())
                    embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

                    await ctx.send(embed=embed)
                    author = ctx.message.author
                    channel =client.get_channel(admin_actions_log_channel_id)
                    await channel.send(f"{author} just kicked {member} for {reason}")
                else:
                    embed = discord.Embed(title="Permission Denied.",
                                          description="You don't have permission to use this command.",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="Permission Denied.",
                                      description="Bot doesn't have correct permissions, or bot can't kick this user.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)


    @commands.command()
    @commands.has_role('Bot Commander')
    async def remove(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        await ctx.send(f"Removed `{role}` role from `{user.name}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def add(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        await ctx.send(f"Gave `{role}` role to `{user.name}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def mute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await user.remove_roles()
        await user.add_roles(role)
        await ctx.send(f"Muted `{user.name}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await user.remove_roles(role)
        await ctx.send(f"Unmuted `{user.name}`")
        
    @commands.command()
    @commands.has_role('Bot Commander')
    async def purge(self, ctx, amount=1000):
        await ctx.channel.purge(limit=amount)
        time.sleep(1)
        await ctx.send("`Purge complete`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def say(self, ctx, *, message):
        await ctx.send(f'{message}')

    @commands.command()
    @commands.has_role('Bot Commander')
    async def watching(self, ctx, *, message):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{message}"))
        await ctx.send(f"Now watching `{message}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def playing(self, ctx, *, message):
        await self.client.change_presence(activity=discord.Game(name=f"{message}"))
        await ctx.send(f"Now playing `{message}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def streaming(self, ctx, *, message):
        await self.client.change_presence(activity=discord.Streaming(name=f"{message}", url="https://www.twitch.tv/fourohfour"))
        await ctx.send(f"Now streaming `{message}`")

    @commands.command()
    @commands.has_role('Bot Commander')
    async def listening(self, ctx, *, message):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{message}"))
        await ctx.send(f"Now listening to `{message}`")

    @client.command()
    @commands.has_role('Bot Commander')
    async def stop(self, ctx):
        await ctx.send("`Stopping.`")
        await self.client.close()

def setup(client):
    client.add_cog(Admin(client))
