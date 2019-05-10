from hedgehog import app, db
from flask import render_template, request, url_for, redirect
from .forms import SearchForm
from .search import query

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

@app.route('/leavereview', methods=["GET", "POST"])
def leaveReview():
	return render_template('leavereview.html')

@app.route('/localplaces', methods=["GET", "POST"])
def localPlaces():
	return render_template('localplaces.html')

@app.route('/placedetails', methods=["GET", "POST"])
def placeDetails():
	return render_template('placedetails.html')
	

@app.route('/login', methods=["GET", "POST"])
def login():
	return render_template('login.html')