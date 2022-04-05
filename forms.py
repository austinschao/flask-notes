from wsgiref import validate

from flask_wtf import FlaskForm

from wtforms import StringField, EmailField, PasswordField, TextAreaField

from wtforms.validators import InputRequired, Email, Length, DataRequired, email_validator



class RegisterForm(FlaskForm):
    """ Create a form for registering new users """

    username = StringField('Username', validators=[DataRequired(), Length(max=20)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])

    email = EmailField('Email', validators=[InputRequired(), Email()])

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])

    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """ Create a form for logging in existing users """

    username = StringField('Username', validators=[DataRequired(), Length(max=20)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])


class CSRFProtection(FlaskForm):
    """ Form for CSRF Protection"""


class AddNote(FlaskForm):
    """ Form for adding a note """

    title = StringField('Title', validators=[DataRequired(), Length(max=100)])

    content = TextAreaField('Content', validators=[DataRequired()])


class EditNote(FlaskForm):
    """ Form for editing a note """

    title = StringField('Title', validators=[DataRequired(), Length(max=100)])

    content = TextAreaField('Content', validators=[DataRequired()])

