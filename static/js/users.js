const searchBar = document.querySelector(".search input"),
    searchIcon = document.querySelector(".search button"),
    usersList = document.querySelector(".users-list");

// var scriptTag = document.currentScript;
// var usersDataAttribute = scriptTag.getAttribute('data-users');

// // var users = JSON.parse(usersDataAttribute);
// console.log(usersDataAttribute);



searchIcon.onclick = () => {
    searchBar.classList.toggle("show");
    searchIcon.classList.toggle("active");
    searchBar.focus();
    if (searchBar.classList.contains("active")) {
        searchBar.value = "";
        searchBar.classList.remove("active");
    }
};

searchBar.onkeyup = () => {
    let searchTerm = searchBar.value;
    if (searchTerm != "") {
        searchBar.classList.add("active");
    } else {
        searchBar.classList.remove("active");
    }
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", "php/search.php", true);
    // xhr.onload = () => {
    //     if (xhr.readyState === XMLHttpRequest.DONE) {
    //         if (xhr.status === 200) {
    //             let data = xhr.response;
    //             usersList.innerHTML = data;
    //         }
    //     }
    // };
    // xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // xhr.send("searchTerm=" + searchTerm);
};

// setInterval(() => {
//     let xhr = new XMLHttpRequest();
//     xhr.open("GET", "php/users.php", true);
//     xhr.onload = () => {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 let data = xhr.response;
//                 if (!searchBar.classList.contains("active")) {
//                     usersList.innerHTML = data;
//                 }
//             }
//         }
//     };
//     xhr.send();
// }, 500);

const socket = io();

socket.on("register", (data) => {
    console.log(data);
    var users = document.querySelectorAll('.users-list');
    var newUserHTML = `
        <a href="/chat" class="user">
            <div class="content">
                <input type="hidden" class="user_id" name="id" value="${data.id}">
                <img src="/static/images/profile.jpg" alt="">
                <div class="details">
                    <span>${data.username}</span>
                    <p></p>
                </div>
            </div>
            <div class="status-dot online"><i class="fas fa-circle"></i></div>
        </a>
    `;

    var tempDiv = document.createElement('div');
    tempDiv.innerHTML = newUserHTML;
    var newUser = user.firstChild;

    users.appendChild(newUser);
});

socket.on("login", (data) => {
    console.log(data);
    var users = document.querySelectorAll('.users-list a');
    users.forEach(function (userElement) {
        var userIdInput = userElement.querySelector('.user_id');
        if (userIdInput && userIdInput.value == data.id) {
            statusDot = userElement.querySelector(".status-dot");
            statusDot.setAttribute("class", "status-dot online");
        }
    });
});

socket.on("logout", (data) => {
    console.log(data);
    var users = document.querySelectorAll('.users-list a');
    users.forEach(function (userElement) {
        var userIdInput = userElement.querySelector('.user_id');
        if (userIdInput && userIdInput.value == data.id) {
            statusDot = userElement.querySelector(".status-dot");
            statusDot = userElement.querySelector(".status-dot");
            statusDot.setAttribute("class", "status-dot offline");
        }
    });
});