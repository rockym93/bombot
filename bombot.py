#!/usr/bin/env python3

import lazybot as bot

import requests

import time

import json

with open('bombot.json') as f:
	config = json.load(f)

bot.key = config['botkey']

def getkindex(location):
	'''generic function for grabbing k-index data for a given location'''
	q = {
		'api_key': config['bomkey'],
		'options': {'location':location}
	}
	bomdata = requests.post('http://sws-data.sws.bom.gov.au/api/v1/get-k-index', data=json.dumps(q)).json()
	k = "unknown"
	try:
		k = str(bomdata['data'][0]['value'])
	except KeyError:
		pass
	
	kindex = "The current k-index for " + location + " is " + k +'.'

	return kindex

def getalert():
	'''generic function for grabbing current aurora alert data'''
	q = {
		'api_key': config['bomkey'],
	}
	bomdata = requests.post('http://sws-data.sws.bom.gov.au/api/v1/get-aurora-alert', data=json.dumps(q)).json()
	alert = None
	try:
		alert = bomdata['data'][0]['description']
	except IndexError:
		pass
	return alert

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
	
	tosend = {
	'chat_id': message['chat']['id'],
	'reply_to_message': message['message_id'],
	'text': getkindex(city)
	}
	bot.api('sendMessage', tosend)

bot.handlers['text'] = location

### END COMMAND DEFINITIONS ###

bot.processupdate()
