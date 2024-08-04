# Third-party
import secrets
from typing import Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

# Project
from logger import server_logger
import config as cf
from database import db
from .models import UserView, TicketView, PreferenceView, CategoryView, QuestionView

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=cf.server['secret_key'])
security = HTTPBasic()

admin = Admin(app=app, engine=db.engine)
[admin.add_view(view) for view in [
    UserView, TicketView, PreferenceView, CategoryView, QuestionView
]]


ADMIN = (cf.admin_panel['admin_name']).encode('utf8')
PASSWORD = (cf.admin_panel['password']).encode('utf8')


@app.get('/')
async def home(request: Request):
    return HTMLResponse(
        '<h1>ACCESS DENIED</h1>',
        status_code=status.HTTP_403_FORBIDDEN,
        media_type='text/html'
    )


def authenticate_user(credentials):
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, ADMIN
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, PASSWORD
    )
    if not (is_correct_username and is_correct_password):
        return False
    return True


@app.get('/admin')
async def admin_page(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    authorized = authenticate_user(credentials)
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return await admin.index(request)


@app.on_event("startup")
async def start_server():
    server_logger.info(f'Server started at http://{cf.server["host"]}:{cf.server["port"]}')


async def start_panel():
    from uvicorn import Config, Server
    config = Config(
        app=app,
        host='0.0.0.0',  # Do not change host, because it's running locally in docker container, not host machine
        port=int(cf.server['port'])
    )
    server = Server(config=config)
    await server.serve()
