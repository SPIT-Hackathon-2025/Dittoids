function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Display user message
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class='user'><p>${userInput}</p></div>`;

    fetch("/send", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            chatBox.innerHTML += `<div class='assistant'><p>${data.response}</p></div>`;
        }
    });

    document.getElementById("user-input").value = "";
}
