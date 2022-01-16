from chatapp import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def default():
    return redirect(url_for("message_page"))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/messages")
@login_required
def message_page():
    return render_template("messages.html")