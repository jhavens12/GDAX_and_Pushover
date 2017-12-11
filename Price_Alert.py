from pprint import pprint
import gdax, time
import os, sys
from pushover import Client
import credentials
from datetime import datetime
from time import sleep
import pickle
from pathlib import Path

#create variables and step points
bottom_alert = 1000 #min number in range
top_alert = 30000 #max number in range
step_amount = 1000 #amount to be alerted at
refresh_rate = 60 #seconds

#######
numbers = list(range(bottom_alert,top_alert,step_amount))

alert_variables = {}
for n,y in enumerate(numbers):
    c = n+1
    alert_variables[c] = {}
    alert_variables[c]['price'] = y
    alert_variables[c]['alert'] = True

#sets external information
client = Client(credentials.push_user, api_token=credentials.push_token)
public_client = gdax.PublicClient()

# set initial time
time = datetime.now()
alert_state = True
i = 1

#check to see if file exists, if yes do below, if no create file and dictionary
limit_file = Path("./historical_pricing.dict")
if limit_file.is_file():
#pricing import
    pickle_in = open("historical_pricing.dict","rb")
    limits = pickle.load(pickle_in)
else:
    f=open("historical_pricing.dict","w+") #create file
    f.close()
    limits = {} #create limits dict and variables
    limits['high_price_time'] = time
    limits['low_price_time'] = time
    limits['low_price'] = limits['high_price'] = float(public_client.get_product_ticker(product_id='BTC-USD')['price'])

    pickle_out = open("historical_pricing.dict","wb") #open file
    pickle.dump(limits, pickle_out) #save limits dict to file
    pickle_out.close()

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
    tops = "\nHigh: "+money_format(limits['high_price'])+" @: "+time_format(limits['high_price_time'])\
    +"\nLow: "+money_format(limits['low_price'])+" @: "+time_format(limits['low_price_time'])\
    +"\n24 Hour High: "+money_format(limits['past_day_high'])+"\n24 Hour Low: "+money_format(limits['past_day_low'])

    if current_price < under_var:
        if alert_state: #if under alert is true
            message = "UNDER " +money_format(under_var)
            client.send_message(current_price_USD+tops, title=message)
            alert_state = False #turn off alert

    if current_price > under_var:
        if not alert_state: #if false from being under 15000
            message = "OVER "+money_format(under_var)
            client.send_message(current_price_USD+tops, title=message)
            alert_state = True #sets the alert to happen if it goes under the val
    return alert_state

while True:

    time = datetime.now() #get current time

    try: #get current pricing
        current_price = float(public_client.get_product_ticker(product_id='BTC-USD')['price'])
        current_price_USD = money_format(current_price)
    except Exception:
        current_price = 0
        current_price_USD = 0


    # add support for the last high price time/amount in notification?
    if current_price > limits['high_price']: #if new high_price
        limits['high_price_old'] = limits['high_price']
        limits['high_price'] = current_price
        high_price_time_gap = time - limits['high_price_time'] #calculate high price time gap since last nigh price
        print(t_delta(high_price_time_gap))
        limits['high_price_time_old'] = limits['high_price_time']
        limits['high_price_time'] = time
        message = current_price_USD+" @: "+time_format(time)+"\n"+money_format(limits['high_price_old'])\
        +" @: "+time_format(limits['high_price_time_old'])+" (OLD)")+"\nGap: "+str(t_delta(high_price_time_gap))
        print(message)
        client.send_message(message, title="LOCAL HIGH")
    if current_price < limits['low_price']:
        limits['low_price_old'] = limits['low_price']
        limits['low_price'] = current_price
        low_price_time_gap = time - limits['low_price_time']
        print(t_delta(low_price_time_gap))
        limits['low_price_time_old'] = limits['low_price_time']
        limits['low_price_time'] = time
        message = current_price_USD+" @: "+time_format(time)+"\n"+money_format(limits['low_price_old'])\
        +" @: "+time_format(limits['low_price_time_old'])+" (OLD)"+"\nGap: "+t_delta(low_price_time_gap)
        print(message)
        client.send_message(message, title="LOCAL LOW")

    try:
        past_day_data = public_client.get_product_24hr_stats('BTC-USD')
        limits['past_day_high'] = past_day_data['high']
        limits['past_day_low'] = past_day_data['low']

    except Exception:
        print("no response for 24 hour values")

    for var in alert_variables: #sets up alerts, keeps track with dictionary
        alert_variables[var]['alert'] = alerts(limits,current_price,alert_variables[var]['price'],alert_variables[var]['alert'])
        if alert_variables[var]['alert'] == False:
            for var2 in alert_variables: #for other prices in the list
                if alert_variables[var]['price'] < alert_variables[var2]['price']: #if current price is lower than second price
                    alert_variables[var2]['alert'] = False #set alert to false as well - do not get under 16,000 and 17,000 if price is 15500

    print("CURRENT: "+str(current_price_USD))
    print("LOW: "+money_format(limits['low_price'])+" At: "+time_format(limits['low_price_time']))
    print("HIGH: "+money_format(limits['high_price'])+ " At: "+time_format(limits['high_price_time']))
    print()
    print("24 HOUR LOW: "+money_format(limits['past_day_low']))
    print("24 HOUR HIGH: "+money_format(limits['past_day_high']))

    print()
    #save limits dictionary to file for next run of entire script, not this loop
    pickle_out = open("historical_pricing.dict","wb")
    pickle.dump(limits, pickle_out)
    pickle_out.close()
    sleep(refresh_rate)
