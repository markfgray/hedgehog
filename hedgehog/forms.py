from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
	submit = SubmitField('Submit')

class SearchForm(Form):
	search = StringField('')
	submit = SubmitField('Search')

class LoginForm(Form):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  submit = SubmitField("Sign in")

class SignupForm(Form):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  username = StringField('Username', validators=[DataRequired("Choose a Username")])  
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')

class ReviewForm(Form):
	place = StringField('Place Name', validators=[DataRequired("Please enter the name of the place you would like to review")])
	location = StringField('Place location', validators=[DataRequired("Please enter the location of this place")])
	rating = SelectMultipleField('Rating', choices=[('1', 'Awful'), ('2', 'Bad'), ('3', 'OK'), ('4', 'Good'), ('5', 'Amazing')])
	best_bits = TextAreaField('What did you like', validators=[Length(max=160)])
	worst_bits = TextAreaField('What did you not like', validators=[Length(max=160)])
	submit = SubmitField('Submit')