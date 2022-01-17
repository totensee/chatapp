from chatapp import app, db
from chatapp.models import User
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/api/send/<channel>", methods=["POST"])
def send_message(channel):
    print(request.data)
    return "Success"