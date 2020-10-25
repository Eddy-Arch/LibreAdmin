import discord
import random
import os
import random
import time
import io
import requests
from discord.ext import commands
from config.config import bot_token, bot_prefix
print(bot_token)

client = commands.Bot(command_prefix=bot_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    channel = discord.utils.get(client.get_all_channels(), name='general')
    print('\n Bot is online! :)')
    print('-'*21)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension} cog has been loaded.`")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension} cog has been unloaded.`")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(bot_token)

