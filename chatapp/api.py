import json, time
from chatapp import app, db
from chatapp.models import User, Message
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/api/send", methods=["POST"])
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

@app.route("/api/get", methods=["POST"])
def get_messages():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    current_id = current_user.id
    second_id = body["to"]

    messages_from = list(Message.query.filter_by(
        msg_from = current_id,
        msg_to = second_id,
    ))

    messages_to = list(Message.query.filter_by(
        msg_from = second_id,
        msg_to = current_id,
    ))

    all_messages = messages_from + messages_to

    all_messages.sort(key=lambda x: x.time)

    messages_json = []

    for message in all_messages:
        msg_json = {
            "content": message.content,
            "from": "self" if message.msg_from == current_id else "nself",
            "time": message.time
        }
        messages_json.append(msg_json)
    
    return jsonify(messages_json)