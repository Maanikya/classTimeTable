from flask import Flask, redirect, render_template, url_for, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user ,logout_user, login_manager, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class Student(db.Model):
    usn=db.Column(db.Integer, primary_key=True)
    password=db.Column(db.String(20), unique=True)

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

# @app.route("/stuRegister", methods=['POST', 'GET'])
# def stuRegister():
#     usn=request.form.get('usn')
#     password=request.form.get('password')
#     print(usn, password)
#     #return render_template('index.html')
#     new_user = db.engine.execute(f"INSERT INTO `student` (`usn`, `password`) VALUES ('{usn}','{password}')")
#     return render_template("index.html")

@app.route("/stuRegister", methods=['POST', 'GET'])
def stuRegister():
    if request.method=="POST":
        usn=request.form.get('usn')
        password=request.form.get('password')
        print(usn, password)
        new_user = db.engine.execute(f"INSERT INTO `student` (`usn`, `password`) VALUES ('{usn}','{password}')")
        return render_template("index.html")

@app.route("/registerPage", methods=['POST', 'GET'])
def registerPage():
    return render_template("register.html")

app.run(debug=True)