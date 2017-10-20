from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


def date_format(form, field):
    try:
        datetime.strptime(field.data, '%m/%d/%Y')
    except ValueError:
        raise ValidationError('Date format is NOT correct.')


def num_checker(form, field):
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
