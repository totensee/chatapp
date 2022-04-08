const submitButton = document.getElementById("submit-bot");
const botName = document.getElementById("bot-name");
const formContainer = document.getElementById("inner-form-container");

submitButton.addEventListener("click", () => {
    
    if (botName.value === "") { return; }

    formContainer.innerHTML = "";
    fetch("/api/bot/create", {
        method: "POST",
        body: JSON.stringify({name: botName.value})
    })
        .then(response => response.json())
        .then(data => displayToken(data));
});

function displayToken(token) {
    const paragraph = document.createElement("p");
    paragraph.classList.add("token-data");
    paragraph.innerText = JSON.stringify(token, null, "\t");
    formContainer.appendChild(paragraph);
}