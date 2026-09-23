import os
import dotenv

dotenv.load_dotenv(
    dotenv_path=".env",
    override=False
)


# Only accept forwarded IPs from this host.
NGINX_HOST = os.getenv("NGINX_HOST")


# Nginx Proxy Manager parameters.
NPM_URL = os.getenv("NPM_URL").removesuffix("/")

NPM_ACCOUNT_EMAIL = os.getenv("NPM_ACCOUNT_EMAIL")
NPM_ACCOUNT_PASSWORD = os.getenv("NPM_ACCOUNT_PASSWORD")

NPM_ACCESS_LIST_NAME = os.getenv("NPM_ACCESS_LIST_NAME")

NPM_ENDPOINT_GET_TOKEN = NPM_URL + "/api/tokens"
NPM_ENDPOINT_GET_ACCESS_LISTS = NPM_URL + "/api/nginx/access-lists?expand=owner%2Citems%2Cclients"

NPM_ENDPOINT_PUT_ACCESS_LIST = NPM_URL + "/api/nginx/access-lists/{}"


# Login page configuration.
LOGIN_PAGE_HOST = os.getenv("LOGIN_PAGE_HOST")
LOGIN_PAGE_PORT = int(os.getenv("LOGIN_PAGE_PORT"))

LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")


# Login attempt limitation configuration.
LOGIN_LIFETIME = int(os.getenv("LOGIN_LIFETIME"))

LOGIN_MAX_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS"))
LOGIN_FAIL_TIMEOUT = int(os.getenv("LOGIN_FAIL_TIMEOUT"))


# Webhook configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

WEBHOOK_ON_SUCCESS = os.getenv("WEBHOOK_ON_SUCCESS").lower() == "true"
WEBHOOK_ON_FAILURE = os.getenv("WEBHOOK_ON_FAILURE").lower() == "true"
WEBHOOK_ON_TIMEOUT = os.getenv("WEBHOOK_ON_TIMEOUT").lower() == "true"

WEBHOOK_SUCCESS_MESSAGE = os.getenv("WEBHOOK_SUCCESS_MESSAGE")
WEBHOOK_FAILURE_MESSAGE = os.getenv("WEBHOOK_FAILURE_MESSAGE")
WEBHOOK_TIMEOUT_MESSAGE = os.getenv("WEBHOOK_TIMEOUT_MESSAGE")