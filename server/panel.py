# Third-party
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

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


# Define a function to check credentials
def authenticate_user(username: str, password: str):
    # Replace with your actual authentication logic (e.g., checking against a database)
    authorized_users = {
        "admin": "password123"  # Example user:password pair
    }
    if username in authorized_users and authorized_users[username] == password:
        return True
    return False

@app.get('/admin')
async def admin_page(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    authorized = authenticate_user(credentials.username, credentials.password)
    if not authorized:
        raise HTTPException(status_code=401, detail="Unauthorized")
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
