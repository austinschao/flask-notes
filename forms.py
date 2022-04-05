from wsgiref import validate

from flask_wtf import FlaskForm

from wtforms import StringField, EmailField, PasswordField

from wtforms.validators import InputRequired, Email, Length, DataRequired, email_validator



class RegisterForm(FlaskForm):
    """ Create a form for registering new users """

    username = StringField('Username', validators=[DataRequired(), Length(max=20)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])

    email = EmailField('Email', validators=[InputRequired(), Email()])

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])

    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
