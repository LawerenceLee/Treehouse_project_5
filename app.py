from flask import (Flask, render_template, url_for, g,
                   flash, redirect)


import forms
import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = 'jri,74gdk20jsynGRYm387*(^$&jfhbfd6GR$fv$%YGR^*HD33RGe4fR'


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
def add_edit():
    form = forms.AddEntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data.strip(),
            date=form.date.data.strip(),
            time_spent=form.time_spent.data,
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip())
        flash("Entry Added!", 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/')
@app.route('/entries')
@app.route('/entries/<entry_id>')
@app.route('/entries/edit/<edit_id>', methods=['GET', 'POST'])
def index(entry_id=None, edit_id=None):
    if edit_id:
        entry = models.Entry.get(models.Entry.id == edit_id)
        return render_template('edit.html', entry=entry)
    elif entry_id:
        entry = models.Entry.get(models.Entry.id == entry_id)
        return render_template('detail.html', entry=entry)
    else:
        entries = models.Entry.select().limit(100)
        return render_template('index.html', entries=entries)


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
