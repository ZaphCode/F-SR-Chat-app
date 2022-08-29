const { auth_user_pk } = document.getElementById("server-info").dataset
let userFields = document.getElementsByClassName("user-to-chat-field")

console.log(auth_user_pk);

for (let i = 0; i < userFields.length; i++) {
    const element = userFields[i];
    const { user_to_chat_pk } = element.dataset
    
    element.addEventListener("click", async (event) => {
        try {
            const res = await fetch(`/chatcreate-chatroom-with/${user_to_chat_pk}`, {method: "POST"})
            const {chatroom_pk} = await res.json()
            window.location.href = `/chatroom/${chatroom_pk}`
        } catch (error) {
            alert("Something went wrong")
            console.log(error);
        }
    })

}
