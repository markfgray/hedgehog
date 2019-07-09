import requests, json
from hedgehog import api_key, app
from flask import request


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
geo_api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='

def placesNearMe():
	raw_ipdata = requests.post(geo_api_url+api_key)
	ipdata = raw_ipdata.json()
	print(ipdata)
	lat = str(ipdata["location"]['lat'])
	longi = str(ipdata["location"]['lng'])
	location = lat + ", " + longi
	radius = '2000'
	r = requests.get(url + 'location=' + location + '&radius=' + radius + '&key=' + api_key)
	x = r.json()
	y = x['results']
	print(y)
	accepted_types = ['lodging', 'food', 'bar', 'restaurant']
	results = []
	for result in y:
		for placetype in result['types']:
			if placetype in accepted_types:
				results.append({'name': result['name'], 'type': result['types']})
	return results