const innerWrapper = document.getElementById("inner-wrapper");
innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;

const chatList = document.getElementById("chat-list");

function updateChats(jsonChats) {

    console.log(jsonChats)

    jsonChats.forEach(chat => {
        const chatItem = document.createElement("li");
        chatItem.classList.add("chat-item");

        const innerButton = document.createElement("button");
        innerButton.innerText = chat.username;

        chatItem.appendChild(innerButton);

        chatList.appendChild(chatItem)
    });

}

fetch('http://127.0.0.1:5000/api/chats', {method: 'POST'})
        .then(response => response.json())
        .then(data => updateChats(data));