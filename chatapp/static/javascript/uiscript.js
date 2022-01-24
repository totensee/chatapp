const innerWrapper = document.getElementById("inner-wrapper");
const chatList = document.getElementById("chat-list");
const innerMessageWrapper = document.getElementById("inner-wrapper");
const messageTextField = document.getElementById("msg-send-input");
const messageSendBtn = document.getElementById("msg-send-btn");
const closeModalButton = document.getElementById("close-btn");
const addChatButton = document.getElementById("add-chat-button");
const modalWrapper = document.getElementById("modal-container");
const contactInput = document.getElementById("contact-input");
const userList = document.getElementById("username-list");

closeModalButton.addEventListener("click", function() {
    modalWrapper.classList.add("closed");
});

addChatButton.addEventListener("click", function() {
    modalWrapper.classList.remove("closed");
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
            joinChat(username[1]);
        });

        userNameItem.appendChild(userNameParagraph);
        userNameItem.appendChild(contactBtn);

        userList.appendChild(userNameItem);
    });
}

function joinChat(chatId) {
    fetch("/api/join", {
        method: "POST",
        body: JSON.stringify({chat: chatId})
    });


    setTimeout(function() { getChatData(); }, 100);
}

let lastChat = "";
let currentChatId = 0;

messageSendBtn.addEventListener("click", function() {

    if (messageTextField.value === "") { return; }

    const content = messageTextField.value;
    fetch('/api/send', {
        method: 'POST',
        body: JSON.stringify({to: currentChatId, content: content})
    });

    // lastChat = content;

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

        if (chat.id == currentChatId) { chatItem.classList.add("active"); }

        const innerButton = document.createElement("button");
        innerButton.innerText = chat.username;

        innerButton.addEventListener("click", function() {
            activeElem = document.querySelector(".chat-item.active");
            if (activeElem) { activeElem.classList.remove("active"); }
            currentChatId = chat.id;
            chatItem.classList.add("active");
            getMessageData();
            getChatData();
            lastChat = "";
        });

        chatItem.appendChild(innerButton);

        
        fetch('/api/new_messages', {
            method: 'POST',
            body: JSON.stringify({from: chat.id})
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
        body: JSON.stringify({to: currentChatId})
    })
        .then(response => response.json())
        .then(data => switchChat(data));
}

function switchChat(jsonChats) {

    if (jsonChats.length === 0) { return; }
    if (jsonChats.at(-1).content == lastChat) { return; }

    lastChat = jsonChats.at(-1).content

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