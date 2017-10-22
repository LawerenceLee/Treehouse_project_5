from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, ValidationError


def date_format(form, field):
    '''Acts as a validator for the date field in the
    AddEditForm Class'''
    try:
        datetime.strptime(field.data, '%m/%d/%Y')
    except ValueError:
        raise ValidationError('Date format is NOT correct.')


def num_checker(form, field):
    '''Acts as a validator for the time_spent field in the
    AddEditForm Class'''
    try:
        float(field.data)
    except ValueError:
        raise ValidationError('This field must contain ONLY numbers.')


class AddEditEntryForm(FlaskForm):
    title = StringField(
        'Entry Title:',
        validators=[
            DataRequired()
        ])
    date = StringField(
        'Date (MM/DD/YYYY):',
        validators=[
            DataRequired(),
            date_format,
        ])
    time_spent = StringField(
        'Time Spent (MINS):',
        validators=[
            DataRequired(),
            num_checker
        ])
    learned = TextAreaField(
        "What I Learned:",
        validators=[
            DataRequired()
        ])
    resources = TextAreaField(
        "Resources to Remember:",
        validators=[
            DataRequired()
        ])
    tags = StringField(
        "Tags (seperate each with a comma):"
        )


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
            ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
            ])
