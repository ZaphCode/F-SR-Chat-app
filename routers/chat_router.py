from fastapi import APIRouter, Depends, HTTPException, Path, Query
from lib.user_dependency import get_user_required
from fastapi.responses import JSONResponse
from services.chatroom_service import ChatroomService
from services.message_service import MessageService
from services.user_service import UserService

router = APIRouter(prefix='/chat', tags=["Chats"])
message_service = MessageService()
chatroom_service = ChatroomService()
user_service = UserService()

@router.post("create-chatroom-with/{user_to_chat_pk}")
async def get_or_create_chatroom(
    user: dict = Depends(get_user_required),
    user_to_chat_pk: str = Path(..., description="User to chat")
):
    if user_to_chat_pk == user["pk"]:
        raise HTTPException(400, "You can create a chat with yourself")
    chatroom, service_error = chatroom_service.create_or_get_chatroom(user["pk"], user_to_chat_pk)
    if service_error:
        raise HTTPException(400, service_error)
    return JSONResponse(status_code=200, content={"chatroom_pk": chatroom["pk"]})


@router.get("/getMessagesAndUsers/{chatroom_pk}")
async def get_messages_of_chatroom(
    chatroom_pk: str = Path(...), 
    skip: int = Query(0),
    limit: int = Query(20),
    user: dict = Depends(get_user_required)
):
    chatroom, service_error = chatroom_service.get_by_pk(chatroom_pk)
    if service_error:
        return HTTPException(400, service_error)

    auth_user = None
    other_user = None

    if user["pk"] == chatroom["user_1_populated"]["pk"]:
        auth_user = chatroom["user_1_populated"]
        other_user = chatroom["user_2_populated"]
    else:
        auth_user = chatroom["user_2_populated"]
        other_user = chatroom["user_1_populated"]

    messages, service_error2 = message_service.get_messages_of_chatroom(chatroom_pk, user["pk"], skip, limit)
    if service_error2:
        return HTTPException(400, service_error2)
    return JSONResponse(
        status_code=200, 
        content={"messages": messages, "auth_user": auth_user, "other_user": other_user}
    )


    
    

