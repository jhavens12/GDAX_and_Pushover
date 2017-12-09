from pprint import pprint
import gdax, time
import os, sys
from pushover import Client
import credentials
from datetime import datetime
from time import sleep


alert_variables = {1: {'price': '16000', 'alert': True}, 2:{'price': '15000', 'alert': True}, 3: {'price': '14000', 'alert': True}, 4:{'price': '13000', 'alert': True}}

print (alert_variables[1]['price'])
# set variables
over_var = "20000"
under_var = "15000"

# set initial time
time = datetime.now()
high_price_time = time
low_price_time = time
alert_state = True
i = 1

#get information
client = Client(credentials.push_user, api_token=credentials.push_token)
public_client = gdax.PublicClient()

low_price = public_client.get_product_ticker(product_id='BTC-USD')['price']
high_price = low_price

def time_format(time):
    return str(time.month) +"/"+ str(time.day)+"/"+ str(time.year)+" "+str(time.time().strftime('%I:%M:%S %p'))

def alerts(i,current_price,under_var,alert_state):
    if current_price < under_var:
        print("price is under "+str(under_var))
        if alert_state: #if under alert is true
            message = "UNDER " +str(under_var)
            client.send_message(current_price_USD, title=message)
            alert_state = False #turn off alert
        if not alert_state: #if set to false (already under)
            if i == 0: #but the loop restarts
                message = "UNDER! REPEAT" #send a repeat alert
                client.send_message(current_price_USD, title=message)

    if current_price > under_var:
        print("price is over "+str(under_var))
        if not alert_state: #if false from being under 15000
            message = "Gone Over "+under_var
            client.send_message(current_price_USD, title=message)
            alert_state = True #sets the alert to happen if it goes under the val
    return alert_state

while True:
    i = i+1
    if i == 12: #every 120 cycles - reset alert variables (30 second variables means every 1 hour)
        i = 0

    time = datetime.now()
    #stamp = str(time.month) +"/"+ str(time.day)+"/"+ str(time.year)+" "+str(time.time().strftime('%I:%M %p'))

    current_price = public_client.get_product_ticker(product_id='BTC-USD')['price']
    current_price_USD = '${:,.2f}'.format(float(current_price))

    if current_price > high_price:
        high_price = current_price
        high_price_time = time
    if current_price < low_price:
        low_price = current_price
        low_price_time = time

    #sets alert settings and sends when necessary
    for var in alert_variables:
        alert_variables[var]['alert'] = alerts(i,current_price,alert_variables[var]['price'],alert_variables[var]['alert'])

    print("CURRENT: "+current_price_USD)
    print("LOW: "+low_price+" At: "+time_format(low_price_time))
    print("HIGH: "+high_price+ "At: "+time_format(high_price_time))

    print(i)
    print()
    sleep(5)
