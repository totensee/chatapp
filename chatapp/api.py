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

@app.route("/api/chats", methods=["POST", "GET"])
def get_chats():

    if not current_user.is_authenticated: return "ERROR"

    chat_ids = [x for x in current_user.chats if x.isnumeric()]
    chats_json = []
    
    for id in chat_ids:
        user = User.query.filter_by(id=id).first()
        chat = {
            "id": id,
            "username": user.username
        }
        chats_json.append(chat)

    return jsonify(chats_json)

@app.route("/api/join", methods=["POST"])
def join_chat():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    chat = body["chat"]

    if str(chat) in current_user.chats:
        return "Already Created"
    elif chat == current_user.id:
        return "Cant add yourself"


    joinedUser = User.query.filter_by(id=chat).first()
    joinedUser.chats = current_user.id
    current_user.chats = chat

    db.session.commit()

    return "Success"

@app.route("/api/users", methods=["POST"])
def get_users():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    user_id = current_user.id
    subsstring = body["user"]

    user_list = list(User.query.filter(User.username.contains(subsstring)).all())[:9]

    return jsonify([[x.username, x.id] for x in user_list if x.id != user_id])