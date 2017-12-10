from pprint import pprint
import gdax, time
import os, sys
from pushover import Client
import credentials
from datetime import datetime
from time import sleep

#create variables and step points
numbers = list(range(1000,25000,1000))

alert_variables = {}
for n,y in enumerate(numbers):
    c = n+1
    alert_variables[c] = {}
    alert_variables[c]['price'] = y
    alert_variables[c]['alert'] = True

# set initial time
time = datetime.now()
high_price_time = time
low_price_time = time
alert_state = True
i = 1

#get information
client = Client(credentials.push_user, api_token=credentials.push_token)
public_client = gdax.PublicClient()

#set initial pricing
low_price = float(public_client.get_product_ticker(product_id='BTC-USD')['price'])
high_price = low_price

def time_format(time):
    return str(str(time.month) +"/"+ str(time.day)+"/"+ str(time.year)+" "+str(time.time().strftime('%I:%M:%S %p')))

def t_delta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return str(hours)+":"+str(minutes)+":"+str(seconds)

def money_format(money):
    return str('${:,.2f}'.format(float(money)))

def alerts(limits,current_price,under_var,alert_state):
    tops = "\nHigh: "+limits['high_price']+" @: "+limits['high_price_time']\
    +"\nLow: "+limits['low_price']+" @: "+limits['low_price_time']\
    +"\n24 Hour High: "+limits['past_day_high']+"\n24 Hour Low: "+limits['past_day_low']
    if current_price < under_var:
        #print("price is under "+str(under_var))
        if alert_state: #if under alert is true
            message = "UNDER " +money_format(under_var)
            client.send_message(current_price_USD+tops, title=message)
            alert_state = False #turn off alert

    if current_price > under_var:
        #print("price is over "+str(under_var))
        if not alert_state: #if false from being under 15000
            message = "OVER "+money_format(under_var)
            client.send_message(current_price_USD+tops, title=message)
            alert_state = True #sets the alert to happen if it goes under the val
    return alert_state

while True:

    limits = {} #create var dictionary
    time = datetime.now() #get current time


    try: #get current pricing
        current_price = float(public_client.get_product_ticker(product_id='BTC-USD')['price'])
        current_price_USD = money_format(current_price)
    except Exception:
        current_price = 0
        current_price_USD = 0

    if current_price > high_price: #if new high_price
        high_price = current_price
        high_price_time_gap = time - high_price_time #calculate high price time gap since last nigh price
        print(t_delta(high_price_time_gap))
        high_price_time = time
        message = current_price_USD+" @: "+time_format(time)+"\nGap: "+t_delta(high_price_time_gap)
        client.send_message(message, title="LOCAL HIGH")
    if current_price < low_price:
        low_price = current_price
        low_price_time_gap = time - low_price_time
        print(t_delta(low_price_time_gap))
        low_price_time = time
        message = current_price_USD+" @: "+time_format(time)+"\nGap: "+t_delta(low_price_time_gap)
        client.send_message(current_price_USD+"\n"+time_format(time), title="LOCAL LOW")

    try:
        past_day_data = public_client.get_product_24hr_stats('BTC-USD')
        past_day_high = past_day_data['high']
        past_day_low = past_day_data['low']

    except Exception:
        past_day_high = 0
        past_day_low = 0

    limits['high_price'] = money_format(high_price)
    limits['high_price_time'] = time_format(high_price_time)
    limits['low_price'] = money_format(low_price)
    limits['low_price_time'] = time_format(low_price_time)
    limits['past_day_high'] = money_format(past_day_high)
    limits['past_day_low'] = money_format(past_day_low)

    for var in alert_variables: #sets up alerts, keeps track with dictionary
        alert_variables[var]['alert'] = alerts(limits,current_price,alert_variables[var]['price'],alert_variables[var]['alert'])
        if alert_variables[var]['alert'] == False:
            for var2 in alert_variables: #for other prices in the list
                if alert_variables[var]['price'] < alert_variables[var2]['price']: #if current price is lower than second price
                    alert_variables[var2]['alert'] = False #set alert to false as well - do not get under 16,000 and 17,000 if price is 15500

    if current_price == past_day_high:
        client.send_message(current_price_USD+"\n"+time_format(time), title="24 HOUR HIGH")
    if current_price == past_day_low:
        client.send_message(current_price_USD+"\n"+time_format(time), title="24 HOUR LOW")

    print("CURRENT: "+str(current_price_USD))
    print("LOW: "+money_format(low_price)+" At: "+time_format(low_price_time))
    print("HIGH: "+money_format(high_price)+ " At: "+time_format(high_price_time))
    print()
    print("24 HOUR LOW: "+money_format(past_day_low))
    print("24 HOUR HIGH: "+money_format(past_day_high))

    print()
    sleep(60)
