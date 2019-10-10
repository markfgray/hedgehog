import requests, json
from hedgehog import api_key, app
from flask import request
from .models import Place


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
geo_api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='

def allPlacesNearMeAccordingToGoogle():
	raw_ipdata = requests.post(geo_api_url+api_key)
	ipdata = raw_ipdata.json()
	lat = str(ipdata["location"]['lat'])
	longi = str(ipdata["location"]['lng'])
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


def placesNearMe():
	raw_ipdata = requests.post(geo_api_url+api_key)
	ipdata = raw_ipdata.json()
	lat = str(ipdata["location"]['lat'])
	longi = str(ipdata["location"]['lng'])
	location = lat + ", " + longi
	#51.6513792, -0.3907584
	all_places = Place.query.all()
	results = []
	for place in all_places:
		results.append({'eid':place.eid, 'name':place.name})
	return results
	
