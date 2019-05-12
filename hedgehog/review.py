import requests, json
from hedgehog import api_key



url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

def placesNearMe():
	location = '51.663392, -0.396565'
	radius = '500'
	r = requests.get(url + 'location=' + location + '&radius=' + radius + '&key=' + api_key)
	x = r.json()
	y = x['results']
	accepted_types = ['lodging', 'food']
	results = []
	for result in y:
		for placetype in result['types']:
			if placetype in accepted_types:
				results.append({'name': result['name'], 'type': result['types']})
	print(x)
	return results