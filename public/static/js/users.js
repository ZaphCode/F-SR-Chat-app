const show_users_btn = document.getElementById("show-users-btn")
const hide_users_btn = document.getElementById("hide-users-btn")
const users_container = document.getElementById("users-to-chat-container")

show_users_btn.addEventListener("click", event => {
    show_users_btn.style.display = "none";
    hide_users_btn.style.display = "block";
    users_container.style.display = "block";
})

hide_users_btn.addEventListener("click", event => {
    show_users_btn.style.display = "block";
    hide_users_btn.style.display = "none";
    users_container.style.display = "none";
})

function myFunction(x) {
    if (x.matches) { // If media query matches
        show_users_btn.style.display = "block";
        hide_users_btn.style.display = "none";
        users_container.style.display = "none";
    } else {
        show_users_btn.style.display = "none";
        hide_users_btn.style.display = "block";
        users_container.style.display = "block";
    }
}

var x = window.matchMedia("(max-width: 640px)")
myFunction(x)
x.addListener(myFunction)

