import os.path
import sqlite3
from bottle import request, route, run, template, redirect, static_file
import airportsdata
import pandas as pd
from createMap import *


DATABASE = './mydata/logbook.db'
CREATE_SCRIPT = './mydata/createdb.sql'

def connectDB():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def initDB():
    with sqlite3.connect(DATABASE) as conn:
        with open(CREATE_SCRIPT,'r') as f:
            conn.executescript(f.read())
        if not os.path.exists(DATABASE):
            print("DB INIT>")
        else:
            print("DB EXISTS")

@route("/")
def index():
    return template('./pages/map.html')
@route("/addairport")
def add_airport_form():
    return static_file("/airports/new.html", root='./pages')
@route("/addairport",method="POST")
def add_airports():
    airports = airportsdata.load('ICAO')
    new_airport = request.forms.get('ICAO')
    if new_airport in airports:
        details = airports[new_airport]
        name = details['name']
        city = details['city']
        subd = details['subd']
        country = details['country']
        elv = details['elevation']
        lat = details['lat']
        lon = details['lon']
        print("WELCOME :")
        print(f"AIRPORT : {name}")
        print(f"{city} , {subd}")
        print(f"{country}")
        print(f"{elv} FEET MSL")
        print(f"{lat} , {lon}")
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO airports (icao, name, city, subd, country, elv,lat,lon) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (new_airport,name,city,subd,country,elv,lat,lon))
        conn.commit()
        cursor.close()
        createMap()
    redirect('/')
if __name__ == '__main__':
    initDB()
    createMap()
    run(host="0.0.0.0",
        port="8888",
        debug=True,
        reloader=True
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
