
const logoutBtn = document.getElementById("logout-btn")

if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        await fetch('logout', {method: "DELETE"})
        location.reload()
    })
}