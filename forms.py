from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


def date_format():
    pass


class AddEntryForm(FlaskForm):
    title = StringField(
        'Entry Title:',
        validators=[
            DataRequired()
        ])
    date = StringField(
        'Date (MM/DD/YYYY):',
        validators=[
            DataRequired(),
            # date_format
        ])
    time_spent = StringField(
        'Time Spent (MINS):',
        validators=[
            DataRequired()
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
