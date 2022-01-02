from flask import Flask, redirect, render_template, url_for

# My Database Connection

local_server=True
#app=Flask(__name__, template_folder='../frontend', static_url_path='/assets' , static_folder='assets')
#app=Flask(__name__, template_folder='../backend/assets', static_url_path='/assets' , static_folder='assets')
#app=Flask(__name__, static_url_path='/assets' , static_folder='assets')
app=Flask(__name__)
app.secret_key="classtimetable"

@app.route("/")
def home():
    return render_template("index.html")


app.run(debug=True)
