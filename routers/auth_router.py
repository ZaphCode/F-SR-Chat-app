from typing import Tuple
from fastapi import APIRouter, BackgroundTasks, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from lib.exceptions import ServerErrorPageException
from lib.user_dependency import get_user_optional
from lib.cloudinary import upload_profile_img
from lib.hash_fns import decrypt_message, encrypt_message
from services.user_service import UserService
from schemas.signup_schema import SignUpSch
from schemas.signin_schema import SignInSch

#* Initializations
router = APIRouter(tags=["Auth"])
j2 = Jinja2Templates(directory='public/templates')
user_service = UserService()

@router.post('/signin', response_class=RedirectResponse)
async def signin(
    request: Request, 
    form_data: Tuple[SignInSch, dict] = Depends(SignInSch.as_form), 
    user: dict = Depends(get_user_optional)
):
    if user:
        raise ServerErrorPageException("Auth", "You are already authenticated")
    credentials, form_errors = form_data
    if form_errors:
        return j2.TemplateResponse('signin.html', {"request": request, "form_errors": form_errors, "user": user})
    user_found, service_error = user_service.singin(credentials.email, credentials.password)
    if service_error:
        return j2.TemplateResponse('signin.html', {"request": request, "service_error": service_error, "user": user})
    request.session["user_pk"] = user_found["pk"]
    return RedirectResponse('/', status.HTTP_303_SEE_OTHER)

@router.post('/signup', response_class=RedirectResponse)
async def signup(
    request: Request, 
    bg_tasks: BackgroundTasks, 
    form_data: Tuple[SignUpSch, dict] = Depends(SignUpSch.as_form), 
    user: dict = Depends(get_user_optional)
):
    if user:
        raise ServerErrorPageException("Auth", "You are already authenticated")
    data, form_errors = form_data
    if form_errors:
        return j2.TemplateResponse('signup.html', {"request": request, "form_errors": form_errors, "user": user})
    new_user, service_error = user_service.signup(data)
    if service_error:
        return j2.TemplateResponse('signup.html', {"request": request, "service_error": service_error, "user": user})
    if data.z_file:
        bg_tasks.add_task(upload_profile_img, new_user.get('pk'), data.z_file)
    return RedirectResponse('/signin', status.HTTP_303_SEE_OTHER)

@router.delete('/logout')
async def logout(request: Request):
    request.session.pop("user_pk", None)
    return "Logout success"

@router.get('/api/testing')
async def testing(message: str):
    enc_msg = encrypt_message(message)
    return {"message": enc_msg}

@router.get('/api/testing-2')
async def testing(message: str):
    users, err = user_service.get_all()
    print(err)
    return {"message": users}

