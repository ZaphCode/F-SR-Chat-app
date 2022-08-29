const serverInfo = document.getElementById("server-info")
const messageContainer = document.getElementById("message-container")
const textAreaMsg = document.getElementById("text-area-msg")
const errorMsg = document.getElementById("error-msg")
const form = document.getElementById("form-message")

const { chatroom_pk, user_pk: auth_user_pk, app_domain } = serverInfo.dataset

let ws

console.log(auth_user_pk)

try {
    ws = new WebSocket(`ws://${app_domain}/ws/chatroom/${chatroom_pk}`);
} catch (error) {
    alert("Connection error")
    console.log(error)
}

//* On message handler
ws.onmessage = (event) => {
    let msg = JSON.parse(event.data)
    let container = document.createElement('div')
    if (msg.sender_pk === auth_user_pk) container.classList.add('flex', 'justify-start');
    else container.classList.add('flex', 'justify-end');
    let message = document.createElement('p')
    if (msg.sender_pk === auth_user_pk) message.classList.add("bg-red-500", "max-w-sm", "overflow-clip", "py-3", "px-6", "rounded-lg", "text-white");
    else message.classList.add("bg-gray-500", "py-3", "px-6", "rounded-lg", "text-white", "max-w-sm", "overflow-clip");
    message.innerText = msg.message
    container.appendChild(message)
    messageContainer.insertBefore(container, messageContainer.firstChild)
};

form.addEventListener('submit', (event) => {
    event.preventDefault()

    message = textAreaMsg.value.trim()

    if (!message || message.length <= 0) {
        errorMsg.innerText = "Don't send empty messages"
        textAreaMsg.value = ""
        return
    }

    try {
        ws.send(JSON.stringify({ message }))
        errorMsg.innerText = ""
        textAreaMsg.value = ""
    } catch (error) {
        console.log(">>> Error sendig message");
        console.log(error)
    }

})

