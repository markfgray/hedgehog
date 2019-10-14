import requests, json, datetime
from hedgehog import api_key, db
from flask import request
from .models import Place, Rating
from .search import getPlaceInfo, getMyLocation


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

def postReview(placename, form_data, user):
	"""takes a place name, form data and the user and posts to the ratings table
	with details fo that review"""
	establishment = Place.query.filter_by(name=placename).first()
	my_location = getMyLocation()
	form = form_data
	date = datetime.date.today()
	best_bits = form['best_bits']	
	worst_bits = form['worst_bits']
	rating = int(form['rating'])
	eid = establishment.eid
	latitude = my_location['latitude']
	longitude = my_location['longitude']
	new_rating = Rating(date, user, placename, rating, best_bits, worst_bits, eid, latitude, longitude)
	db.session.add(new_rating)
	db.session.commit()
	return "added to DB"

def reviewNewPlace(form_data, user):
	place = form_data['place']
	place_type = form_data['place_type']
	location = form_data['location']
	place_info = getPlaceInfo(place, place_type, location)
	if type(place_info) is dict:
		est_type = place_info['type']
		est_name = place_info['name']
		est_lat = place_info['latitude']
		est_long = place_info['longitude']
		est_facs = "placeholder"
		est_location = place_info['location']
		new_place = Place(est_type, est_name, est_lat, est_long, est_facs, est_location)
		db.session.add(new_place)
		db.session.commit()
		establishment = Place.query.filter_by(name=est_name).first()
		my_location = getMyLocation()
		form = form_data
		date = datetime.date.today()
		best_bits = form['best_bits']	
		worst_bits = form['worst_bits']
		rating = int(form['rating'])
		eid = establishment.eid
		latitude = my_location['latitude']
		longitude = my_location['longitude']
		new_rating = Rating(date, user, est_name, rating, best_bits, worst_bits, eid, latitude, longitude)
		db.session.add(new_rating)
		db.session.commit()
		return "New review added"
	else: return "failed"


def suggestNewPlace(form_data):
	place = form_data['place']
	place_type = form_data['place_type']
	location = form_data['location']
	place_info = getPlaceInfo(place, place_type, location)
	if type(place_info) is dict:
		est_type = place_info['type']
		est_name = place_info['name']
		est_lat = place_info['latitude']
		est_long = place_info['longitude']
		est_facs = "placeholder"
		est_location = place_info['location']
		new_place = Place(est_type, est_name, est_lat, est_long, est_facs, est_location)
		db.session.add(new_place)
		db.session.commit()
		return "Place Added"
	else:
		return "failed"


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
