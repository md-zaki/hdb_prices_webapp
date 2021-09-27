from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    ##email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class resalepriceinputform(FlaskForm):
    town = StringField('Select Town Name')
    flatType = SelectField(u'Select Flat type', choices=[('2 Room', '2 Room'), ('3 Room', '3 Room'), ('4 Room', '4 Room'),('5 Room', '5 Room'),('Executive', 'Executive')])
    ogprice = IntegerField('Enter Original Price')
    floorArea = IntegerField('Enter Floor Area (in sqm)')
    storey = SelectField(u'Select Preferred Storey', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    age = SelectField(u'Select Preferred Age', choices=[('New', 'New'), ('Medium', 'Medium'), ('Old', 'Old')])
    submit = SubmitField('Submit')
