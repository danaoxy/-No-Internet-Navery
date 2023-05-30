import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    # go straight to the login page
    return redirect(url_for("login"))


@app.route('/home/<string:cat>')
def home(cat):
    userData = request.form.get('userData')

    # connecting to the database
    db = sqlite3.connect('itinerary.db')

    # command for filtering the attractions via category
    if cat == "main":
        comm = "SELECT Places.PlaceIndex, Places.PlaceName, Places.PlaceImg FROM Places ORDER BY Places.Hit DESC"
    else:
        comm = "SELECT Places.PlaceIndex, Places.PlaceName, Places.PlaceImg FROM Places WHERE Places.Categories = '{}' ORDER BY Places.Hit DESC".format(cat)
    lst = []
    cursor = db.execute(comm)
    data = cursor.fetchall()

    # putting the data into a readable format by jinja
    for record in data:
        lst.append(record)
    return render_template('home.html', lst=lst, userData=userData)

# supposed to be a user-defined sql function for using regex since regexp does not work in python
# It does not work
def regexp(expr, item):
    pattern = re.compile(expr)
    return pattern.search(item) is not None

@app.route('/search', methods=['POST'])
def search():
    # The function is to use regex to get the search results
    # However, since the user-defined function does not work, the search bar is decorative with no functions
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
    # This is to display more information about a particular destination
    # Due to time contraints, the webpage is a basic skeleton of the most bare minimum of information
    db = sqlite3.connect('itinerary.db')

    #It uses the index of the record to find all information about a particular destination
    comm = "SELECT * FROM Places WHERE Places.PlaceIndex = {}".format(index)
    cursor = db.execute(comm)
    data = cursor.fetchone()

    # Whenever a display of a particular destination is accessed, the hit counter is incremented
    # This is to ensure the destination with the most hit AKA the most popular will appear first on the homepage
    newHit = data[7] + 1
    comm= "UPDATE Places SET Hit = {} WHERE PlaceIndex = {}".format(newHit, index)
    cursor = db.execute(comm)
    db.commit()
    db.close()

    return render_template('display.html', data=data)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # add user information into database
    msg = ""
    if request.method == 'GET':
        return render_template("signup.html", msg=msg)
    elif request.method == 'POST':
        # get information inputted by the user
        name = request.form.get('name')
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('password').encode()).hexdigest()
        # the password has md5 hash encrytion on it to prevent the password from being stored as plaintext

        db = sqlite3.connect('itinerary.db')

        # This is to check whether a record of the email is already used by an existing user
        comm = "SELECT User.UserName FROM User WHERE User.UserEmail = '{}'".format(email)
        cursor = db.execute(comm)
        data = cursor.fetchone()

        # If any of the fields are empty, put out a warning and bring them back to the same page
        if name == "" or email == "" or password == "":
            msg = "empty field. fill them in"
            return render_template("signup.html", msg=msg)
        
        # If there are no records of the email in the database, insert the info of new user in the database
        elif data is None:
            comm2 = "INSERT INTO User(UserName, UserEmail, UserPP) VALUES ('{}', '{}', '{}')".format(name, email, password)
            db.execute(comm2)
            db.commit()
            db.close()
            return redirect(url_for('home', cat="main"))
        
        # If a record exists, put out a warning
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

        # This is to check whether user exists by the input email
        comm = "SELECT User.UserIndex, User.UserName FROM User WHERE User.UserEmail = '{}' AND User.UserPP = '{}'".format(email, password)
        cursor = db.execute(comm)
        userData = cursor.fetchone()

        # If a record exists, redirect them to the homepage
        if userData is not None:
            #return render_template("test.html", data=data)
            return redirect(url_for('home', cat="main", userData=userData))
        else:
            return render_template("login.html")
        
@app.route('/itinerary')
def itinerary():
    # supposed to have the function to create an itinerary
    # due to time contraints and lack of ability and sleep, this remains uncomplete.
    return render_template('itinerary.html')

if __name__ == "__main__":
    app.run(debug=True)