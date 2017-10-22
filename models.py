from peewee import *

DATABASE = SqliteDatabase('entries.db', threadlocals=True)


class Entry(Model):
    title = CharField(max_length=100)
    date = CharField(max_length=10)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()
    slug = CharField(max_length=100)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
