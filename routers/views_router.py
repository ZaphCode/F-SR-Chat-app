from typing import Tuple
from fastapi import APIRouter, BackgroundTasks, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from lib.exceptions import ServerErrorPageException
from lib.get_user import get_user_optional, get_user_required
from lib.upload_bg_task import upload_profile_img
from database.user_model import User
from services.user_service import UserService
from schemas.signup_schema import SignUpSch
from schemas.signin_schema import SignInSch

router = APIRouter(tags=["Views"])
j2 = Jinja2Templates(directory='public/templates')
user_service = UserService(model=User)

@router.get('/', response_class=HTMLResponse)
async def index_page(request: Request, user: dict = Depends(get_user_optional)):
    return j2.TemplateResponse('index.html', {"request": request, "user": user})

@router.get('/protected', response_class=HTMLResponse)
async def index_page(request: Request, user: dict = Depends(get_user_required)):
    return j2.TemplateResponse('protected.html', {"request": request, "user": user})

@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request, user: dict = Depends(get_user_optional)):
    if user:
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    return j2.TemplateResponse('login.html', {"request": request, "user": user})

@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request, user: dict = Depends(get_user_optional)):
    if user:
        return RedirectResponse('/', status.HTTP_307_TEMPORARY_REDIRECT)
    return j2.TemplateResponse('register.html', {"request": request, "user": user})

@router.post('/login', response_class=RedirectResponse)
async def login(
    request: Request, 
    form_data: Tuple[SignInSch, dict] = Depends(SignInSch.as_form), 
    user: dict = Depends(get_user_optional)
):
    if user:
        raise ServerErrorPageException("Auth", "You are already authenticated")
    credentials, form_errors = form_data
    if form_errors:
        return j2.TemplateResponse('login.html', {"request": request, "form_errors": form_errors, "user": user})
    created_user, service_error = user_service.login(credentials.email, credentials.password)
    if service_error:
        return j2.TemplateResponse('login.html', {"request": request, "service_error": service_error, "user": user})
    request.session["user_pk"] = created_user["pk"]
    return RedirectResponse('/', status.HTTP_303_SEE_OTHER)

@router.post('/register', response_class=RedirectResponse)
async def register(
    request: Request, 
    bg_tasks: BackgroundTasks, 
    form_data: Tuple[SignUpSch, dict] = Depends(SignUpSch.as_form), 
    user: dict = Depends(get_user_optional)
):
    if user:
        raise ServerErrorPageException("Auth", "You are already authenticated")
    data, form_errors = form_data
    if form_errors:
        return j2.TemplateResponse('register.html', {"request": request, "form_errors": form_errors, "user": user})
    new_user, service_error = user_service.register(data)
    if service_error:
        return j2.TemplateResponse('register.html', {"request": request, "server_error": service_error, "user": user})
    if data.z_file:
        bg_tasks.add_task(upload_profile_img, new_user.get('pk'), data.z_file)
    return RedirectResponse('/login', status.HTTP_303_SEE_OTHER)

@router.delete('/logout')
async def logout(request: Request):
    request.session.pop("user_pk", None)
    return "Logout success"

