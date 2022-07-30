from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from lib.exceptions import ServerErrorPageException, RequiresLoginException
from routers.views_router import j2, router as views_router
from starlette.middleware.sessions import SessionMiddleware
from redis_om import Migrator
import cloudinary
import config

cloudinary.config( 
  cloud_name = config.cloudinary_db_name, 
  api_key = config.cloudinary_api_key, 
  api_secret = config.cloudinary_secret_key 
)

app = FastAPI(
    title="Chat APP - Zaph",
    description="Simple chat app with FastAPI, Redis Stack, Cloudinary and Tailwind",
    version="1.1",
)

app.add_middleware(
    SessionMiddleware, 
    secret_key = config.session_secret, 
    session_cookie = 'z-session', 
    max_age = 259200 # 3 days
)

app.mount('/static', StaticFiles(directory='public/static'), 'static')

#* Exception Handlers
@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    return RedirectResponse('/login', status.HTTP_307_TEMPORARY_REDIRECT)

@app.exception_handler(ServerErrorPageException)
async def exception_handler(request: Request, exc: ServerErrorPageException):
    return j2.TemplateResponse(
        'error.html', 
        {
            "request": request, 
            "error_type": exc.error_type,
            "error_msg": exc.error_msg,
            "error_code": exc.error_code
        }
    )

@app.exception_handler(404)
async def exception_handler(request: Request, exc):
    return j2.TemplateResponse('not_found.html', {"request": request})

@app.on_event('startup')
async def startup():
    Migrator().run()
    print("Server start!")

app.include_router(views_router)