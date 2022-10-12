from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from lib.event_handlers import shutdown_handler, startup_handler
from lib.exceptions import ServerErrorPageException, RequiresSignInException
from lib.exception_handlers import internal_err_handler, requeries_login_exc_handler, server_error_page_exc_handler, not_found_exc_handler
from routers.views_router import router as views_router
from routers.ws_router import router as ws_router
from routers.chat_router import router as chat_router
from routers.auth_router import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import config
import uvicorn


#* Initialization
app = FastAPI(
    title="Chat APP - Zaph",
    description="Simple chat app with FastAPI, Redis Stack, Cloudinary and Tailwind",
    version="1.1",
)

#* Middlewares
app.add_middleware(
    SessionMiddleware, 
    secret_key = config.session_secret, 
    session_cookie = 'z-session',
    same_site="strict",
    https_only=True,
    max_age = 259200 # 3 days
)

origins = [
    "http://localhost",
    "http://localhost:8500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#* Settings
app.mount('/static', StaticFiles(directory='public/static'), 'static')

#* Exception Handlers
app.add_exception_handler(RequiresSignInException, requeries_login_exc_handler)
app.add_exception_handler(ServerErrorPageException, server_error_page_exc_handler)
app.add_exception_handler(404, not_found_exc_handler)
app.add_exception_handler(500, internal_err_handler)

#* Events handlers
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

#* Routers
app.include_router(router = views_router)
app.include_router(router = ws_router)
app.include_router(router = auth_router)
app.include_router(router = chat_router)

#* Run
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=config.port, 
        reload=config.debugging, 
        debug=config.debugging,
    )