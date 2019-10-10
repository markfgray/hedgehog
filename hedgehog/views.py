from hedgehog import app, db
from flask import render_template, request, url_for, redirect, session
import datetime
from .forms import SearchForm, LoginForm, SignupForm, ReviewForm
from .search import query
from .review import placesNearMe
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
	results = query(search_term)
	return render_template('results.html', results=results, search_term=search_term)

@app.route('/localplaces', methods=["GET", "POST"])
def localPlaces():
	if request.method == "GET":
		results = placesNearMe()
		return render_template('localplaces.html', results=results)
	else:
		return render_template('leavereview.html')

@app.route('/placedetails/<placename>', methods=["GET", "POST"])
def placeDetails(placename):
	return render_template('placedetails.html', placename=placename)
	

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

	form = ReviewForm()
	search_form = SearchForm()
	local_places = placesNearMe()

	if request.method == "GET":
		return render_template("leavereview.html", form=form, search_form=search_form, local_places=local_places)
	else:
		if session.get('user_id'):
			rater = session.get('user_id')
		else: rater = "guest"
		rating = int(form.rating.data[0])
		date = datetime.date.today()
		name = form.place.data
		if Place.query.filter_by(name=name).first() != None:
			establishment = Place.query.filter_by(name=name).first()
			eid = establishment.eid
		else:
			newPlace = Place("Pub", name, 0.1, 0.2, "Real Ale")
			db.session.add(newPlace)
			db.session.commit()
			establishment = Place.query.filter_by(name=name).first()
			eid = establishment.eid
		print("eid =", eid)
		new_rating = Rating(date, rater, name, rating, form.best_bits.data, form.worst_bits.data, eid)
		db.session.add(new_rating)
		db.session.commit()
		return redirect(url_for('index', name=session.get('name')))

@app.route("/logout")
def logout():
  session.pop('email', None)
  session.pop('name', None)
  return redirect(url_for('index'))