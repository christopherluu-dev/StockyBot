import os
import requests
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import discord
from dotenv import load_dotenv
from discord.ext import commands
from retrieve import get_daily_info

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FINNHUB = os.getenv('FINNHUB_API')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command(name='tick')
async def check_tick(ctx, arg):
    symbol = arg.upper()
    url = 'https://finnhub.io/api/v1/quote?symbol=%s&token=%s' % (symbol, FINNHUB)
    url_info = 'https://finnhub.io/api/v1/stock/profile2?symbol=%s&token=%s' % (symbol, FINNHUB)

    r = requests.get(url)
    r_info = requests.get(url_info)
    
    print(r.json())
    print(r_info.json())
    
    start = '2020-09-14'
    end = '2020-09-14'

    response = r.json()
    response_info = r_info.json()

    company_name = response_info['name']
    company_url = response_info['weburl']
    current = response['c']
    opening = response['o']
    closing = response['pc']
    high = response['h']
    low = response['l']
   
    get_daily_info(symbol)
    print(company_name, company_url, current, opening, closing, high, low)
    await ctx.send(file = discord.File('chart.png'))

bot.run(TOKEN)
