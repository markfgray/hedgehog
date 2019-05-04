from hedgehog import app
from flask import render_template
from .forms import SignupForm

@app.route('/')
def index():
	form = SignupForm()
	print("well that worked")
	return render_template('index.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
	print("signup complete")
	return("Thanks for signing up!")