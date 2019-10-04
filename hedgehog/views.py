from hedgehog import app, db
from flask import render_template, request, url_for, redirect, session
import datetime
from .forms import SearchForm, LoginForm, SignupForm
from .search import query
from .review import placesNearMe
from .models import User

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "GET":
		form = SearchForm()
		return render_template('index.html', form=form)
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
        session['name'] = user.firstname
        return redirect(url_for('search', name=session.get('name')))
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