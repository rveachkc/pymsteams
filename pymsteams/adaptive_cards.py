import logging

from typing import Optional, Union
from types import NoneType


from pymsteams.templating.adaptive_card_base import adaptive_card_base
from pymsteams.webhook import send_webhook_sync


class AdaptiveCard:
    def __init__(
        self,
        webhook_url: str,
        proxies: Optional[dict] = {},
        timeout: Optional[Union[float, tuple, NoneType]] = 60,
        verify: Optional[bool] = True,
    ):

        self.log = logging.getLogger(__name__)
        self.webhook_url = webhook_url
        self.proxies = self.proxies
        self.timeout = self.timeout
        self.verify = self.verify

    def send_card_content(
        self,
        content: dict,
        contentUrl: Optional[str] = None,
        alternate_url: Optional[str] = "",
    ):

        if alternate_url:
            url = alternate_url
            self.log.debug("Sending card content to alterate url")
        else:
            url = self.webhook_url
            self.log.debug("Sending webhook to class webhook url")

        send_webhook_sync(
            url,
            payload=adaptive_card_base(content=content, contentUrl=contentUrl),
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.verify,
        )
