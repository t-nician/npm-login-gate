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
    nginx_address = request.client.host
    client_address = request.headers.get("x-real-ip")
    
    if nginx_address != env.NGINX_HOST:
        return "Wait a second... who are you?"
    
    if await logic.is_timed_out(client_address):
        return "You are timed out!"
    
    if await logic.is_whitelisted(client_address):
        return "You are already whitelisted!"
    
    # TODO make this return an HTML page.
    return "Hello world!"


async def login_endpoint(body: LoginBody, request: Request):
    nginx_address = request.client.host
    client_address = request.headers.get("x-real-ip")
    
    if nginx_address != env.NGINX_HOST:
        return "Wait a second... who are you?"
    
    if await logic.is_timed_out(client_address):
        return "You are timed out!"
        
    if await logic.is_whitelisted(client_address):
        return "You are already whitelisted!"
    
    return await logic.attempt_login(client_address, body.password)


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