import { DisplayManager } from "./helpers/display.js";
import { initEmojis } from "./helpers/emojis.js";
import { getChatroom, getMessagesAndUsers } from "./helpers/requests.js";
alert("FFFack")
//* Constants
const { chatroom_pk } = document.getElementById("server-info").dataset
const user_fields = document.getElementsByClassName("users-to-chat-field")
const MC = document.getElementById("messages-container")

//* Display mannager
const display = new DisplayManager(MC)

//* Open Websocket connection 
if (chatroom_pk) {
    (async () => {
        try {
            display.renderLoading()
            const { messages, auth_user, other_user } = await getMessagesAndUsers(chatroom_pk)
            display.renderMessages(messages, auth_user, other_user)
            let max_top = -500, skip = 0, limit = 20
            const msg_div = MC.firstElementChild
            msg_div.addEventListener("scroll", async (event) => {
                if (msg_div.scrollTop < max_top) {
                    max_top *= 2, skip += 20, limit += 20
                    const { messages, auth_user, other_user } = await getMessagesAndUsers(chatroom_pk, skip, limit)
                    display.renderMoreMessages(messages, auth_user, other_user)
                }
            })
            initEmojis()
            let protocol
            window.location.protocol === 'https:' ? protocol = 'wss' : protocol = 'ws'
            const ws = new WebSocket(`${protocol}://${location.host}/ws/chatroom/${chatroom_pk}`);
            document.getElementById("msg-form").addEventListener("submit", event => {
                event.preventDefault()
                const message = event.target["msg-input"].value.trim()
                if (!message || message.lenght <= 0) return
                ws.send(JSON.stringify({ to_pk: other_user.pk, message }))
                event.target.reset()
            })

            ws.onmessage = (event) => {
                let data = JSON.parse(event.data)
                switch (data.type) {
                    case "message":
                        if (data.chatroom_pk === chatroom_pk) display.renderNewMessage(data, auth_user, other_user)
                        break
                    default:
                        break
                }
            }
            ws.onclose = (event) => {
                display.renderError("Socket close")
            }
            ws.onclose = (event) => {
                display.renderError("Connection error")
            }
        } catch (error) {
            display.renderError(error)
            console.log("<< Error >>", error);
        }
    })()
}

//* Add listeners to all user fields
for (let field of user_fields) {
    const { user_to_chat_pk } = field.dataset
    field.addEventListener("click", async (event) => {
        try {
            display.renderLoading()
            const chatroom_pk = await getChatroom(user_to_chat_pk)
            window.location.href = `/chat/${chatroom_pk}`
        } catch (error) {
            display.renderError(error)
            console.log("<< Error >>", error);
        }
    })
}