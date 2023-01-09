import logging
from types import NoneType
import requests
from typing import Optional, Union

logger = logging.getLogger(__name__)


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
    timeout: Optional[Union[float, tuple, NoneType]] = 60,
    verify: Optional[bool] = True,
):

    response = requests.post(
        url,
        json=payload,
        headers=HTTP_HEADERS,
        proxies=proxies,
        timeout=timeout,
    )

    try:
        response.raise_for_status()
    except Exception as Argument:
        logger.error("Webhook failed with status code: %s", response.status_code)
        logger.debug("Response Text: %s", response.text)
        logger.exception(Argument)

        if verify:
            raise TeamsWebhookException("HTTP call failed. See previous logging")

    return response.status_code


async def send_webhook_async(
    url: str,
    payload,
    # http_proxy: Optional[dict] = {},
    timeout: Optional[float] = 5.0,
    verify: Optional[bool] = True,
):

    if not ASYNC_OK:
        raise AsyncRequirementsMissing(
            "Missing python dependencies. Was pymsteams installed with the async option?"
        )

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            url,
            json=payload,
            headers=HTTP_HEADERS,
        )

    try:
        response.raise_for_status()
    except Exception as Argument:
        logger.error("Webhook failed with status code: %s", response.status_code)
        logger.debug("Response Text: %s", response.text)
        logger.exception(Argument)

        if verify:
            raise TeamsWebhookException("HTTP call failed. See previous logging")

        return False

    return True
