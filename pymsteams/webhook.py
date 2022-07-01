import requests
from typing import Optional


try:
    import httpx

    ASYNC_OK = True
except ImportError:
    ASYNC_OK = False

from pymsteams.exceptions import TeamsWebhookException, AsyncRequirementsMissing

HTTP_HEADERS = {"Content-Type": "application/json"}


def send_webhook_sync(
    url: str,
    payload,
    proxies: Optional[dict] = {},
    timeout: Optional[int] = 60,
    verify: Optional[bool] = None,
):

    response = requests.post(
        url,
        json=payload,
        headers=HTTP_HEADERS,
        proxies=proxies,
    )

    if response.status_code != requests.codes.ok:
        raise TeamsWebhookException(response.text)

    return response.status_code


async def send_webhook_async(
    url: str,
    payload,
    # http_proxy: Optional[dict] = {},
    timeout: Optional[int] = 60,
    verify: Optional[bool] = None,
):

    if not ASYNC_OK:
        raise AsyncRequirementsMissing(
            "Missing python dependencies. Was pymsteams installed with the async option?"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=payload,
            headers=HTTP_HEADERS,
        )

        if response.status_code != requests.codes.ok:
            raise TeamsWebhookException(response.text)

        return True
