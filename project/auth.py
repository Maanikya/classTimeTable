from flask import Flask, Blueprint, redirect, render_template, url_for, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user ,logout_user, login_manager, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/stuLogin", methods=['POST'])
def stuLogin():
    usn=request.form.get('usn')
    password=request.form.get('password')
    print(usn, password)
    #return render_template('index.html')
    new_user = db.engine.execute(f"INSERT INTO `student` (`usn`, `password`) VALUES ('{usn}','{password}')")
    return render_template("stuDashboard.html")