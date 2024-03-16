const form = document.querySelector(".login form"),
    continueBtn = form.querySelector(".button input"),
    errorText = form.querySelector(".error-text");

form.onsubmit = (e) => {
    e.preventDefault();
};

continueBtn.onclick = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/login", true);
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            let data = xhr.response;
            if (xhr.status === 200) {
                location.href = "users";
            } else {
                errorText.style.display = "block";
                errorText.textContent = data;
            }
        }
    };
    let formData = new FormData(form);
    xhr.send(formData);
};