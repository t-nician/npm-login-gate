import uvicorn

from gate import logic, model, env

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field


class LoginBody(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=256
    )


async def home_endpoint(request: Request):
    pass


async def login_endpoint(body: LoginBody, request: Request):
    pass


def launch():
    app = FastAPI()

    model.register_database(app)
    
    app.add_api_route("/", home_endpoint, methods=["GET"])
    app.add_api_route("/login", login_endpoint, methods=["POST"])
    
    uvicorn.run(
        app=app,
        host=env.LOGIN_PAGE_HOST,
        port=env.LOGIN_PAGE_PORT
    )