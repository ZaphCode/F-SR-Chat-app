from fastapi import APIRouter, Depends, Path
from lib.user_dependency import get_user_required
from services.chatroom_service import ChatroomService
from services.message_service import MessageService

router = APIRouter(prefix='/chat', tags=["Chats"])
message_service = MessageService()
chatroom_service = ChatroomService()

@router.post("create-chatroom-with/{user_to_chat_pk}")
async def get_or_create_chatroom(
    user: dict = Depends(get_user_required),
    user_to_chat_pk: str = Path(..., description="User to chat")
):
    if user_to_chat_pk == user["pk"]:
        return "You can create a chat with yourself"
    chatroom, service_error = chatroom_service.create_or_get_chatroom(user["pk"], user_to_chat_pk)
    if service_error:
        return service_error
    return chatroom["pk"]

    

