import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    #if not log in, redirect to signup page
    #if logged in, display homepage and recommended stuff and other shenanigans
    return render_template("home.html")

@app.route('/signup')
def signup():
    # add user information into data base
    db = sqlite3.connect("database.db")
    comm = "INSERT INTO 'table' VALUES ()".format()
    return render_template("signup.html")

@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        #if user information does not exist in database, 
        #if user info exist in database, log them in 
        db = sqlite3.connect("database.db")
        
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)