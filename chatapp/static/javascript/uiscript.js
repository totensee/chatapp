const innerWrapper = document.getElementById("inner-wrapper");
const chatList = document.getElementById("chat-list");
const innerMessageWrapper = document.getElementById("inner-wrapper");
const messageTextField = document.getElementById("msg-send-input");
const messageSendBtn = document.getElementById("msg-send-btn");
const closeContactModalButton = document.getElementById("contact-close-btn");
const addChatButton = document.getElementById("add-chat-button");
const contactModalWrapper = document.getElementById("contact-modal-container");
const contactInput = document.getElementById("contact-input");
const userList = document.getElementById("username-list");
const createServerBtn = document.getElementById("create-server-btn");
const createServerModalWrapper = document.getElementById("create-server-modal-container");
const closeServerModalBtn = document.getElementById("server-modal-close-btn");
const serverModalBtn = document.getElementById("server-modal-btn");
const serverModalInput = document.getElementById("server-modal-input");

serverModalBtn.addEventListener("click", () => {
    fetch("/api/servers/create", {
        method: "POST",
        body: JSON.stringify({name: serverModalInput.value})
    });
    createServerModalWrapper.classList.add("closed");
    setTimeout(function() { getChatData(); }, 100);
});

closeServerModalBtn.addEventListener("click", () => {
    createServerModalWrapper.classList.add("closed");
});

createServerBtn.addEventListener("click", () => {
    contactModalWrapper.classList.add("closed");
    createServerModalWrapper.classList.remove("closed");
});

closeContactModalButton.addEventListener("click", function() {
    contactModalWrapper.classList.add("closed");
});

addChatButton.addEventListener("click", function() {
    if (!createServerModalWrapper.classList.contains("closed")) {
        createServerModalWrapper.classList.add("closed");
        return;
    }
    contactModalWrapper.classList.toggle("closed");
});

contactInput.addEventListener("input", function(input) {
    fetch("/api/users", {
        method: "POST",
        body: JSON.stringify({user: input.target.value})
    })
        .then(response => response.json())
        .then(data => updateUsernames(data));
});

function updateUsernames(usernameJson) {
    userList.innerHTML = "";

    usernameJson.forEach(username => {
        const userNameItem = document.createElement("li");
        userNameItem.classList.add("user-item");

        const userNameParagraph = document.createElement("p");
        userNameParagraph.classList.add("username");
        userNameParagraph.innerText = username[0];

        const contactBtn = document.createElement("button");
        contactBtn.classList.add("contact-btn");
        contactBtn.innerText = "contact";
        contactBtn.addEventListener("click", function() {
            joinChat(username[1], username[2]);
        });

        userNameItem.appendChild(userNameParagraph);
        userNameItem.appendChild(contactBtn);

        userList.appendChild(userNameItem);
    });
}

function joinChat(chatId, server) {
    if (!server) {
        fetch("/api/join", {
            method: "POST",
            body: JSON.stringify({chat: chatId})
        });
    } else if (server) {
        fetch("/api/servers/join", {
            method: "POST",
            body: JSON.stringify({server: chatId})
        });
    }

    setTimeout(function() { getChatData(); }, 100);
}

let lastChat = null;
let currentChatId = 0;
let currentChatIsServer = null;

messageSendBtn.addEventListener("click", function() {

    if (messageTextField.value === "") { return; }
    else if (currentChatId == 0) { return; }

    const content = messageTextField.value;
    fetch('/api/send', {
        method: 'POST',
        body: JSON.stringify({to: currentChatId, content: content, server: currentChatIsServer})
    });

    const time = Math.floor(Date.now() / 1000);

    createMessage({from: "self", time: time, content: content})
    messageTextField.value = "";
    innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;

});

function getChatData() {
    fetch('/api/chats', {method: 'POST'})
        .then(response => response.json())
        .then(data => updateChats(data));
}

function updateChats(jsonChats) {

    chatList.innerHTML = "";

    jsonChats.forEach(chat => {
        const chatItem = document.createElement("li");
        chatItem.classList.add("chat-item");

        if (chat.id == currentChatId && chat.server == currentChatIsServer) { chatItem.classList.add("active"); }

        const innerButton = document.createElement("button");
        innerButton.innerText = chat.name;

        if (chat.server) {
            chatItem.classList.add("server");
        }

        innerButton.addEventListener("click", function() {
            activeElems = document.querySelectorAll(".chat-item.active");
            activeElems.forEach((activeElem) => {
                activeElem.classList.remove("active");
            });
            currentChatId = chat.id;
            currentChatIsServer = chat.server;
            chatItem.classList.add("active");
            getMessageData();
            getChatData();
        });

        chatItem.appendChild(innerButton);

        
        fetch('/api/new_messages', {
            method: 'POST',
            body: JSON.stringify({from: chat.id, server: chat.server})
        })
            .then(response => response.json())
            .then(data => addUnseenMessages(data, chatItem));
    
        chatList.appendChild(chatItem)
    });

}

function addUnseenMessages(jsonMessage, chatItem) {
    unseenMessageParagraph = document.createElement("p");
    unseenMessageParagraph.innerText = jsonMessage.unseen;
    unseenMessageParagraph.classList.add("unseen-messages");
    chatItem.appendChild(unseenMessageParagraph);
}

function getMessageData() {

    if (currentChatId == 0) { return; }

    fetch('/api/get', {
        method: 'POST',
        body: JSON.stringify({to: currentChatId, server: currentChatIsServer}),
        server: currentChatIsServer
    })
        .then(response => response.json())
        .then(data => switchChat(data));
    

}

function switchChat(jsonChats) {

    if (jsonChats.length === 0) {
        innerMessageWrapper.innerHTML = "";
        lastChat = null;
        return;
    }
    if (jsonChats[jsonChats.length - 1].id == lastChat) { return; } // Check if the last message is the same as the last message in the chat

    lastChat = jsonChats[jsonChats.length - 1].id;

    innerMessageWrapper.innerHTML = "";

    jsonChats.forEach(chat => {
        createMessage(chat);   
    });
    innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;
}

function createMessage(chat) {
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message");

    if (chat.from == "self") {
        messageContainer.classList.add("right")
    } else {
        messageContainer.classList.add("left");
    }
    
    const messageContent = document.createElement("p");
    
    messageContent.innerText = chat.content;

    if (currentChatIsServer && chat.from != "self") {
        const authorParagraph = document.createElement("p");
        authorParagraph.innerText = chat.from;
        authorParagraph.classList.add("message-author");
        messageContainer.appendChild(authorParagraph);
    }

    messageContent.classList.add("message-content");
    
    const date = new Date(chat.time * 1000);
    const hours = date.getHours();
    const minutes = "0" + date.getMinutes();
    const seconds = "0" + date.getSeconds();
    const formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

    const timeParagraph = document.createElement("p");
    timeParagraph.innerText = formattedTime;
    timeParagraph.classList.add("message-time");

    messageContainer.appendChild(messageContent);
    messageContainer.appendChild(timeParagraph);
    innerMessageWrapper.appendChild(messageContainer);
}

window.setInterval(getMessageData, 1000);
window.setInterval(getChatData, 5000)
getChatData();