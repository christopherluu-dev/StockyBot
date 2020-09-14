import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FINNHUB = os.getenv('FINNHUB_API')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command(name='tick')
async def check_tick(ctx, arg):
    url = 'https://finnhub.io/api/v1/quote?symbol=%s&token=%s' % (arg, FINNHUB)
    url_info = 'https://finnhub.io/api/v1/stock/profile2?symbol=%s&token=%s' % (arg, FINNHUB)

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
    
    print(company_name, company_url, current, opening, closing, high, low)

bot.run(TOKEN)
