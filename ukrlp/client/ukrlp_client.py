import json
import os
from collections.abc import Iterator

import requests
from dotenv import load_dotenv

from client.auth import fetch_access_token_from_env
from client.models import ProviderRecord, ProvidersResponse


def stream_providers(
    page_number: int = 1,
    page_size: int = 5,
    updated_since: str | None = None,
    base_url: str | None = None,
    subscription_key: str | None = None,
    access_token: str | None = None,
    user_agent: str | None = None,
) -> Iterator[ProvidersResponse]:
    load_dotenv(override=True)

    if not base_url:
        base_url = os.getenv("API_BASE_URL", "").rstrip("/")
    if subscription_key is None:
        subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY", "")
    if not access_token or user_agent is None:
        access_token, user_agent = fetch_access_token_from_env()

    params = {"PageNumber": page_number, "PageSize": page_size}
    if updated_since:
        params["UpdatedSince"] = updated_since

    response = requests.get(
        f"{base_url}/api/providers",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Accept": "application/x-ndjson, application/json",
            "User-Agent": user_agent,
        },
        params=params,
        stream=True,
        timeout=120,
    )
    response.raise_for_status()

    for raw_line in response.iter_lines(decode_unicode=True):
        if raw_line:
            payload = json.loads(raw_line)
            yield ProvidersResponse.from_dict(payload)


def stream_provider_records(
    page_number: int = 1,
    page_size: int = 5,
    updated_since: str | None = None,
    base_url: str | None = None,
    subscription_key: str | None = None,
    access_token: str | None = None,
    user_agent: str | None = None,
) -> Iterator[ProviderRecord]:
    for payload in stream_providers(
        page_number=page_number,
        page_size=page_size,
        updated_since=updated_since,
        base_url=base_url,
        subscription_key=subscription_key,
        access_token=access_token,
        user_agent=user_agent,
    ):
        for record in payload.MatchingProviderRecords:
            yield record
