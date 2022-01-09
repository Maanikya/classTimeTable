from flask import Flask, redirect, render_template, url_for, request, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user ,logout_user, login_manager, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# My Database Connection
local_server=True
# app=Flask(__name__, static_url_path='/assets' , static_folder='assets')
app=Flask(__name__)
app.secret_key="classtimetable"

# This is for getting the Unique User Access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databaseName'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/classtimetable'
db=SQLAlchemy(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="classtimetable"
)
 
timetable = mydb.cursor()
 
timetable.execute("SELECT * FROM timetable")
 
myresult = timetable.fetchall()
 
for x in myresult:
    print(x)

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(user_id)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class Student(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True)
    password=db.Column(db.String(1000))

@app.route("/")
def home():
    return render_template("index.html")

# Testing whether DB is connected or not
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return 'MY DATABASE IS CONNECTED'
    
    except Exception as e:
        print(e)
        return f'MT DATABASE IS NOT CONNECTED. Exception: {e}'


@app.route("/registerPage", methods=['POST', 'GET'])
def registerPage():
    return render_template("register.html")

# Student Register Route
@app.route("/stuRegister", methods=['POST', 'GET'])
def stuRegister():
    if request.method=="POST":
        id=request.form.get('usn')
        password=request.form.get('password')
        encPassword = generate_password_hash(password)
        user=Student.query.filter_by(id=id).first()
        if user:
            flash("Student Already Registered")
            return render_template("register.html")
        new_user = db.engine.execute(f"INSERT INTO `student` (`id`, `password`) VALUES ('{id}','{encPassword}')")
        return render_template("index.html")

# Student Login Route
@app.route("/stuLogin", methods=['POST', 'GET'])
def stuLogin():
    if request.method=="POST":
        usn=request.form.get('usn')
        password=request.form.get('password')
        user=Student.query.filter_by(id=usn).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            for x in myresult:
                flash(x)
            return render_template("/stuDashboard.html")
        else:
            flash('Invalid Credentials. Please Try Again.')
            return render_template("index.html")

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route('/tt')
# def tt():

app.run(debug=True)