from .models import Place, Rating
from hedgehog import api_key
import datetime
import requests, json
from operator import itemgetter



class GoogleRequests(object):
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
	details_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
	geo_api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='

	def getMyLocation():
		raw_ipdata = requests.post(GoogleRequests.geo_api_url+api_key)
		ipdata = raw_ipdata.json()
		my_location = {'latitude': ipdata["location"]['lat'], 'longitude': ipdata["location"]['lng'] }
		return my_location

	def getDetailsFromGoogle(place, place_type, location):
		search_term = place + " " + place_type + " in " + location
		r = requests.get(GoogleRequests.url + 'query=' + search_term +
	                        '&key=' + api_key)
		x = r.json()
		y = x['results']
		if len(y) == 0:
			return "No results found"
		elif len(y) == 1:
			place_search_name_words = place.split(" ")
			lowercase_place_search_name_words = [word.lower() for word in place_search_name_words]
			place_search_location_words = location.split(" ")
			lowercase_place_search_location_words = [word.lower() for word in place_search_location_words]
			name = y[0]['name']
			result_name_words = name.split(" ")
			lowercase_result_name_words = [word.lower() for word in result_name_words]
			result_location = y[0]['formatted_address']
			result_location_words = result_location.split(" ")
			lowercase_result_location_words = [word.lower() for word in result_location_words]
			name_match = False
			location_match = False
			for i in lowercase_place_search_location_words:
				if i in (lowercase_result_location_words):
					location_match = True
			for j in lowercase_place_search_name_words:
				if j in lowercase_result_name_words:
					name_match = True
			if name_match == True and location_match == True:
				result = y[0]
				info = {}
				info['name'] = place
				info['location'] = location
				info['type'] = place_type
				info['latitude'] = result['geometry']['location']['lat']
				info['longitude'] = result['geometry']['location']['lng']
				info['street address'] = result['formatted_address']
				info['place_id'] = result['place_id']
				r = requests.get(GoogleRequests. url + 'query=' + search_term +
	                        '&key=' + api_key)
				extra_details = requests.get(GoogleRequests.details_url + info['place_id'] + "&key=" + api_key)
				a = extra_details.json()
				b = a['result']
				for k,v in b.items():
					info[k] = v
				return info
			else: return "No results found"
		else: return "Multiple Results found"


class DBSearch(object):
	def search(search_term):
		"""takes a search term and looks in the hedgehog DB for matches"""
		s = '%'+search_term+'%'
		r = Place.query.filter(Place.name.ilike(s)).all()
		results = []
		for i in r:
			details = DBSearch.getDetails(i.name)
			rating = details['true score']
			no_of_ratings = details['number of ratings']
			place_type = details['type']
			results.append({'name': i.name, \
							'location': i.location, \
							'type': place_type, \
							'rating': rating, 'number of ratings': no_of_ratings})
		sorted_results = sorted(results, key=itemgetter('rating'), reverse=True)
		return sorted_results
	
	def getDetails(placename):
		establishment = Place.query.filter_by(name=placename).first()
		all_ratings = Rating.query.filter_by(eid=establishment.eid).all()
		details = {}
		details['location'] = establishment.location
		details['type'] = establishment.establishment_type
		details['number of ratings'] = Truescore.getTotalRatings(all_ratings)
		details['average rating'] = Truescore.getAvgScore(all_ratings)
		details['true score'] = Truescore.calculateTrueScore(all_ratings)
		details['comments'] = Truescore.getComments(all_ratings)
		return details
		
	def placesNearMe():
		my_location = GoogleRequests.getMyLocation()
		lat = my_location['latitude']
		longi = my_location['longitude']	
		closeness = 0.02
		close_places = Place.query.filter(Place.latitude.between(lat-closeness, lat+closeness)). \
						filter(Place.longitude.between(longi-closeness, lat-closeness)).all() 
		results = []
		for place in close_places:
			results.append({'eid':place.eid, 'name':place.name, 'location': place.location, 'type': place.establishment_type})
		return results


