from gevent.pywsgi import WSGIServer
from flask import Flask, redirect, abort, request, render_template
import sqlite3
app = Flask(__name__)

# DB init
conn = sqlite3.connect('urls.db')
c = conn.cursor()
try:
	c.execute('SELECT * FROM urls')
except sqlite3.OperationalError as e:
	print('Creating new table')
	c.execute('CREATE TABLE urls(short TEXT, full TEXT)')
	conn.commit()
conn.close()

@app.route("/")
def hello():
	with sqlite3.connect('urls.db') as conn:
		c = conn.cursor()
		c.execute("SELECT * FROM urls")
		return render_template('index.html', urls=c.fetchall())

@app.route("/<short>")
def go(short):
	with sqlite3.connect('urls.db') as conn:
		c = conn.cursor()
		c.execute("SELECT full FROM urls WHERE short=?", [short])
		full = c.fetchone()[0]
		print(full)
		if full:
			return redirect(full)
	abort(404)

@app.route("/add", methods=['POST'])
def add():
	full = request.form['full']
	short = request.form['short']
	with sqlite3.connect('urls.db') as conn:
		c = conn.cursor()
		c.execute("INSERT into URLS values (?,?)", [short, full])
		conn.commit()

	return redirect("/")

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()
