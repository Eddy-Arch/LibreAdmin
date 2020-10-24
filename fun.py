import discord 
import os
import random
from numpy import genfromtxt
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

class Fun(commands.Cog):

    def __init__(self, client):  
        self.blacklist = genfromtxt('./config/blacklist.csv', delimiter=',')                      
        self.client = client

    @commands.command()
    async def joke(self, ctx):
        jokes = ['placeholder',
                 'placeholder',
                 'placeholder',
                 'placeholder',
                 'placeholder',
                 'placeholder',
                 'placeholder']
        embed = discord.Embed(
            title = 'Joke',
            description = '\nhere is the joke',
            color = discord.Colour.blue()
        )
        embed.add_field(name='Response', value=f'{random.choice(jokes)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', '8b'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Dont count on it.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        embed = discord.Embed(
            title = '8 Ball',
            color = discord.Colour.green()
        )
        embed.add_field(name='Question', value=f'{question}', inline=False)
        embed.add_field(name='Response', value=f'{random.choice(responses)}', inline=False)
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to give me a question')

def setup(client):
    client.add_cog(Fun(client))
