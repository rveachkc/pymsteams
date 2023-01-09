import asyncio
import os
import sys
from unittest import TestCase, IsolatedAsyncioTestCase

# add scripts to the path
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import pymsteams
import pprint

FAKE_URL = "http://127.0.0.1:3456"
CARD_TEXT = "This is my card text"


class TestAsyncCard(IsolatedAsyncioTestCase):
    async def test_async_message(self):

        msg = pymsteams.async_connectorcard(FAKE_URL).text(CARD_TEXT)
        pprint.pprint(msg.payload)
        self.assertEqual(msg.payload, {"text": "This is my card text"})

        # result = await msg.send()

        # pprint.pprint(result)
