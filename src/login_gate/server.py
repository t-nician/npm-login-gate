import os


LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")


from fastapi import FastAPI, Request
from pydantic import BaseModel, Field


tracked_attempts = {}
is_approved = {}


class LoginBody(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=256
    )
    

async def is_timed_out(ip: str):
    return False


async def home_endpoint(request: Request):
    if await is_timed_out(request.client.host):
        return "You are timed out for {} minutes!".format(
            os.getenv("LOGIN_FAIL_TIMEOUT")
        )
    
    return "Hello world!"


async def login_endpoint(body: LoginBody, request: Request):
    client_ip = request.client.host
    
    if await is_timed_out(client_ip):
        return "You are timed out for {} minutes!".format(
            os.getenv("LOGIN_FAIL_TIMEOUT")
        )
    
    password = body.password
    
    if password == LOGIN_PASSWORD:
        pass
    else:
        

    return "Hello world!"


def create_app():
    app = FastAPI()
    
    app.add_api_route("/", home_endpoint, methods=["GET"])
    app.add_api_route("/login", login_endpoint, methods=["POST"])
    
    return app