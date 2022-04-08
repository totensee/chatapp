import json, time, jwt
from chatapp import app, db
from chatapp.models import User, Message, Server, ServerMessage, Bot
from flask import request, jsonify
from flask_login import current_user

def auth_token(id):
    payload = {
        "id": id
    }

    return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

@app.route("/api/send", methods=["POST"])
def send_message():

    if not current_user.is_authenticated: return "ERROR"
    
    body = json.loads(request.data.decode())
    send_time = time.time()

    if not body["server"]:

        message = Message(
            msg_from = current_user.id,
            msg_to = body["to"],
            content = body["content"],
            time = send_time,
            seen = False
        )
        
        db.session.add(message)

    elif body["server"]:

        server_message = ServerMessage(
            server_id = body["to"],
            msg_from = current_user.id,
            content = body["content"],
            time = send_time
        )

        server = Server.query.filter_by(
            id = body["to"]
        ).first()
        server.last_message = send_time

        db.session.add(server_message)
    
    db.session.commit()
    return "Success"

@app.route("/api/get", methods=["POST"])
def get_messages():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    messages_json = []

    if not body["server"]:

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

        for message in all_messages:
            msg_json = {
                "content": message.content,
                "from": "self" if message.msg_from == current_id else User.query.filter_by(id=message.msg_from).first().username,
                "time": message.time,
                "id": message.id
            }
            messages_json.append(msg_json)
        
        unseen_messages = list(Message.query.filter_by(msg_from=second_id, seen=False))
        
        for unseen_message in unseen_messages:
            unseen_message.seen = True

    elif body["server"]:

        current_id = current_user.id
        server_id = body["to"] # the id of the server

        all_messages = list(ServerMessage.query.filter_by(
            server_id = server_id
        ))

        all_messages.sort(key=lambda x: x.time)

        for message in all_messages:
            msg_json = {
                "content": message.content,
                "from": "self" if message.msg_from == current_id and not message.bot else (User.query.filter_by(id=message.msg_from).first().username if message.bot == 0 else f"{Bot.query.filter_by(id=message.msg_from).first().name} - Bot"),
                "time": message.time,
                "id": message.id
            }
            messages_json.append(msg_json)

    db.session.commit() # Commiting because of the seen attribute

    return jsonify(messages_json)


@app.route("/api/chats", methods=["POST"])
def get_chats():

    if not current_user.is_authenticated: return "ERROR"

    chat_ids = [x for x in current_user.chats if x.isnumeric()]
    server_ids = [x for x in current_user.servers_in if x.isnumeric()]
    chats_json = []

    current_id = current_user.id

    def sortChats(chat):

        if not chat["server"]:

            second_id = chat["id"]

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

            if len(all_messages) > 0:
                return all_messages[-1].time
            else:
                return 0
        
        elif chat["server"]:

            servers_in = current_user.servers_in
            server_id = chat["id"]

            server = Server.query.filter_by(id=server_id).first()

            return server.last_message

    for id in chat_ids:
        user = User.query.filter_by(id=id).first()
        chat = {
            "id": id,
            "server": False,
            "name": user.username
        }
        chats_json.append(chat)

    for id in server_ids:
        server = Server.query.filter_by(id=id).first()
        chat = {
            "id": id,
            "server": True,
            "name": server.name
        }
        chats_json.append(chat)

    chats_json.sort(key=sortChats, reverse=True)

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
    server_list = list(Server.query.filter(Server.name.contains(subsstring)).all())[:9]

    return jsonify([[x.username, x.id, False] for x in user_list if x.id != user_id] + [[x.name, x.id, True] for x in server_list]) # [name, id, server]

@app.route("/api/new_messages", methods=["POST"])
def new_messages():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    if not body["server"]:

        current_id = current_user.id
        second_id = body["from"]
        unseen_messages = list(Message.query.filter_by(msg_to=current_id, msg_from=second_id, seen=False))

        return jsonify({"unseen": str(len(unseen_messages))})

    elif body["server"]:

        return jsonify({"unseen": 0}) # Implement

@app.route("/api/servers/create", methods=["POST"])
def create_server():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    server_name = body["name"]
    
    newServer = Server(
        name = server_name,
        owner = current_user.id
    )

    db.session.add(newServer)
    db.session.commit()

    current_user.servers_in = newServer.id

    db.session.commit()

    return "Success"

@app.route("/api/servers/join", methods=["POST"])
def join_server():

    if not current_user.is_authenticated: return "ERROR"

    body = json.loads(request.data.decode())

    server_id = body["server"]

    if str(server_id) in current_user.servers_in:
        return "Already Joined"
    
    current_user.servers_in = server_id

    db.session.commit()

    return "Success"

@app.route("/api/bot/create", methods=["POST"])
def create_bot():

    body = json.loads(request.data.decode())

    bot = Bot(
        name = body["name"]
    )

    db.session.add(bot)
    db.session.commit()

    bot.auth_token = auth_token(bot.id)

    db.session.add(bot)
    db.session.commit()

    return jsonify({"token": bot.auth_token, "id": bot.id})

@app.route("/api/bot/join/<bot_id>/<server_id>", methods=["POST", "GET"])
def join_bot(bot_id, server_id):

    bot = Bot.query.filter_by(id=bot_id).first()

    if not bot:
        return "ERROR"

    bot.servers_in = server_id

    db.session.commit()

    return jsonify({"joined": server_id})

@app.route("/api/bot/servers_in", methods=["POST"])
def get_bot_servers():

    body = json.loads(request.data.decode())

    bot_token = body["auth_token"]

    bot = Bot.query.filter_by(auth_token=str(bot_token)).first()

    if not bot:
        return "ERROR"

    return jsonify({"servers": bot.servers_in})

@app.route("/api/bot/get_messages", methods=["POST"])
def get_bot_messages():

    body = json.loads(request.data.decode())

    bot_token = body["auth_token"]
    server_id = body["server"]

    bot = Bot.query.filter_by(auth_token=bot_token).first()

    if not bot:
        return "ERROR"

    messages = list(ServerMessage.query.filter_by(server_id=server_id))

    messages.sort(key=lambda x: x.time)

    messages_json = []

    for message in messages:
        messages_json.append({
            "content": message.content,
            "time": message.time,
            "bot": message.bot != 0
        })

    return jsonify(messages_json)

@app.route("/api/bot/send_message", methods=["POST"])
def send_bot_message():

    body = json.loads(request.data.decode())

    bot_token = body["auth_token"]
    server_id = body["server"]
    message = body["content"]

    bot = Bot.query.filter_by(auth_token=bot_token).first()

    if not bot:
        return "ERROR"

    send_time = time.time()

    newMessage = ServerMessage(
        content = message,
        server_id = server_id,
        bot = 1,
        msg_from = bot.id,
        time = send_time
    )

    db.session.add(newMessage)
    db.session.commit()

    return jsonify({"status": "success"})