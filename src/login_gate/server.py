import os
import time

LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
LOGIN_MAX_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS"))
LOGIN_FAIL_TIMEOUT = int(os.getenv("LOGIN_FAIL_TIMEOUT"))

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field


tracked_attempts = {}
timed_out_clients = {}

approved_clients = {}


class LoginBody(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=256
    )
    

async def is_timed_out(ip: str):
    return timed_out_clients.get(ip) != None


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
        current_attempts = tracked_attempts.get(client_ip)
        
        if not current_attempts:
            tracked_attempts[client_ip] = 1
        else:
            tracked_attempts[client_ip] = tracked_attempts[client_ip] + 1
        
        if tracked_attempts[client_ip] >= LOGIN_MAX_ATTEMPTS:
            timed_out_clients[client_ip] = int(time.time()) + LOGIN_FAIL_TIMEOUT * 60
            return "You have been timed out!"
        
        return "Incorrect password!"

    return "Hello world!"


def create_app():
    app = FastAPI()
    
    app.add_api_route("/", home_endpoint, methods=["GET"])
    app.add_api_route("/login", login_endpoint, methods=["POST"])
    
    return app