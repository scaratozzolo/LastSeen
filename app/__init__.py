from flask import Flask, render_template, flash, redirect, url_for, request
import sqlite3
from os import listdir
from os.path import isfile, join
import random
import datetime

lastseen = datetime.datetime.now()
kills = 0


app = Flask(__name__)


conn = sqlite3.connect("cat.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS lastseen (timestamp TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS kills (timestamp TEXT, count TEXT)")
lastquery = c.execute("SELECT * FROM lastseen ORDER BY timestamp DESC LIMIT 1").fetchone()
if lastquery is not None:
    lastseen = datetime.datetime.fromtimestamp(int(lastquery[0]))

killsquery = c.execute("SELECT * FROM kills ORDER BY count DESC LIMIT 1").fetchone()
if killsquery is not None:
    kills = int(killsquery[1])

conn.commit()
conn.close()

mypath = "app/static/imgs/Cat"
catpics = [f for f in listdir(mypath) if isfile(join(mypath, f))]


@app.route("/")
@app.route("/index")
def index():
    randimg = random.choice(catpics)
    return render_template("index.html", time=lastseen.strftime("%I:%M %p"), date=lastseen.strftime("%m/%d"), kills=kills, catimg=url_for('static', filename="imgs/Cat/" + randimg))


@app.route("/newseen", methods=["POST"])
def newseen():

    with sqlite3.connect("cat.db") as conn:

        c = conn.cursor()
        nowstamp = int(datetime.datetime.now().timestamp())
        c.execute("INSERT INTO lastseen (timestamp) VALUES (?)", (nowstamp,))
        conn.commit()

    return redirect(url_for("index"))


@app.route("/newkill", methods=["POST"])
def newkill():
    global kills

    with sqlite3.connect("cat.db") as conn:

        c = conn.cursor()
        nowstamp = int(datetime.datetime.now().timestamp())
        kills += 1
        c.execute("INSERT INTO kills (timestamp, count) VALUES (?, ?)", (nowstamp, kills, ))
        conn.commit()

    return redirect(url_for("index"))
