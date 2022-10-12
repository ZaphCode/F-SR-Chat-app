export function initEmojis() {
    const emojis_btn = document.getElementById("emojis-btn")
    const emojis_div = document.getElementById("emojis-div")
    const msg_input = document.getElementById("msg-input")
    const emojis = document.getElementsByClassName("emoji")

    emojis_div.style.display = "none"; // Init

    for (let emoji of emojis) {
        emoji.addEventListener('click', event => {
            msg_input.value += emoji.textContent
        })
    }

    emojis_btn.addEventListener('click', event => {
        if (emojis_div.style.display === "none") {
            emojis_div.style.display = "grid";
        } else {
            emojis_div.style.display = "none"
        }
    })

    document.addEventListener("click", event => {
        if (
            emojis_div.style.display === "grid" &&
            !event.target.matches("#emojis-btn")
        ) {
            if (!event.target.closest("#emojis-div")) {
                emojis_div.style.display = "none"
            }
        }
    })
}




