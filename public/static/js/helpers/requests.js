export async function getChatroom(user_to_chat_pk) {
    const res = await fetch(`/chatcreate-chatroom-with/${user_to_chat_pk}`, { method: "POST" })
    const { chatroom_pk } = await res.json()
    return chatroom_pk
}

export async function getMessagesAndUsers(chatroom_pk, skip = 0, limit = 20) {
    const res = await fetch(`/chat/getMessagesAndUsers/${chatroom_pk}?skip=${skip}&limit=${limit}`)
    const data = await res.json()
    if (!res.ok) {
        throw new Error(data.detail)
    }
    return data
}
