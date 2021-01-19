from flask_wtf import FlaskForm
from flaskblog import app,mongo,bcrypt
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = mongo.db.users
        existing_user = users.find_one({'name' : username.data})
        if existing_user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = mongo.db.users
        existing_user = users.find_one({'email' : email.data})
        if existing_user:
            raise ValidationError('That email is taken. Please choose a different one.')               


class Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class forgotPassword(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired(),Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change')

class addCity(FlaskForm):
    cityName = StringField('City Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    imageUrl = StringField('Image URL',
                           validators=[DataRequired(), Length(min=2, max=1000)])
    descript = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=2000)])
    ratings = StringField('Ratings',
                           validators=[DataRequired()])                      
    submit = SubmitField('Change')

    def validate_addCity(self, cityName):
        city = mongo.db.city
        existing_city = city.find_one({'name' : cityName.data})
        if existing_city:
            raise ValidationError('That cityName is taken. Please choose a different one.')
    
class updateCity(FlaskForm):
    cities = StringField('Select City',
                           validators=[DataRequired()])
    cityName = StringField('City Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    imageUrl = StringField('Image URL',
                           validators=[DataRequired(), Length(min=2, max=1000)])
    descript = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=2000)])
    ratings = StringField('Ratings',
                           validators=[DataRequired()])                      
    submit = SubmitField('Change')

    def validate_updateCity(self, cityName):
        city = mongo.db.city
        existing_city = city.find_one({'name' : cityName.data})
        if existing_city:
            raise ValidationError('That cityName is taken. Please choose a different one.')

class addPlace(FlaskForm):
    placeName = StringField('Place',
                           validators=[DataRequired(), Length(min=2, max=50)])
    imageUrl = StringField('Image URL',
                           validators=[DataRequired(), Length(min=2, max=1000)])
    descript = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=2000)])
    ratings = StringField('Ratings',
                           validators=[DataRequired()])                      
    submit = SubmitField('Add')

    def validate_getplaces(self,PlaceName):
        places = mongo.db.places
        existing_place = places.find_one({'name' : placeName.data})
        if existing_place:
            raise ValidationError('That placeName is taken. Please choose a different one.')

class updatePlace(FlaskForm):
    places = StringField('Select City',
                           validators=[DataRequired()])
    placeName = StringField('Place Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    imageUrl = StringField('Image URL',
                           validators=[DataRequired(), Length(min=2, max=1000)])
    descript = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=2000)])
    ratings = StringField('Ratings',
                           validators=[DataRequired()])                      
    submit = SubmitField('Change')

    def validate_updateCity(self, cityName):
        places = mongo.db.places
        existing_place = places.find_one({'name' : placeName.data})
        if existing_place:
            raise ValidationError('That placeName is taken. Please choose a different one.')