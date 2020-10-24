import discord
import random
import subprocess
import sys
import json
import async_cse
import csv
import time
from numpy import genfromtxt
from discord.ext import commands
from discord.utils import get
import os

client = commands.Bot(command_prefix = '!')

class Commands(commands.Cog):

    def __init__(self, client): 
        self.blacklist = genfromtxt('./config/blacklist.csv', delimiter=',')                        
        self.client = client

# ------------------------------------------------------------- Error Handlers ------------------------------------------------------

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance (error, commands.MissingRole):
            await ctx.send("You have insufficient permissions.")
            
    def bot_check(self, ctx: commands.Context):
         return ctx.author.id not in self.blacklist

# -------------------------------------------------------------  Error Handlers ------------------------------------------------------------- 

    @commands.command()
    async def lists(self, ctx):
        await ctx.send(self.blacklist)

    @commands.command(aliases=['halp', 'h'])
    async def help(self, ctx):
        embed = discord.Embed(
        colour = discord.Colour(0xD80083)
        )
        num = random.randint(1,100)
        embed.add_field(name="!av", value="Shows your avatar or someone elses, !av [user]",inline=False)
        embed.add_field(name="!info", value="Shows server info, !info",inline=False)
        embed.add_field(name="!commandercmds", value="Shows admin commands, !commandercmds",inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['haha', 'poggers'])
    async def commandercmds(self, ctx):
        embed = discord.Embed(
        colour = discord.Colour.red()
        )
        num = random.randint(1,100)
        embed.add_field(name="!purge", value="Purges a given amount of messages, !purge (1-1000)", inline=False)
        embed.add_field(name="!restart", value="Restarts the bot, !restart", inline=False)
        embed.add_field(name="!say", value="Sends a message as the bot, !say (message)", inline=False)
        embed.add_field(name="!add/remove", value="Add or removes roles, !add/remove (role) (member)", inline=False)
        embed.add_field(name="!mute/unmute", value="Mute or unmute, !mute/unmute (member)", inline=False)
        embed.add_field(name="!streaming/listening/watching/playing", value="Change presence, !streaming (message)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def av(self, ctx, user: discord.Member):
        embed = discord.Embed(
        color = discord.Color(0xffff),
        title=f"{user.name}"
        )
        embed.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            color = discord.Color(0xffff),
            title=f"{ctx.guild.name}"
        )
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name='Region', value=f"`{ctx.guild.region}`")
        embed.add_field(name='Member Count', value=f"`{ctx.guild.member_count}`")
        embed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Guild ID: {ctx.guild.id}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Commands(client))
