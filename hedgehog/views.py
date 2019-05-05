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
	email = request.form['email']
	try:
		interested_user = RegisterInterest(email=email)
		db.session.add(interested_user)
		db.session.commit()
		#return "Thanks for singing up. We'll send you an email at {} when we're up and running".format(interested_user.email)
		return redirect(url_for('thanks', email=email))
	except Exception as e:
	    return(str(e))

@app.route('/thanks/<email>', methods=["GET"])
def thanks(email):
	return render_template('thankyou.html', email=email)