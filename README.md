# Chat app

## TODO

- [x] Routes design
    - [x] Login Page
    - [x] Register Page
    - [x] message Page
        - [x] message word wrap
    - [x] Home Page

- [x] flask
    - [x] Flash message implemantation
    - [x] User auth username check
    - [x] API
        - [x] Send Messages
        - [x] Get messages
        - [x] Join Channel
        - [x] Get Chats
        - [x] Get Users
        - [x] Sort Messages after a time
            - [x] frequent update
        - [x] Unseen Messages
        - [x] Servers

- [ ] User settings
    - [ ] pfp

- [ ] javascript
    - [ ] Server creatio

- Bot
    - "/api/bot/create" json = {name}
    - "/api/bot/join/bot_id/server_id"
    - "/api/bot/servers_in" json = {bot_token}, return = [server_id]
    - "/api/bot/get_messages" json = {bot_token, server_id}, return = [{content, time}]
    - "/api/bot/send_message" json = {bot_token, server_id, content} return {status}