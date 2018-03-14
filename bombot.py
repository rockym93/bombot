#!/usr/bin/env python3

import lazybot as bot
import bom_aurora as bom
import json

with open('bombot.json') as f:
	config = json.load(f)

bot.key = config['botkey']



### Command Definitions ###

def bothelp(message):
	helptext = '''I can help you spot the Aurora Australis from Australia.

Send me the name of a major city to get a k-index, or /alerts to turn alerts on or off.'''
	tosend = {
	'chat_id': message['chat']['id'],
	'reply_to_message': message['message_id'],
	'text': helptext
	}
	bot.api('sendMessage', tosend)

bot.commands['/help'] = bothelp

def setalerts(message):
	chatid = message['chat']['id']
	if chatid in config['alerts']:
		config['alerts'].remove(chatid)
		subtext = 'Alerts disabled.'
	else:
		config['alerts'].append(chatid)
		subtext = 'Alerts enabled.'
	
	with open('bombot.json','w') as f:
		json.dump(config,f)

	tosend = {
	'chat_id': message['chat']['id'],
	'reply_to_message': message['message_id'],
	'text': subtext
	}
	bot.api('sendMessage', tosend)

bot.commands['/alerts'] = setalerts

def sendalerts(alerttext):
	for chat in config['alerts']:
		tosend = {
		'chat_id': chat,
		'text': alerttext
		}
	bot.api('sendMessage', tosend)

def location(message):
	city = message['text']

	#Remove @usernames - they confuse the BOM api.
	city = ' '.join([i for i in city.split() if not i.startswith('@')])
	
	tosend = {
	'chat_id': message['chat']['id'],
	'reply_to_message': message['message_id'],
	'text': bom.getkindex(city)
	}
	bot.api('sendMessage', tosend)

bot.handlers['text'] = location

### END COMMAND DEFINITIONS ###

bot.processupdate()
