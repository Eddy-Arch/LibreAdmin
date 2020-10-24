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
    @commands.has_role('Bot Commander')
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"`{member}` has been kicked.")

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
