from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user , logout_user, login_manager, LoginManager, current_user
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
 
# for x in myresult:
    # timetable.execute("SELECT P1 FROM timetable where day=")
    # myresult=timetable.fetchall()
    #print(myresult)
    # print(x[3])

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return teacher.query.get(user_id)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class Student(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True)
    password=db.Column(db.String(1000))

class teacher(UserMixin, db.Model):
    id=db.Column(db.String, primary_key=True, unique=True)
    password=db.Column(db.String(1000))

@app.route("/")
def home():
    return render_template("index.html")

# Testing whether DB is connected or not
@app.route("/test")
def test():
    timetable = mydb.cursor()
    timetable.execute("SELECT * FROM timetable") 
    myresult = timetable.fetchall()
    flash(myresult)
    return render_template("test.html")

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
            flash("Student Already Registered", 'student')
            return render_template("register.html")
        new_user = db.engine.execute(f"INSERT INTO `student` (`id`, `password`) VALUES ('{id}','{encPassword}')")
        return render_template("index.html")

# Teacher Register Route
@app.route("/teaRegister", methods=['POST', 'GET'])
def teaRegister():
    if request.method=="POST":
        id=request.form.get('tid')
        password=request.form.get('password')
        encPassword = generate_password_hash(password)
        user=teacher.query.filter_by(id=id).first()
        if user:
            flash("Teacher Already Registered", 'teacher')
            return render_template("register.html")
        new_user = db.engine.execute(f"INSERT INTO `teacher` (`id`, `password`) VALUES ('{id}','{encPassword}')")
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
            timetable = mydb.cursor()
            timetable.execute("SELECT * FROM timetable") 
            myresult = timetable.fetchall()
            flash(myresult, 'tt')
            subdetails = mydb.cursor()
            subdetails.execute("SELECT * FROM subject")
            subresult = subdetails.fetchall()
            flash(subresult, 'subject')
            return render_template("/stuDashboard.html")
        else:
            flash('Invalid Credentials. Please Try Again.', 'student')
            return render_template("index.html")

# Teacher Login Route
@app.route("/teaLogin", methods=['POST', 'GET'])
def teaLogin():
    if request.method=="POST":
        id=request.form.get('tid')
        password=request.form.get('password')
        user=teacher.query.filter_by(id=id).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            timetable = mydb.cursor()
            timetable.execute("SELECT * FROM timetable") 
            myresult = timetable.fetchall()
            flash(myresult, 'tt')
            subdetails = mydb.cursor()
            subdetails.execute("SELECT * FROM subject")
            subresult = subdetails.fetchall()
            flash(subresult, 'subject')
            return render_template("/teaDashboard.html")
        else:
            flash('Invalid Credentials. Please Try Again.', 'teacher')
            return render_template("index.html")

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

app.run(debug=True)