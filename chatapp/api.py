from crypt import methods
import json, time
from chatapp import app, db
from chatapp.models import User, Message
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/api/send/", methods=["POST"])
def send_message():

    if not current_user.is_authenticated: return "ERROR"
    
    body = json.loads(request.data.decode())
    send_time = time.time()

    print(body)

    message = Message(
        msg_from = current_user.id,
        msg_to = body["to"],
        content = body["content"],
        time = send_time,
    )
    
    db.session.add(message)
    db.session.commit()

    return "Success"