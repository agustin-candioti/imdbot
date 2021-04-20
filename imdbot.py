# bot.py
import os
import random
import discord
import requests
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands
from pprintpp import pprint as pp
from prettytable import PrettyTable


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD2 = os.getenv('DISCORD_GUILD2')
KEY = os.getenv('OMDBKEY')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

db = mysql.connector.connect(host="localhost", user="root", passwd="1404", database="movies")
cursor = db.cursor()
cursor.execute("SELECT * FROM discordmovies")
data = cursor.fetchall()

@bot.command(name='agregar')
async def agregar(ctx, imdblink):
    url='http://www.omdbapi.com/?apiKey='+KEY
    params = {
        'i': imdblink
    }
    response = requests.get(url,params=params).json()
    pp(response)
    if response['Response'] == "True":
        title = response['Title']
        year = response['Year']
        imdbRating = response['imdbRating']
        director = response['Director']
        plot = response['Plot']
        cursor.execute("INSERT INTO discordmovies (Title,Year,IMDBRating,Director,Plot) VALUES (title,year,imdbRating,director,plot)")
        db.commit()
        response = title+' fue agregada a la lista mi rey'
        print(title + " " + year + " " + plot)
    else:
        response = "qué mierda me mandaste ridículo?"
        print(response['Response'])

    await ctx.send(response)

@bot.command(name='lista')
async def lista(ctx):
    cursor.execute("SELECT * FROM discordmovies")
    data = cursor.fetchall()
    myTable = PrettyTable(["Title", "Year", "imdbRating", "Director", "Plot"])
    for row in data:
        title = row[0]
        year = row[1]
        imdbRating = row[2]
        director = row[3]
        plot = row[4]
        myTable.add_row([title, year, imdbRating, director, plot])
    await ctx.send(myTable)

bot.run(TOKEN)