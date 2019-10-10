from hedgehog import app, db
from flask import render_template, request, url_for, redirect, session
import datetime
from .forms import SearchForm, LoginForm, SignupForm, ReviewForm
from .review import placesNearMe
from .search import getDetails
from .models import User, Rating, Place

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
	a = '%'+search_term+'%'
	r = Place.query.filter(Place.name.like(a)).all()
	results = []
	for place in r:
		results.append({'name': place.name, 'location': place.location})
	return render_template('results.html', results=results, search_term=search_term, form=form)

@app.route('/findPlaces', methods=["GET"])
def findPlaces(search_term):
	form = ReviewForm()
	a = '%'+search_term+'%'
	r = Place.query.filter(Place.name.like(a)).all()
	results = []
	for place in r:
		results.append({'name': place.name, 'location': place.location})
	return render_template('placestoreview.html', results=results, search_term=search_term, form=form)


@app.route('/reviewpage/<placename>', methods=["GET", "POST"])
def postReview(placename):
	if request.method == "GET":
		form = ReviewForm()
		return render_template('reviewpage.html', placename=placename, form=form)
	else:
		formatted_name = placename[1:-1]
		establishment = Place.query.filter_by(name=formatted_name).first()
		form = request.form
		date = datetime.date.today()
		if session.get('user_id'):
			rater = session.get('user_id')
		else: rater = 0
		name = formatted_name
		best_bits = form['best_bits']	
		worst_bits = form['worst_bits']
		rating = int(form['rating'])
		eid = establishment.eid
		new_rating = Rating(date, rater, name, rating, best_bits, worst_bits, eid)
		db.session.add(new_rating)
		db.session.commit()
		return redirect(url_for('index', name=session.get('name')))

@app.route('/details/<placename>', methods=["GET","POST"])
def placeDetails(placename):
	if request.method == "GET":
		details = getDetails(placename)
		return render_template("placedetails.html", placename=placename, details=details)

	

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
	local_places = placesNearMe()

	if request.method == "GET":
		return render_template("leavereview.html", search_form=search_form, local_places=local_places)
	else:
		search_term = request.form['search']
		return findPlaces(search_term)

@app.route("/logout")
def logout():
  session.pop('email', None)
  session.pop('user_id', None)
  session.pop('name', None)
  return redirect(url_for('index'))