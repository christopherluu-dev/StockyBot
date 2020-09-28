import os
import datetime as dt
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
from dateutil import tz

def get_daily_info(symbol, company_name, up_down, closing, period = '1d', data_intervals='1m'):
    #Retrieves the minute to minute data from Yahoo Finance
    data = yf.download(symbol, period = period, interval = data_intervals)['Adj Close']
    matplotlib.use('agg')
    #Plots the data
    fig, ax = plt.subplots()
    if up_down == True:
        data.plot(color = '#2ECC71')
    elif up_down == False:
        data.plot(color = '#E74C3C')

    #Sets the formatting for the x-axis that allows it to show only the time. y-axis shows the price
    fmt = mdates.DateFormatter('%H:%M', tz = tz.gettz('US/Pacific'))
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
     
    plt.format_xdata = fmt
    plt.grid(True)
    plt.axhline(closing, color = 'k', linestyle='dashed')
    fig.autofmt_xdate()
    
    #Changes the labels and title of the graph
    fig.suptitle(company_name, fontsize = 25)
    plt.xlabel('TIME', fontsize=16)
    plt.ylabel('PRICE', fontsize=16)
    
    #Saves the graph as an image for viewing
    plt.savefig('resources/chart.png', bbox_inches = 'tight', dpi = 200)

    
    #FOR DEBUGGING
    #plt.show()
    #print(data.head())
    #print(data.tail())
