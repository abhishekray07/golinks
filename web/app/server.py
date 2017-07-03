from flask import Flask, render_template, request, redirect, url_for
import pickle
import os

app = Flask(__name__)

########
# Routes
##########

@app.route('/')
@app.route('/index')
def index():
    return _index()

@app.route('/create')
def create():
    return _create()

@app.route('/add', methods=['POST'])
def add():
    add_link(request.form['shortcut'], request.form['redirect'])
    return redirect(url_for('index'))

@app.route('/<path:path>')
def catch_all(path):
    for link in links:
        if link['shortcut'] == path:
            return redirect(link['redirect'])

    return _create(shortcut=path)

###########
# Helpers
###########

def _index():
    return render_template('index.html',
                           title='Home',
                           links=links)

def _create(shortcut=None, redirect_url=None):
    return render_template('create.html',
                           title='Create a new link',
                           shortcut=shortcut,
                           redirect_url=redirect_url)

#########
# Storage
#########

LINKS_FILE = 'golinks'

def read_links():
    if not os.path.exists(LINKS_FILE):
        return []

    with open(LINKS_FILE, 'r') as f:
        return pickle.load(f)

links = read_links()

def write_links(links):
    with open(LINKS_FILE, 'a+') as f:
        pickle.dump(links, f)

def add_link(shortcut, redirect_url):
    global links
    links.append(
        {
            'shortcut': shortcut,
            'redirect': redirect_url
        }
    )
    write_links(links)
