const logoutBtn = document.getElementById("logout-btn")
const chatBtn = document.getElementById("chat-btn")

if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        await fetch('/logout', {method: "DELETE"})
        window.location.href = `/`
        location.reload()
    })
}

if (chatBtn) {
    chatBtn.addEventListener("click", async (e) => {
        window.location.href = `/chat`
    })
}

