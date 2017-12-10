from pprint import pprint
import gdax, time
import os, sys
from pushover import Client
import credentials
import datetime
from time import sleep

# time = datetime.datetime.now()
# week_ago = time - datetime.timedelta(weeks=0, days=+7)
#
# print(week_ago)
public_client = gdax.PublicClient()
#
# pprint(public_client.get_product_24hr_stats('BTC-USD'))

#pprint(public_client.get_product_historic_rates('BTC-USD', granularity=3000, start=week_ago.isoformat(), end=time.isoformat()))

result = public_client.get_product_ticker(product_id='BTC-USD')
print (result.status_code)
