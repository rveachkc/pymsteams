import asyncio
import os

import pymsteams


def test_async_send_message():
    """
    This asynchronously send a simple text message with a title and link button.
    """

    _ = asyncio.get_event_loop()

    teams_message = pymsteams.async_connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    teams_message.text("This is a simple text message.")
    teams_message.title("Simple Message Title")
    teams_message.addLinkButton(
        "Go to the Repo", "https://github.com/rveachkc/pymsteams"
    )
    # loop.run_until_complete(teams_message.send())

    # assert isinstance(teams_message.last_http_response.status_code, int)
