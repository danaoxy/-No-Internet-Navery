import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/home/<string:cat>')
def home(cat):
    userData = request.form.get('userData')
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
    return render_template('home.html', lst=lst, userData=userData)

def regexp(expr, item):
    pattern = re.compile(expr)
    return pattern.search(item) is not None

@app.route('/search', methods=['POST'])
def search():
    # This does not work
    if request.method == 'POST':
        search = request.form.get("filter")
        db = sqlite3.connect('itinerary.db')
        db.create_function("REGEXP", 2, regexp)
        comm = "SELECT Places.PlaceIndex, Places.PlaceName FROM Places WHERE Places.PlaceName REGEXP '{}' ORDER BY Places.Hit DESC".format(search)
        lst = []
        cursor = db.execute(comm)
        data = cursor.fetchall()
        for record in data:
            lst.append(record)
        return render_template('home_result.html', lst=lst)
    
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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # add user information into data base
    msg = ""
    if request.method == 'GET':
        return render_template("signup.html", msg=msg)
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('password').encode()).hexdigest()
        db = sqlite3.connect('itinerary.db')
        comm = "SELECT User.UserName FROM User WHERE User.UserEmail = '{}'".format(email)
        cursor = db.execute(comm)
        data = cursor.fetchone()
        if name == "" or email == "" or password == "":
            msg = "empty field. fill them in"
            return render_template("signup.html", msg=msg)
        elif data is None:
            comm2 = "INSERT INTO User(UserName, UserEmail, UserPP) VALUES ('{}', '{}', '{}')".format(name, email, password)
            db.execute(comm2)
            db.commit()
            db.close()
            return redirect(url_for('home', cat="main"))
        else:
            msg = "email has already been used"
            return render_template("signup.html", msg=msg)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('password').encode()).hexdigest()
        db = sqlite3.connect("itinerary.db")
        comm = "SELECT User.UserIndex, User.UserName FROM User WHERE User.UserEmail = '{}' AND User.UserPP = '{}'".format(email, password)
        cursor = db.execute(comm)
        userData = cursor.fetchone()
        if userData is not None:
            #return render_template("test.html", data=data)
            return redirect(url_for('home', cat="main", userData=userData))
        else:
            return render_template("login.html")
        
@app.route('/itinerary')
def itinerary():
    return render_template('itinerary.html')

if __name__ == "__main__":
    app.run(debug=True)