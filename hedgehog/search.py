from .models import Place, Rating
from hedgehog import api_key
import datetime
import requests, json

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

def getDetails(placename):
	establishment = Place.query.filter_by(name=placename).first()
	all_ratings = Rating.query.filter_by(eid=establishment.eid).all()
	details = {}
	details['location'] = establishment.location
	details['number of ratings'] = getTotalRatings(all_ratings)
	details['average rating'] = getAvgScore(all_ratings)
	details['true score'] = calculateTrueScore(all_ratings)
	return details

def getPlaceInfo(place, place_type, location):
	search_term = place + " " + place_type + " in " + location
	r = requests.get(url + 'query=' + search_term +
                        '&key=' + api_key)
	x = r.json()
	y = x['results']
	#need to check that the name given by the user matches the name returned by the api
	#then take te data for that specific one
	if len(y) > 0:
		result = y[0]
		info = {}
		info['name'] = place
		info['location'] = location
		info['type'] = place_type
		info['latitude'] = result['geometry']['location']['lat']
		info['longitude'] = result['geometry']['location']['lng']
		return info
	else:
		return "No results found"


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
	average = total / number_of_ratings
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
			voter_weight = calculateRaterWeight(rating)
			recency_weight = calculateRecencyWeight(rating)
			proximity_weight = calculateProximityWeight(rating)
			print('pw: ', proximity_weight)
			weighting = (voter_weight + recency_weight + proximity_weight) / 3
			all_ratings.append({'rater': rating.rater, 'date': rating.date, \
								'rating': rating.rating, 'weight':weighting})
	for i in all_ratings:
		effective_number_of_votes +=  i['weight']
		effective_total += i['weight'] * i['rating']
	true_score = effective_total / effective_number_of_votes
	print(all_ratings)
	print("effective_total: ", effective_total)
	print("effective_number_of_votes: ", effective_number_of_votes)
	return true_score

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
	print("prox = ", proximity)
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






