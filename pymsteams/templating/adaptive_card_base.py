from typing import Optional


def adaptive_card_base(content: dict, contentUrl: Optional[str] = None):

    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": contentUrl,
                "content": content,
            }
        ],
    }
