from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.views_router import router as views_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='public/static'), 'static')

app.include_router(views_router)