from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

# My Database Connection

local_server=True
#app=Flask(__name__, template_folder='../backend/assets', static_url_path='/assets' , static_folder='assets')
#app=Flask(__name__, static_url_path='/assets' , static_folder='assets')
app=Flask(__name__)
app.secret_key="classtimetable"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databaseName'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/classtimetable'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

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

app.run(debug=True)
