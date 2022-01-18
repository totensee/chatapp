const messageTextField = document.getElementById("msg-send-input");
const messageSendBtn = document.getElementById("msg-send-btn");

messageSendBtn.addEventListener("click", function() {
    const rawResponse = fetch('http://127.0.0.1:5000/api/send', {
        method: 'POST',
        body: JSON.stringify({to: 2, content: messageTextField.value})
    });

    messageTextField.value = "";

});

const rawResponse = fetch('http://127.0.0.1:5000/api/get', {
        method: 'POST',
        body: JSON.stringify({to: 2})
});

const rawResponse2 = fetch('http://127.0.0.1:5000/api/join', {
        method: 'POST',
        body: JSON.stringify({chat: 2})
});