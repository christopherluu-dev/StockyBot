import os
import requests
import discord
import urllib.request
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from retrieve import get_daily_info
from voice import get_TextToSpeech

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FINNHUB = os.getenv('FINNHUB_API')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command(pass_context=True)
async def tick(ctx, arg):
    symbol = arg.upper()
    url = 'https://finnhub.io/api/v1/quote?symbol=%s&token=%s' % (symbol, FINNHUB)
    url_info = 'https://finnhub.io/api/v1/stock/profile2?symbol=%s&token=%s' % (symbol, FINNHUB)

    r = requests.get(url)
    r_info = requests.get(url_info)
    
    print(r.json())
    print(r_info.json())
    
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

    image_url = './resources/chart.png'
    chart_file = discord.File(image_url, filename='chart.png')
    embed = discord.Embed(title = company_name, description= '', url= company_url)
    embed.set_image(url = "attachment://chart.png")
    
    if response_info['logo'] != '':
        embed.set_thumbnail(url = response_info['logo'])

    await ctx.send(file = chart_file, embed = embed)
    print(f'Message for tick: {company_name} has been sent')

bot.run(TOKEN)
