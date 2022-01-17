from chatapp import app, db
from chatapp.models import User
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def default():
    print(current_user.is_authenticated)
    return redirect(url_for("message_page"))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    attempted_user = User.query.filter_by(username=username).first()
    if attempted_user and attempted_user.check_password_correction(attempted_password=password):
        login_user(attempted_user)
        flash(f"Successfully logged in as {attempted_user.username}", category="success")
        return redirect(url_for("message_page"))
    else:
        flash("Username and password dont match! Please try again")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    # Check if passwords match
    if not password1 == password2:
        flash("Passwords don't match")
        return redirect(url_for("register_page"))

    user_to_create = User(
        username = username,
        password = password1
    )

    db.session.add(user_to_create)
    db.session.commit()

    login_user(user_to_create)

    flash(f"Successfully created the user {user_to_create.username}")

    return redirect(url_for("message_page"))

@app.route("/logout")
def logout():
    logout_user()
    flash("Sucessfully loged out!")
    return redirect(url_for("login_page"))

@app.route("/messages")
@login_required
def message_page():
    return render_template("messages.html")