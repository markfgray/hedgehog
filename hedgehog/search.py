import requests, json



url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"


def query(search_term):
	r = requests.get(url + 'query=' + search_term +
                        '&key=' + api_key)
	x = r.json()
	y = x['results']
	results = []
	for result in y:
		results.append({'name': result['name'], 'type': result['types']})
	return results