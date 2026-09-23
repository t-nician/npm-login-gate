import asyncio
import uvicorn

from gate import logic, model, env

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, Field


index_page = ""
with open("./src/index.html", "r") as file:
    index_page = file.read()


class LoginBody(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=256
    )


async def home_endpoint(request: Request):
    nginx_address = request.client.host    
    client_address = request.headers.get("x-real-ip")
    
    interrupt_message = await logic.gate(nginx_address, client_address)
    
    if interrupt_message:
        return interrupt_message
    
    nginx_url = request.headers.get("host")
    nginx_proto = request.headers.get("x-forwarded-proto")
    
    public_url = nginx_proto + "://" + nginx_url
    
    return index_page.replace("__ENDPOINT__", public_url)


async def login_endpoint(body: LoginBody, request: Request):
    nginx_address = request.client.host
    client_address = request.headers.get("x-real-ip")
    
    interrupt_message = await logic.gate(nginx_address, client_address)
        
    if interrupt_message:
        return interrupt_message
    
    return await logic.attempt_login(client_address, body.password)


def launch():
    app = FastAPI(
        lifespan=logic.lifespan
    )

    model.register_database(app)
    
    app.add_api_route("/", home_endpoint, methods=["GET"], response_class=HTMLResponse)
    app.add_api_route("/login", login_endpoint, methods=["POST"])
    
    uvicorn.run(
        app=app,
        host=env.LOGIN_PAGE_HOST,
        port=env.LOGIN_PAGE_PORT
    )