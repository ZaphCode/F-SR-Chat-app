from fastapi import APIRouter, Path, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from lib.exceptions import ServerErrorPageException
from services.chatroom_service import ChatroomService
from services.message_service import MessageService
from services.user_service import UserService
from lib.user_dependency import get_user_optional, get_user_required
import config

#* Initializations
router = APIRouter(tags=["Views"])
j2 = Jinja2Templates(directory='public/templates')
user_service = UserService()
chatroom_service = ChatroomService()
message_service = MessageService()

@router.get('/', response_class=HTMLResponse)
async def index_page(request: Request, user: dict = Depends(get_user_optional)):
    return j2.TemplateResponse('index.html', {"request": request, "user": user})

@router.get('/info', response_class=HTMLResponse)
async def index_page(request: Request, user: dict = Depends(get_user_optional)):
    return j2.TemplateResponse('info.html', {"request": request, "user": user})

@router.get('/profile', response_class=HTMLResponse)
async def index_page(request: Request, user: dict = Depends(get_user_required)):
    chatrooms, service_error = chatroom_service.get_chatrooms_of_user(user["pk"])
    if service_error:
        raise ServerErrorPageException("DB_ERROR", service_error)
    return j2.TemplateResponse('profile.html', {"request": request, "user": user, "chatrooms": chatrooms})

#* Chat Page
@router.get('/chat', response_class=HTMLResponse)
async def index_page(
    request: Request, 
    user: dict = Depends(get_user_required),
):
    users, service_error = user_service.get_all(limit=10)
    if service_error:
        raise ServerErrorPageException("DB_ERR", service_error)
    
    return j2.TemplateResponse('chat.html', {
        "request": request, 
        "user": user, "users": users, 
    })

#* Chat / <pk>
@router.get('/chat/{chatroom_pk}', response_class=HTMLResponse)
async def index_page(
    request: Request, 
    user: dict = Depends(get_user_required),
    chatroom_pk: str = Path(..., description="Chat primary key")):
    users, service_error = user_service.get_all(limit=10)
    if service_error:
        raise ServerErrorPageException("DB_ERR", service_error)
    chatroom, service_error = chatroom_service.get_by_pk(chatroom_pk)
    if service_error or not chatroom:
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    if not (chatroom["user_pk_1"] == user["pk"] or chatroom["user_pk_2"] == user["pk"]):
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    
    return j2.TemplateResponse('chat.html', {
        "request": request, 
        "user": user, "users": users, 
        "app_domain": config.app_domain,
        "chatroom_pk": chatroom["pk"]
    })

@router.get('/signin', response_class=HTMLResponse, tags=["Auth"])
async def signin_page(request: Request, user: dict = Depends(get_user_optional)):
    if user:
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    return j2.TemplateResponse('signin.html', {"request": request, "user": user})

@router.get('/signup', response_class=HTMLResponse, tags=["Auth"])
async def signup_page(request: Request, user: dict = Depends(get_user_optional)):
    if user:
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    return j2.TemplateResponse('signup.html', {"request": request, "user": user})

#* Testing
@router.get('/testing/{id}', response_class=HTMLResponse)
async def testing_page(id: str, request: Request, user: dict = Depends(get_user_optional)):
    if id == "35":
        raise ServerErrorPageException("HATE_ERROR", "No me gusta para nada ese numero deberias cambiarlo o te agarro a putasos")
    return j2.TemplateResponse('test.html', {"request": request, "user": user, "id": id})





