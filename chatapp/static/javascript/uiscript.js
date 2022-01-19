const innerWrapper = document.getElementById("inner-wrapper");
innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;

const chatList = document.getElementById("chat-list");
const innerMessageWrapper = document.getElementById("inner-wrapper");
const messageTextField = document.getElementById("msg-send-input");
const messageSendBtn = document.getElementById("msg-send-btn");
const closeModalButton = document.getElementById("close-btn");
const addChatButton = document.getElementById("add-chat-button");
const modalWrapper = document.getElementById("modal-container");

closeModalButton.addEventListener("click", function() {
    modalWrapper.classList.add("closed");
});

addChatButton.addEventListener("click", function() {
    modalWrapper.classList.remove("closed");
});

// 
// 
// 

let lastChat = "";
let currentChatId = 0;

messageSendBtn.addEventListener("click", function() {

    if (messageTextField.value === "") { return; }

    const content = messageTextField.value;
    fetch('http://127.0.0.1:5000/api/send', {
        method: 'POST',
        body: JSON.stringify({to: 2, content: content})
    });

    lastChat = content;

    const time = Math.floor(Date.now() / 1000);

    createMessage({from: "self", time: time, content: content})
    messageTextField.value = "";
    innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;

});

function updateChats(jsonChats) {

    jsonChats.forEach(chat => {
        const chatItem = document.createElement("li");
        chatItem.classList.add("chat-item");

        const innerButton = document.createElement("button");
        innerButton.innerText = chat.username;

        innerButton.addEventListener("click", function() {
            currentChatId = chat.id;
            getChatData();
        });

        chatItem.appendChild(innerButton);

        chatList.appendChild(chatItem)
    });

}

function getChatData() {

    if (currentChatId == 0) { return; }

    fetch('http://127.0.0.1:5000/api/get', {
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

window.setInterval(getChatData, 1000);

fetch('http://127.0.0.1:5000/api/chats', {method: 'POST'})
        .then(response => response.json())
        .then(data => updateChats(data));