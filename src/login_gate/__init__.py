import os
import uvicorn

from login_gate.server import create_app


def launch():
    uvicorn.run(
        app=create_app(),
        host=os.getenv("PAGE_HOST"),
        port=int(os.getenv("PAGE_PORT"))
    )