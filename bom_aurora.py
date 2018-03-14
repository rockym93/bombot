#!/usr/bin/env python3
'''Some tools for interacting with the Bureau of Meteorology's Space Weather API at <http://sws-data.sws.bom.gov.au/>'''
import requests

import time

import json

with open('bombot.json') as f:
	config = json.load(f)

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