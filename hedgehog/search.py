from .models import Place, Rating

def getDetails(placename):
	establishment = Place.query.filter_by(name=placename).first()
	all_ratings = Rating.query.filter_by(eid=establishment.eid).all()
	details = {}
	details['location'] = establishment.location
	details['number of ratings'] = getTotalRatings(all_ratings)
	details['average score'] = getAvgScore(all_ratings)
	print(details)
	return details

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
	scores = []
	for rating in ratings:
		total += rating.rating
	return total





