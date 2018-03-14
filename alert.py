#!/usr/bin/env/python3
'''this script runs every so often and checks if there's been an alert posted. 
If there has, it notifies the chats which have subscribed.'''

import bom_aurora as bom
import json 

with open('bombot.json') as f:
	config = json.load(f)

def sendalerts(alerttext):
	for chat in config['alerts']:
		tosend = {
		'chat_id': chat,
		'text': alerttext
		}
		requests.post('https://api.telegram.org/' + config['botkey'] + '/sendMessage', params=tosend)

current = bom.getalert()

#if the alert has changed, push it to subscribers and save the new alert.
if current != config['previous'] and current is not None:
    sendalerts(current)
    config['previous'] = current
    with open('bombot.json','w') as f:
        json.dump(config,f)