class Truescore(object):

	def getTotalRatings(ratings):
		return len(ratings)

	def getPositiveComments(ratings):
		comments = []
		for rating in ratings:
			comments.append(rating.pros)
		return comments

	def getNegativeComments(ratings):
		comments = []
		for rating in ratings:
			comments.append(rating.cons)
		return comments

	def getAvgScore(ratings):
		total = 0
		number_of_ratings = len(ratings)
		scores = []
		for rating in ratings:
			total += rating.rating
		if number_of_ratings > 0:
			average = total / number_of_ratings
		else: average = "N/A"
		return average

	def calculateTrueScore(ratings):
		"""looks at the number of ratings, recency of ratings and person behind
		each rating and plots on scale of 0 - 100 """
		#for each vote 3 weighting functions to give final weight from 0 - 100
		all_ratings = []
		effective_number_of_votes = 0
		effective_total = 0
		for rating in ratings:
			if rating.rater == '0':
				all_ratings.append({'rater': rating.rater, 'date': rating.date, \
									'rating': rating.rating, 'weight':1})
			else:
				voter_weight = Truescore.calculateRaterWeight(rating)
				recency_weight = Truescore.calculateRecencyWeight(rating)
				proximity_weight = Truescore.calculateProximityWeight(rating)
				weighting = (voter_weight + recency_weight + proximity_weight) / 3
				all_ratings.append({'rater': rating.rater, 'date': rating.date, \
									'rating': rating.rating, 'weight':weighting})
		for i in all_ratings:
			effective_number_of_votes +=  i['weight']
			effective_total += i['weight'] * i['rating']
		if len(all_ratings) > 0:
			score = 20 * effective_total / effective_number_of_votes
		else:
			score = 50
		true_score = Truescore.adjustForRatingsVolume(score, len(all_ratings))
		return true_score

	def getComments(ratings):
		comments = {'pros': [], 'cons': []}
		for i in ratings:
			if i.pros:
				comments['pros'].append(i.pros)
			if i.cons:
				comments['cons'].append(i.cons)
		return comments

	def calculateRaterWeight(rating):
		if rating.rater == 0:
			return 1
		else:
			all_ratings = Rating.query.filter_by(rater=rating.rater).all()
			lifetime_ratings = len(all_ratings)
			lifetime_total = 0

			for i in all_ratings:
				lifetime_total += i.rating
			lifetime_average = lifetime_total / lifetime_ratings
			if lifetime_ratings < 2:
				rater_volume_weighting = 1
			elif lifetime_ratings < 3:
				rater_volume_weighting = 2
			elif lifetime_ratings < 5:
				rater_volume_weighting = 3
			elif lifetime_ratings < 8:
				rater_volume_weighting = 5
			elif lifetime_ratings < 13:
				rater_volume_weighting = 8
			elif lifetime_ratings < 20:
				rater_volume_weighting = 13
			else:
				rater_volume_weighting = 20
			return rater_volume_weighting 
		
	def calculateRecencyWeight(rating):
		today = datetime.datetime.today()
		days_ago = today - rating.date
		number_of_days = days_ago.days
		if number_of_days < 7:
			return 10
		elif number_of_days < 21:
			return 5
		elif number_of_days < 100:
			return 3
		else: return 1

	def calculateProximityWeight(rating):
		user_lat = rating.latitude
		user_lng = rating.longitude
		place = Place.query.filter_by(eid=rating.eid).first()
		place_lat = place.latitude
		place_lng = place.longitude
		proximity = abs(place_lat - user_lat) + abs(place_lng - user_lng)
		if proximity > 5:
			proximity_weighting = 1
		elif proximity > 2:
			proximity_weighting = 3
		elif proximity > 1:
			proximity_weighting = 5
		elif proximity > 0.5:
			proximity_weighting = 10
		elif proximity > 0.25:
			proximity_weighting = 20
		elif proximity > 0.1:
			proximity_weighting = 30
		elif proximity < 0.1:
			proximity_weighting = 50
		else: proximity_weighting = 1
		return proximity_weighting

	def adjustForRatingsVolume(score, number_of_ratings):
		delta = abs(score - 50)
		if number_of_ratings < 2:
			new_delta = delta / 5
		elif number_of_ratings < 5:
			new_delta = delta / 3
		elif number_of_ratings < 10:
			new_delta = delta / 2
		elif number_of_ratings < 25:
			new_delta = delta / 1.5
		else: new_delta = delta

		if score < 50:
			new_score = 50 - new_delta
		else: new_score = 50 + new_delta
		return int(new_score)







