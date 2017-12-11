# gdax_testing
testing with gdax api and pushover notification system

# requirements:

pip install gdax

pip install python-pushover

# Price_Alert.py

Uses a credentials.py file which houses a pushover token "push_token" and a pushover user key "push_user"

Monitors the GDAX current price using their api. It keeps track of the local low and high that it sees and is kept through script restarts
using pickle to store the dictionary to file. Script alerts you at the set intervals in the beginning of the script via pushover notification.
Also alerts you when a new local low or local high has been hit.

You can reset the local high and local low data by stopping the script, removing the historical_data.dict file.
