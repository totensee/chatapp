const messageTextField = document.getElementById("msg-send-input");
const messageSendBtn = document.getElementById("msg-send-btn");

messageSendBtn.addEventListener("click", function() {
    const rawResponse = fetch('http://127.0.0.1:5000/api/send', {
        method: 'POST',
        body: JSON.stringify({to: 1, content: messageTextField.value})
    });

    messageTextField.value = "";

});