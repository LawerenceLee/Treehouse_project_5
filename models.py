from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('entries.db', threadlocals=True)


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    title = CharField(max_length=100)
    date = CharField(max_length=10)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()
    slug = CharField(max_length=100)
    tags = CharField(max_length=200)

    class Meta:
        database = DATABASE


def initialize():
    '''Open database, create tables if they are not already
    there, close database'''
    DATABASE.connect()
    DATABASE.create_tables([Entry, User], safe=True)
    DATABASE.close()
