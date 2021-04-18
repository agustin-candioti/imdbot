# bot.py
import os
import random
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from pprintpp import pprint as pp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD2 = os.getenv('DISCORD_GUILD2')
KEY = os.getenv('OMDBKEY')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.command(name='agregar')
async def agregar(ctx, year, *, multi_word):

    url='http://www.omdbapi.com/?apiKey='+KEY
    params = {
        's':multi_word,
        'type':'movie',
        'y': year
    }
    response = requests.get(url,params=params).json()
    pp(response)
    if len(response['Search']) > 1:
        response = 'A ver si sos un poquito más específico la concha de tu madre'
    else:
        response = multi_word+' fue agregada a la lista mi rey'

    await ctx.send(response)



bot.run(TOKEN)