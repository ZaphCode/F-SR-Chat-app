import { TEXTS } from "./helpers/texts.js"

const translate_btn = document.getElementById("translate-btn")

let current_lang = "en"

translate_btn.addEventListener('click', (e) => {
    current_lang === "en" ? current_lang = "es" : current_lang = "en" 
    for (let i = 1; i < 6; i++) {
        const text = document.getElementById(`text_${i}`)
        if (text) text.innerText = TEXTS[`text_${i}`][current_lang]
    }
})

