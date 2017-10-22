import re

from flask import (Flask, render_template, url_for, g,
                   flash, redirect)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required)

import forms
import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = 'jri,74gdk20jsynGRYm387*(^$&jfhbfd6GR$fv$%YGR^*HD33RGe4fR'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    '''Loads a User from the Database'''
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


def slugify(string):
    '''Deletes special characters, and replaces spaces,
    periods, and underscores with dashes'''
    string = re.sub(r'[_.\s]', '-', string).lower()
    string = re.sub(r'\\', '', string)
    return re.sub('[?#$%^&!@*]', '', string)


@app.before_request
def before_request():
    '''Database is opened prior to request'''
    g.db = models.DATABASE
    try:
        g.db.connect()
    except models.OperationalError:
        pass


@app.after_request
def after_request(response):
    '''Database is closed after the request'''
    g.db.close()
    return response


@app.route('/entry', methods=['GET', 'POST'])
@app.route('/entries/delete/<slug>')
@login_required
def add_delete(slug=None):
    '''Allows for the adding of new entries, and deleting of old entries.'''
    if slug:
        models.Entry.get(models.Entry.slug == slug).delete_instance()
        flash("Entry Deleted!", 'success')
        return redirect(url_for('index'))
    else:
        form = forms.AddEditEntryForm()
        if form.validate_on_submit():
            models.Entry.create(
                title=form.title.data.strip(),
                date=form.date.data.strip(),
                time_spent=form.time_spent.data,
                learned=form.learned.data.strip(),
                resources=form.resources.data.strip(),
                slug=slugify(form.title.data.strip()),
                tags=form.tags.data.strip())
            flash("Entry Added!", 'success')
            return redirect(url_for('index'))
        return render_template('new.html', form=form)


@app.route('/entries/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit(slug=None):
    '''Allows the editing of entries'''
    entry = models.Entry.get(models.Entry.slug == slug)
    form = forms.AddEditEntryForm()
    if form.validate_on_submit():
        models.Entry.update(
            title=form.title.data.strip(),
            date=form.date.data.strip(),
            time_spent=form.time_spent.data.strip(),
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip(),
            slug=slugify(form.title.data.strip()),
            tags=form.tags.data.strip()
            ).where(models.Entry.slug == slug
                    ).execute()
        flash("Entry Updated!", 'success')
        return redirect(url_for('index'))
    form.title.data = entry.title
    form.date.data = entry.date
    form.time_spent.data = entry.time_spent
    form.learned.data = entry.learned
    form.resources.data = entry.resources
    form.tags.data = entry.tags
    return render_template('edit.html', form=form)


@app.route('/entries/<slug>')
def detail(slug=None):
    '''View shows the full details of a single entry'''
    entry = models.Entry.get(models.Entry.slug == slug)
    return render_template('detail.html', entry=entry)


@app.route('/login', methods=('GET', 'POST'))
def login():
    '''Allows an admin to login, add, edit and delete entries.'''
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    '''Logs out the admin'''
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
@app.route('/entries/tag/<tag>')
def index(tag=None):
    '''View shows a list of all entries, and will
    also show a list of all entries that share a tag.'''
    if tag:
        entries = models.Entry.raw(
            'SELECT * FROM Entry WHERE Entry.tags LIKE "%{}%"'.format(tag))
    else:
        entries = models.Entry.select(
            ).order_by(models.Entry.id.desc()).limit(100)
    return render_template('index.html', entries=entries)


if __name__ == "__main__":
    models.initialize()
    try:
        models.User.create_user(
            username='admin',
            password='password',
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
