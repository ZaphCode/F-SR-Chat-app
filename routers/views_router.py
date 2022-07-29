from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Views"])
j2 = Jinja2Templates(directory='public/templates')

@router.get('/', response_class=HTMLResponse)
async def index_page(request: Request):
    return j2.TemplateResponse('index.html', {"request": request})

@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return j2.TemplateResponse('login.html', {"request": request})

@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return j2.TemplateResponse('register.html', {"request": request})
