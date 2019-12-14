from hedgehog import app, db, api_key
from flask import render_template, request, url_for, redirect, session
import datetime, requests
from .forms import SearchForm, LoginForm, SignupForm, ReviewForm
from .review import Review
from .search import DBSearch, GoogleRequests
from .models import User, Rating, Place
from .wordcloudgenerator import generate

photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "GET":
		form = SearchForm()
		return render_template('index.html', form=form, name=session.get('name'))
	else:
		search_term = request.form['search']
		return search(search_term)

@app.route('/search', methods=["GET"])
def search(search_term):
	form = ReviewForm()
	results = DBSearch.search(search_term)	
	return render_template('results.html', results=results, search_term=search_term, form=form, name=session.get('name'))

@app.route('/about', methods=["GET"])
def about():	
	return render_template('about.html', name=session.get('name'))

@app.route('/findPlaces', methods=["GET"])
def findPlaces(search_term):
	form = ReviewForm()
	results = DBSearch.search(search_term)	
	return render_template('placestoreview.html', results=results, search_term=search_term, form=form)


@app.route('/reviewpage/<placename>', methods=["GET", "POST"])
def postAReview(placename):
	if request.method == "GET":
		form = ReviewForm()
		return render_template('reviewpage.html', placename=placename, form=form)
	else:
		if session.get('user_id'):
			rater = session.get('user_id')
		else: rater = 0
		Review.existing(placename, request.form, rater)
		return redirect(url_for('index', name=session.get('name')))

@app.route('/details/<placename>', methods=["GET","POST"])
def placeDetails(placename):
	if request.method == "GET":
		basic_details = DBSearch.getDetails(placename)
		google_details = GoogleRequests.getDetailsFromGoogle(placename, basic_details['type'], basic_details['location'])
		pros_wordcloud = generate(basic_details['comments']['pros'])
		cons_wordcloud = generate(basic_details['comments']['cons'])
		return render_template("placedetails.html", placename=placename, details=basic_details, google_details=google_details, pwcd=pros_wordcloud, cwcd=cons_wordcloud)

@app.route("/login", methods=["GET", "POST"])
def login():
	if 'email' in session:
		return redirect(url_for('index', name=session.get('name')))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data 

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				session['name'] = user.first_name
				session['user_id'] = user.user_id
				return redirect(url_for('index', name=session.get('name')))
			else:
				return redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('login.html', form=form)
 
@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('index', name=session.get('name')))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.email.data, form.username.data, form.password.data, datetime.datetime.now(), datetime.datetime.now(), form.first_name.data, form.last_name.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      session['name'] = newuser.first_name
      return redirect(url_for('index', name=session.get('name')))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/leaveReview", methods=["GET", "POST"])
def leaveReview():

	search_form = SearchForm()
	local_places = DBSearch.placesNearMe()

	if request.method == "GET":
		return render_template("leavereview.html", search_form=search_form, local_places=local_places)
	else:
		search_term = request.form['search']
		return findPlaces(search_term)

@app.route("/suggestNewPlace", methods=["POST"])
def suggestANewPlace():
	data = request.form
	if Review.suggest(data) == "Place Added":
		return redirect(url_for('index', name=session.get('name')))
	else: return render_template("placenotfound.html")	

@app.route("/reviewNewPlace", methods=["POST"])
def reviewANewPlace():
	if session.get('user_id'):
		rater = session.get('user_id')
	else: rater = 0
	Review.new(request.form, rater)
	return redirect(url_for('index', name=session.get('name')))


@app.route("/logout")
def logout():
  session.pop('email', None)
  session.pop('user_id', None)
  session.pop('name', None)
  return redirect(url_for('index'))