from typing import Optional, Iterable, Tuple

from pymsteams.templating.adaptive_card_base import adaptive_card_base
from pymsteams.templating.body_elements import (
    fmt_title_text,
    fmt_body_text,
    fmt_url_actions,
)
from pymsteams.templating.constants import *


def simple_card(
    body_text: str,
    title_text: Optional[str] = "",
    contentUrl: Optional[str] = None,
    action_urls: Optional[Iterable[Tuple[str, str]]] = [],
):

    body_elements = []

    if title_text:
        body_elements.append(fmt_title_text(title_text))

    body_elements.append(fmt_body_text(body_txt=body_text))

    card_content = {
        "type": "AdaptiveCard",
        "body": body_elements,
        "$schema": ADAPTIVE_CARD_SCHEMA,
        "version": ADAPTIVE_CARD_VERSION_STR,
    }

    if action_urls:
        card_content["actions"] = fmt_url_actions(action_urls)

    return adaptive_card_base(
        content=card_content,
        contentUrl=contentUrl,
    )
