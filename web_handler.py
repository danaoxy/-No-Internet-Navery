import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home', cat="main"))


@app.route('/home/<string:cat>')
def home(cat):
    db = sqlite3.connect('itinerary.db')
    if cat == "main":
        comm = "SELECT Places.PlaceIndex, Places.PlaceName, Places.PlaceImg FROM Places ORDER BY Places.Hit DESC"
    else:
        comm = "SELECT Places.PlaceIndex, Places.PlaceName, Places.PlaceImg FROM Places WHERE Places.Categories = '{}' ORDER BY Places.Hit DESC".format(cat)
    lst = []
    cursor = db.execute(comm)
    data = cursor.fetchall()
    for record in data:
        lst.append(record)
    return render_template('home.html', lst=lst)

@app.route('/search')
    
@app.route('/display/<int:index>')
def display(index):
    db = sqlite3.connect('itinerary.db')
    comm = "SELECT * FROM Places WHERE Places.PlaceIndex = {}".format(index)
    cursor = db.execute(comm)
    data = cursor.fetchone()
    newHit = data[7] + 1
    comm= "UPDATE Places SET Hit = {} WHERE PlaceIndex = {}".format(newHit, index)
    cursor = db.execute(comm)
    db.commit()
    db.close()

    return render_template('display.html', data=data)


@app.route('/signup')
def signup():
    # add user information into data base
    db = sqlite3.connect("database.db")
    comm = "INSERT INTO 'table' VALUES ()".format()
    return render_template("signup.html")

@app.route('/login')
def login():
        #if user information does not exist in database, 
        #if user info exist in database, log them in 
        #db = sqlite3.connect("database.db")
        
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)