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
    url_info = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB}'
    
    url = f'https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}'

    headers = {
                'x-rapidapi-host': 'yahoo-finance15.p.rapidapi.com',
                'x-rapidapi-key': 'abb323c569mshcb7668a99253ae7p188886jsncd1eae2507a2'
              }

    response = requests.request("GET", url, headers=headers)

    r_info = requests.get(url_info)
    
    print(response.json())
    print(r_info.json())
    
    response = response.json()
    response_info = r_info.json()

    company_name = response[0]['shortName']
    
    if len(response_info) != 0:
        company_url = response_info['weburl']
    else:
        company_url = ''
    current = response[0]['regularMarketPrice']
    opening = response[0]['regularMarketOpen']
    closing = response[0]['regularMarketPreviousClose']
    high = response[0]['regularMarketDayHigh']
    low = response[0]['regularMarketDayLow']
    
    
    if current >= closing:
        diff = current - closing
        up_down = True
    elif current < closing:
        diff = closing - current
        up_down = False

    get_daily_info(symbol, company_name, up_down, closing)
    print(company_name, current, opening, closing, high, low)

    image_url = './resources/chart.png'
    chart_file = discord.File(image_url, filename = 'chart.png')

    if up_down == True:
        if company_url != '':
            embed = discord.Embed(title = company_name, url = company_url, description = '', colour = discord.Colour.green())
        else:
            embed = discord.Embed(title = company_name, description = '', colour = discord.Colour.green())

    elif up_down == False:
        if company_url != '':
            embed = discord.Embed(title = company_name, url = company_url, description = '', colour= discord.Colour.red())
        else:
            embed = discord.Embed(title = company_name, description = '', colour= discord.Colour.red())

        
    embed.set_image(url = 'attachment://chart.png')

    if up_down == True:
        embed.add_field(name = 'Current', value = f'{current} +{diff:.2f}▲', inline=True)
    elif up_down == False:
        embed.add_field(name = 'Current', value = f'{current} -{diff:.2f}▼', inline=True)
 
    embed.add_field(name = 'Opening', value = opening, inline = True)
    embed.add_field(name = 'Prev Closing', value = closing, inline = True)
    
    if len(response_info) != 0:
       embed.set_thumbnail(url = response_info['logo'])

    await ctx.send(file = chart_file, embed = embed)
    print(f'Message for tick: {company_name} has been sent')

bot.run(TOKEN)
