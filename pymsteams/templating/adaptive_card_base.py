from typing import Optional


def adaptive_card_base(content: dict, contentUrl: Optional[str] = None):

    card_base = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": contentUrl,
                "content": content,
            }
        ],
    }

    return card_base
