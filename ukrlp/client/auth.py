import os

import requests
from dotenv import load_dotenv


def fetch_access_token_from_env():
    load_dotenv(override=True)

    user_agent = os.getenv("HTTP_USER_AGENT", "").strip()
    token_url = os.getenv("OAUTH_TOKEN_URL", "").strip()
    client_id = os.getenv("OAUTH_CLIENT_ID", "").strip()
    client_secret = os.getenv("OAUTH_CLIENT_SECRET", "").strip()
    scope = os.getenv("OAUTH_SCOPE", "").strip()

    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        },
        headers={"Accept": "application/json", "User-Agent": user_agent},
        timeout=60,
    )
    response.raise_for_status()

    token = response.json().get("access_token", "")
    return token, user_agent
