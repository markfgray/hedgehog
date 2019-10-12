import requests, json
from hedgehog import api_key
from flask import request
from .models import Place


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
geo_api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='

def getMyLocation():
	raw_ipdata = requests.post(geo_api_url+api_key)
	ipdata = raw_ipdata.json()
	my_location = {'latitude': ipdata["location"]['lat'], 'longitude': ipdata["location"]['lng'] }
	return my_location

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
	my_location = getMyLocation()
	lat = my_location['latitude']
	longi = my_location['longitude']	
	closeness = 0.02
	close_places = Place.query.filter(Place.latitude.between(lat-closeness, lat+closeness)). \
					filter(Place.longitude.between(longi-closeness, lat-closeness)).all() 
	results = []
	for place in close_places:
		results.append({'eid':place.eid, 'name':place.name})
	return results
	
