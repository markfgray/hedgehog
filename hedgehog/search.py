import requests, json
from hedgehog import api_key



url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
details_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='

def query(search_term):
	r = requests.get(url + 'query=' + search_term +
                        '&key=' + api_key)
	x = r.json()
	y = x['results']
	results = []
	for result in y:
		place_id = result['place_id']
		a = requests.get(details_url + place_id + '&fields=rating&key=' + api_key)
		b = a.json()
		google_rating = b['result']['rating']
		rating = truscore(google_rating)
		results.append({'name': result['name'], 'type': result['types'], 'rating': str(rating)})
	return results

def truscore(rating):
	multiplied_rounded_rating = round(rating * 20)
	return multiplied_rounded_rating