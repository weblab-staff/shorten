from gevent.pywsgi import WSGIServer
from flask import Flask, redirect, abort, request, render_template
from flask_basicauth import BasicAuth
import sqlite3
import os

app = Flask(__name__)
# We're currently serving static files through Flask directly. This isn't great,
# and it'd be nice if we let nginx do it for us.
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = os.environ['PASSWORD']
basic_auth = BasicAuth(app)

# DB init
conn = sqlite3.connect('urls.db')
c = conn.cursor()
try:
    c.execute('SELECT * FROM urls')
except sqlite3.OperationalError as e:
    print('Creating new table')
    c.execute('CREATE TABLE urls(short TEXT UNIQUE, full TEXT)')
    conn.commit()
conn.close()

@app.route("/")
@basic_auth.required
def home():
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM urls")
        return render_template('index.html', urls=c.fetchall())

@app.route("/<short>")
def go(short):
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        c.execute("SELECT full FROM urls WHERE short=?", [short])
        full = c.fetchone()
        if full:
            return redirect(full[0])
    abort(404)

@app.route("/api/add", methods=['POST'])
@basic_auth.required
def add():
    full = request.form['full']
    short = request.form['short']
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO urls VALUES (?,?)", [short, full])
        conn.commit()

    return redirect("/")

# would ideally be POST/DELETE request, but using a simple href GET for simplicity
@app.route("/api/rm")
@basic_auth.required
def rm():
    short = request.args.get('url')
    with sqlite3.connect('urls.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM urls WHERE short=?", [short])
        conn.commit()

    return redirect("/")

default_port = 7000
http_server = WSGIServer(('', default_port), app)
http_server.serve_forever()
