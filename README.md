# gdax_testing
testing with gdax api and pushover notification system

# requirements:

pip3 install gdax (https://github.com/danpaquin/gdax-python)

pip3 install python-pushover (https://github.com/Thibauth/python-pushover)

# Price_Alert.py

Run this script from an always on computer (or something like a raspberry pi) to continuously monitor the GDAX trading price and never miss a dip (or high) again with notifications right to your phone. Requires a pushover.net account and the app to be set up on your phone (or device)

Uses a credentials.py file which houses a pushover token "push_token" and a pushover user key "push_user"

    push_token = "xxxx"
    push_user = "xxxx"

Monitors the GDAX current price using their api and the gdax python package from danpaquin. The script will send a notification every time the price goes over/under the set steps that you set up in the Price_Alert.py file (ex. every 1000 will alert you when the price goes over/under 15,000 16,000 17,000 etc). You can also set the start amount and end amount if you wish so you can monitor specfic price points.

The following config will alert you every $1,000 starting at $1,000 and going up to $30,000 every 60 seconds.

    bottom_alert = 1000 #min number in range
    top_alert = 30000 #max number in range
    step_amount = 1000 #amount to be alerted at
    refresh_rate = 60 #seconds


Script alerts you of these intervals via pushover notification. Notifications also include the local high/low based on the GDAX api response based on the last 24 hours.

Also alerts you when a new local low or local high has been hit (Since the script has been running or pulled from the historical_data.dict file). The Gap in the notification lists how long its been since a new local high/low has been hit (hours, minutes, seconds)


You can reset the local high and local low data by stopping the script, removing the historical_data.dict file.

# Example Notification Format:
  
  OVER $16,000.00
    
    $16,048.98
    High: $16,199.99 @: 12/10/2017 06:05:51 PM
    Low: $14,677.03 @: 12/10/2017 05:56:42 PM
    24 Hour High: $16,300.00
    24 Hour Low: $13,501.00
    
  LOCAL HIGH
    
    $16,245.00 $: 12/10/2017 09:19:35 PM
    Gap: 3:13:43
