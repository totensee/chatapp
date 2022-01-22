const flashMessages = document.querySelectorAll(".flash-message");
const flashMessageButtons = document.querySelectorAll(".flash-close");

flashMessageButtons.forEach(btn => {
    btn.addEventListener("click", function() {
        btn.parentElement.style.display = "none";
    });
});