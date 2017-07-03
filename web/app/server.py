from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

golinks_json = 'golinks.json'
golinks_db = TinyDB(golinks_json)

########
# Routes
##########

@app.route('/')
@app.route('/index')
def index():
    return _index()

@app.route('/create')
def create():
    return render_template('create.html',
                           title='Create a new link',
                           shortcut=None,
                           redirect_url=None)

@app.route('/add', methods=['POST'])
def add():
    add_link(request.form['shortcut'], request.form['redirect'])
    return redirect(url_for('index'))

@app.route('/delete/<shortcut>/')
def delete(shortcut):
    delete_link(shortcut)
    return redirect(url_for('index'))

@app.route('/edit/<shortcut>/')
def edit(shortcut):
    link_query = Query()
    link = golinks_db.search(link_query.shortcut == shortcut)[0]
    return render_template('create.html',
                           title='Edit Link',
                           shortcut=link['shortcut'],
                           redirect_url=link['redirect'])

@app.route('/<path:path>')
def catch_all(path):
    link_query = Query()
    redirect_url = golinks_db.search(link_query.shortcut == path)

    if redirect_url:
        return redirect(redirect_url[0]['redirect'])

    return render_template('create.html',
                           title='Create a new link',
                           shortcut=path,
                           redirect_url=None)

###########
# Helpers
###########

def _index():
    links = golinks_db.all()
    return render_template('index.html',
                           title='Home',
                           links=links)

#########
# Storage
#########

def add_link(shortcut, redirect_url):
    link_query = Query()
    link = golinks_db.search(link_query.shortcut == shortcut)

    if link:
        golinks_db.update({'shortcut': shortcut, 'redirect': redirect_url},
                          link_query.shortcut == shortcut)
    else:
        golinks_db.insert({'shortcut': shortcut, 'redirect': redirect_url})

def delete_link(shortcut):
    link_query = Query()
    golinks_db.remove(link_query.shortcut == shortcut)
