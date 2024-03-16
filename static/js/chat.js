const form = document.querySelector(".typing-area"),
    incoming_id = form.querySelector(".incoming_id").value,
    my_id = form.querySelector(".my_id").value,
    inputField = form.querySelector(".input-field"),
    sendBtn = form.querySelector("button"),
    chatBox = document.querySelector(".chat-box"),
    userStatus = document.querySelector(".details p");

form.onsubmit = (e) => {
    e.preventDefault();
};

window.onload = () => {
    scrollToBottom();
};

inputField.focus();
inputField.onkeyup = () => {
    if (inputField.value != "") {
        sendBtn.classList.add("active");
    } else {
        sendBtn.classList.remove("active");
    }
};

sendBtn.onclick = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/chat", true);
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                inputField.value = "";
                scrollToBottom();
            }
        }
    };
    let formData = new FormData(form);
    xhr.send(formData);
};
chatBox.onmouseenter = () => {
    chatBox.classList.add("active");
};

chatBox.onmouseleave = () => {
    chatBox.classList.remove("active");
};


function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

const socket = io();

function addChat(isIncoming, message) {
    const newChat = document.createElement('div');
    newChat.className = `chat ${isIncoming ? 'incoming' : 'outgoing'}`;
    newChat.innerHTML = isIncoming ? '<img src="/static/images/profile.jpg" alt="">' : '';
    newChat.innerHTML += `<div class="details"><p>${message}</p></div>`;
    chatBox.appendChild(newChat);
}

socket.on("message", (data) => {
    console.log(data);
    if (my_id == data.sender_id) {
        addChat(true, data.content);
    }
    if (my_id == data.receiver_id && incoming_id == data.sender_id) {
        addChat(false, data.content);
    }
    scrollToBottom();
});

socket.on("login", (data) => {
    console.log(data);
    if (incoming_id == data.id) {
        userStatus.textContent = "Online";
        // userStatus.style.color = "green";
    }
});

socket.on("logout", (data) => {
    if (incoming_id == data.id) {
        userStatus.textContent = "Offline";
        // userStatus.style.color = "red";
    }

});
