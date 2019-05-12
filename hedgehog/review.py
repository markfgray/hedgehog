import requests, json
from hedgehog import api_key, app, ip_key
from flask import request


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
ip_url = 'http://api.ipstack.com/134.201.250.155?access_key='

def placesNearMe():
	clinetip = request.remote_addr
	raw_ipdata = requests.get(ip_url+ip_key)
	ipdata = raw_ipdata.json()
	lat = str(ipdata['latitude'])
	longi = str(ipdata['longitude'])
	location = lat + ", " + longi
	radius = '2000'
	r = requests.get(url + 'location=' + location + '&radius=' + radius + '&key=' + api_key)
	x = r.json()
	y = x['results']
	accepted_types = ['lodging', 'food', 'bar', 'restaurant']
	results = []
	for result in y:
		for placetype in result['types']:
			if placetype in accepted_types:
				results.append({'name': result['name'], 'type': result['types']})
	return results