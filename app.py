import re

from flask import (Flask, render_template, url_for, g,
                   flash, redirect)


import forms
import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = 'jri,74gdk20jsynGRYm387*(^$&jfhbfd6GR$fv$%YGR^*HD33RGe4fR'


def slugify(string):
    string = re.sub(r'[_.\s]', '-', string).lower()
    string = re.sub(r'\\', '', string)
    return re.sub('[?#$%^&!@*]', '', string)


@app.before_request
def before_request():
    g.db = models.DATABASE
    try:
        g.db.connect()
    except models.OperationalError:
        pass


@app.after_request
def after_request(response):
    g.db.close()
    return response


# Needs two routes
@app.route('/entry', methods=['GET', 'POST'])
@app.route('/entries/edit/<slug>', methods=['GET', 'POST'])
def add_edit(slug=None):
    if slug:
        entry = models.Entry.get(models.Entry.slug == slug)
        form = forms.AddEditEntryForm()
        if form.validate_on_submit():
            models.Entry.update(
                title=form.title.data.strip(),
                date=form.date.data.strip(),
                time_spent=form.time_spent.data.strip(),
                learned=form.learned.data.strip(),
                resources=form.resources.data.strip(),
                slug=slugify(form.title.data.strip())
                ).where(models.Entry.slug == slug
                        ).execute()
            flash("Entry Updated!", 'success')
            return redirect(url_for('index'))
        form.title.data = entry.title
        form.date.data = entry.date
        form.time_spent.data = entry.time_spent
        form.learned.data = entry.learned
        form.resources.data = entry.resources
        return render_template('edit.html', form=form)
    else:
        form = forms.AddEditEntryForm()
        if form.validate_on_submit():
            models.Entry.create(
                title=form.title.data.strip(),
                date=form.date.data.strip(),
                time_spent=form.time_spent.data,
                learned=form.learned.data.strip(),
                resources=form.resources.data.strip(),
                slug=slugify(form.title.data.strip()))
            flash("Entry Added!", 'success')
            return redirect(url_for('index'))
        return render_template('new.html', form=form)


@app.route('/entries/<slug>')
def detail(slug=None):
    entry = models.Entry.get(models.Entry.slug == slug)
    return render_template('detail.html', entry=entry)


@app.route('/entries/delete/<slug>')
def delete(slug=None):
    models.Entry.get(models.Entry.slug == slug).delete_instance()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
