import os
import datetime as dt
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas_datareader.data as web
import pandas as pd
from dateutil import tz

def get_daily_info(symbol='AAPL', period = '1d', data_intervals='1m'):
    #Retrieves the minute to minute data from Yahoo Finance
    data = yf.download(symbol, period = period, interval = data_intervals)['Adj Close']
    matplotlib.use('agg')
    #Plots the data
    fig, ax = plt.subplots()
    data.plot()

    #Sets the formatting for the x-axis that allows it to show only the time. y-axis shows the price
    fmt = mdates.DateFormatter('%H:%M', tz = tz.gettz('US/Pacific'))
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.tick_right()
     
    plt.format_xdata = fmt
    plt.format_ydata = lambda x: '$&1.2f' % x
    plt.grid(True)
    fig.autofmt_xdate()
    
    #Changes the labels and title of the graph
    fig.suptitle(symbol, fontsize = 25)
    plt.xlabel('TIME', fontsize=16)
    plt.ylabel('PRICE', fontsize=16)
    
    #Saves the graph as an image for viewing
    plt.savefig('resources/chart.png',dpi = 200)
    
    #FOR DEBUGGING
    #plt.show()
    #print(data.head())
    #print(data.tail())
