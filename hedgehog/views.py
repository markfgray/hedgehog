from hedgehog import app, db
from flask import render_template, request, url_for, redirect
from .forms import SignupForm
from .models import RegisterInterest

@app.route('/')
def index():
	form = SignupForm()
	return render_template('index.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template('signup.html')
	else:
		email = request.form['email']
		try:
			interested_user = RegisterInterest(email=email)
			db.session.add(interested_user)
			db.session.commit()
			#return "Thanks for singing up. We'll send you an email at {} when we're up and running".format(interested_user.email)
			return redirect(url_for('thanks'))
		except Exception as e:
		    return(str(e))

@app.route('/thanks', methods=["GET"])
def thanks():
	return render_template('thankyou.html')

@app.route('/search', methods=["GET", "POST"])
def search():
	return render_template('search.html')

@app.route('/leavereview', methods=["GET", "POST"])
def leaveReview():
	return render_template('leavereview.html')

@app.route('/localplaces', methods=["GET", "POST"])
def localPlaces():
	return render_template('localplaces.html')

@app.route('/placedetails', methods=["GET", "POST"])
def placeDetails():
	return render_template('placedetails.html')

@app.route('/results', methods=["GET", "POST"])
def results():
	return render_template('results.html')
	

@app.route('/login', methods=["GET", "POST"])
def login():
	return render_template('login.html')