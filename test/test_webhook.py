import asyncio
import warnings
from unittest import TestCase
from unittest.mock import patch

import pytest
import requests_mock
from pymsteams.exceptions import AsyncRequirementsMissing, TeamsWebhookException
from pymsteams.webhook import send_webhook_async, send_webhook_sync
from pytest_httpx import HTTPXMock

FAKE_URL = "http://fakeurl.com"
FAKE_DATA = {"hi": "there"}


class TestSyncWebhook(TestCase):
    @requests_mock.Mocker()
    def test_valid_webhook(self, req_mock: requests_mock.mocker.Mocker):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        send_status = send_webhook_sync(FAKE_URL, FAKE_DATA)

        self.assertEqual(send_status, 200)

    @requests_mock.Mocker()
    def test_invalid_status(self, req_mock):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=500,
        )

        with self.assertRaises(TeamsWebhookException):
            send_webhook_sync(FAKE_URL, FAKE_DATA)


class TestAsyncWebhook(TestCase):
    def do_async_call(self, url: str, data):

        warnings.filterwarnings("ignore", category=DeprecationWarning)

        loop = asyncio.get_event_loop()

        loop.run_until_complete(send_webhook_async(url, data))

    @patch("pymsteams.webhook.ASYNC_OK", False)
    def test_missing_dependency(self):

        with self.assertRaises(AsyncRequirementsMissing):
            self.do_async_call(FAKE_URL, FAKE_DATA)


@pytest.mark.asyncio
async def test_simple_async(httpx_mock: HTTPXMock) -> None:

    httpx_mock.add_response(url=FAKE_URL)

    async_success = await send_webhook_async(FAKE_URL, FAKE_DATA)
    assert bool(async_success)


@pytest.mark.asyncio
async def test_simple_async_failure(httpx_mock: HTTPXMock) -> None:

    httpx_mock.add_response(url=FAKE_URL, status_code=500)

    with pytest.raises(TeamsWebhookException):
        _ = await send_webhook_async(FAKE_URL, FAKE_DATA)
