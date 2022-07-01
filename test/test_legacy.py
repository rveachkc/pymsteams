import os
import sys
import pytest
from unittest import TestCase

import requests_mock


# add scripts to the path
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

import pymsteams

# from pytest_mock import mocker
import pytest

FAKE_URL = "http://127.0.0.1:3456"
FAKE_DATA = {"hi": "there"}


class TestLegacyCards(TestCase):
    @requests_mock.Mocker()
    def test_send_message(self, req_mock: requests_mock.mocker.Mocker):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        teams_message = pymsteams.connectorcard(FAKE_URL)
        teams_message.text("This is a simple text message.")
        teams_message.title("Simple Message Title")
        teams_message.addLinkButton(
            "Go to the Repo", "https://github.com/rveachkc/pymsteams"
        )
        teams_message.send()

        self.assertEqual(teams_message.last_http_response, 200)

        # TODO: add data validation

    @requests_mock.Mocker()
    def test_failed_send(self, req_mock: requests_mock.mocker.Mocker):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=500,
        )

        teams_message = pymsteams.connectorcard(FAKE_URL)
        teams_message.text("This is a simple text message.")

        with self.assertRaises(pymsteams.exceptions.TeamsWebhookException):
            teams_message.send()
