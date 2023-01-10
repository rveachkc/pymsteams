import logging

from typing import Optional, Union, Iterable, Tuple
from types import NoneType


from pymsteams.templating.adaptive_card_base import adaptive_card_base
from pymsteams.templating.simple_card import simple_card
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

    def send_raw_json(
        self,
        data: dict,
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
            data=data,
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.verify,
        )

    def send_card_content(
        self,
        content: dict,
        contentUrl: Optional[str] = None,
        alternate_url: Optional[str] = "",
    ):

        self.send_raw_json(
            data=adaptive_card_base(content=content, contentUrl=contentUrl),
            alternate_url=alternate_url,
        )

    def send_simple_card(
        self,
        body_text: str,
        title_text: Optional[str] = "",
        contentUrl: Optional[str] = None,
        action_urls: Optional[Iterable[Tuple[str, str]]] = [],
        alternate_url: Optional[str] = "",
    ):

        self.send_raw_json(
            data=simple_card(
                body_text=body_text,
                title_text=title_text,
                contentUrl=contentUrl,
                action_urls=action_urls,
            ),
            alternate_url=alternate_url,
        )
