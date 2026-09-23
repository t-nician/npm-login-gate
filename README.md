# npm-login-gate

A small Python web server that sits in front of services protected by [Nginx Proxy Manager](https://nginxproxymanager.com/) access lists.

It serves a simple password page. When the correct password is entered, the visitor’s IP is temporarily added to a chosen NPM access list. After a configurable lifetime the IP is removed again.

Useful when you want self-service temporary access without giving people permanent whitelist entries or full NPM credentials.

![Preview](https://github.com/t-nician/npm-login-gate/blob/main/.img/preview.png)

## Features

- Password-protected login page
- Temporary IP allowlisting via the NPM API
- Configurable whitelist duration
- Rate limiting / temporary timeout after failed attempts
- Optional Discord-compatible webhooks for success, failure, and timeout events
- Only accepts requests that come through a trusted Nginx host (via `X-Real-IP`)

## How it works

1. User visits the login page (proxied through Nginx Proxy Manager).
2. They enter the shared password.
3. On success the server:
   - Logs into Nginx Proxy Manager with the configured account
   - Adds the client’s IP (`X-Real-IP`) to the named access list with an `allow` directive
   - Stores the IP locally so it can be removed later
4. A background task periodically refreshes the NPM token and removes expired whitelist / timeout entries.

## Requirements

- Python 3.10+
- A running Nginx Proxy Manager instance
- An NPM access list that your protected hosts already use
- The login-gate service reachable only through Nginx (so the real client IP is passed via `X-Real-IP`)

## Installation

```bash
git clone https://github.com/t-nician/npm-login-gate.git
cd npm-login-gate

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

# Edit .env file.

python src/main.py
```


## Environment variables.
⚠️ it is recommended to create a separate NPM account to manage the access list! ⚠️
| Variable                                                     | Description                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| LOGIN_PAGE_HOST                                              | Bind address (default 0.0.0.0)                                |
| LOGIN_PAGE_PORT                                              | Port the server listens on (default 8000)                     |
| NGINX_HOST                                                   | IP of the Nginx instance that is allowed to forward X-Real-IP |
| NPM_URL                                                      | Base URL of Nginx Proxy Manager (e.g. http://192.168.1.10:81) - https recommended.|
| NPM_ACCOUNT_EMAIL                                            | NPM admin / user email                                        |
| NPM_ACCOUNT_PASSWORD                                         | NPM password                                                  |
| NPM_ACCESS_LIST_NAME                                         | Exact name of the access list to modify                       |
| LOGIN_PASSWORD                                               | Shared password users must enter                              |
| LOGIN_LIFETIME                                               | How long (hours) an IP stays on the access list               |
| LOGIN_MAX_ATTEMPTS                                           | Failed attempts before a temporary timeout                    |
| LOGIN_FAIL_TIMEOUT                                           | Timeout duration in minutes after too many failures           |
| LOGIN_CHECK_DATABASE_INTERVAL | How often it will check the database for expired timeouts & whitelists.                      |
| WEBHOOK_URL                                                  | Optional webhook URL (works with Discord)                     |
| WEBHOOK_ON_SUCCESS / WEBHOOK_ON_FAILURE / WEBHOOK_ON_TIMEOUT | "true" / "false"                                              |
| WEBHOOK_SUCCESS_MESSAGE etc.                                 | Message templates; {} is replaced with the IP                 |

