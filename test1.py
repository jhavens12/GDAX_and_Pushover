from pprint import pprint
import gdax, time
import os, sys
from pushover import Client
import credentials
from datetime import datetime
from time import sleep



# set variables
over_var = "20000"
under_var_1 = "15000"
under_var_2 = "10000"

# set initial time
time = datetime.now()
high_price_time = time
low_price_time = time
send_under_alert_1 = True
i = 1

#get information
client = Client(credentials.push_user, api_token=credentials.push_token)
public_client = gdax.PublicClient()

low_price = public_client.get_product_ticker(product_id='BTC-USD')['price']
high_price = low_price

def time_format(time):
    return str(time.month) +"/"+ str(time.day)+"/"+ str(time.year)+" "+str(time.time().strftime('%I:%M:%S %p'))

while True:
    i = i+1
    if i == 12: #every 120 cycles - reset alert variables (30 second variables means every 1 hour)
        i = 0
#        send_under_alert = True #reset alert to repeat

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
    #under_var_1
    if current_price < under_var_1:
        print("price is under "+str(under_var_1))
        if send_under_alert_1: #if under alert is true
            if i == 0:
                message = "UNDER! REPEAT"
            else:
                message = "UNDER!"
            client.send_message(current_price_USD, title=message)
            send_under_alert_1 = False #turn off alert

    if current_price > under_var_1:
        print("price is over "+str(under_var_1))
        if not send_under_alert_1: #if false from being under 15000
            client.send_message(current_price_USD, title="Gone Over")
            send_under_alert_1 = True #sets the alert to happen if it goes under the val

    ###

    print("CURRENT: "+current_price_USD)
    print("LOW: "+low_price+" At: "+time_format(low_price_time))
    print("HIGH: "+high_price+ "At: "+time_format(high_price_time))

    print(i)
    sleep(5)
