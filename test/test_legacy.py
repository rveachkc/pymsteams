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

    CARD_TITLE = "This is a message Title"
    CARD_TEXT = "this is a message text field"

    @requests_mock.Mocker()
    def test_send_message(self, req_mock: requests_mock.mocker.Mocker):
        """
        Create a basic message, send it, and validate payload

        Expected payload:
        {
            'potentialAction': [
                {
                    '@context': 'http://schema.org',
                    '@type': 'ViewAction',
                    'name': 'Go to the Repo',
                    'target': ['https://github.com/rveachkc/pymsteams'],
                }
            ],
            'text': 'this is a message text field',
            'title': 'This is a message Title'}
        """

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        button_text = "Go to the Repo"
        button_url = "https://github.com/rveachkc/pymsteams"

        teams_message = pymsteams.connectorcard(FAKE_URL)
        teams_message.text(self.CARD_TEXT)
        teams_message.title(self.CARD_TITLE)
        teams_message.addLinkButton(button_text, button_url)
        teams_message.send()

        self.assertEqual(teams_message.last_http_response, 200)

        self.assertEqual(teams_message.payload.get("text"), self.CARD_TEXT)
        self.assertEqual(teams_message.payload.get("title"), self.CARD_TITLE)

        self.assertTrue("potentialAction" in teams_message.payload.keys())
        self.assertIsInstance(teams_message.payload.get("potentialAction"), list)
        self.assertEqual(len(teams_message.payload.get("potentialAction")), 1)

        self.assertEqual(
            teams_message.payload.get("potentialAction", [])[0].get("name"),
            button_text,
        )
        self.assertEqual(
            teams_message.payload.get("potentialAction", [])[0].get("target")[0],
            button_url,
        )

    @requests_mock.Mocker()
    def test_send_chained_message(self, req_mock: requests_mock.mocker.Mocker):
        """
        This is a copy of test_send_message, using chained methods

        Expected payload:
        {
            'potentialAction': [
                {
                    '@context': 'http://schema.org',
                    '@type': 'ViewAction',
                    'name': 'Go to the Repo',
                    'target': ['https://github.com/rveachkc/pymsteams'],
                }
            ],
            'text': 'this is a message text field',
            'title': 'This is a message Title'}
        """

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        button_text = "Go to the Repo"
        button_url = "https://github.com/rveachkc/pymsteams"

        teams_message = (
            pymsteams.connectorcard(FAKE_URL)
            .text(self.CARD_TEXT)
            .title(self.CARD_TITLE)
            .addLinkButton(button_text, button_url)
            .send()
        )

        self.assertEqual(teams_message.last_http_response, 200)

        self.assertEqual(teams_message.payload.get("text"), self.CARD_TEXT)
        self.assertEqual(teams_message.payload.get("title"), self.CARD_TITLE)

        self.assertTrue("potentialAction" in teams_message.payload.keys())
        self.assertIsInstance(teams_message.payload.get("potentialAction"), list)
        self.assertEqual(len(teams_message.payload.get("potentialAction")), 1)

        self.assertEqual(
            teams_message.payload.get("potentialAction", [])[0].get("name"),
            button_text,
        )
        self.assertEqual(
            teams_message.payload.get("potentialAction", [])[0].get("target")[0],
            button_url,
        )

    @requests_mock.Mocker()
    def test_status_500(self, req_mock: requests_mock.mocker.Mocker):

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

    @requests_mock.Mocker()
    def test_status_403(self, req_mock: requests_mock.mocker.Mocker):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=403,
        )

        teams_message = pymsteams.connectorcard(FAKE_URL)
        teams_message.text("This is a simple text message.")

        with self.assertRaises(pymsteams.exceptions.TeamsWebhookException):
            teams_message.send()

    @requests_mock.Mocker()
    def test_bad_resp_text(self, req_mock: requests_mock.mocker.Mocker):

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="not cool",
            status_code=200,
        )

        teams_message = pymsteams.connectorcard(FAKE_URL)
        teams_message.text("This is a simple text message.")

        with self.assertRaises(pymsteams.exceptions.TeamsWebhookException):
            teams_message.send()

    @requests_mock.Mocker()
    def test_sectioned_message(self, req_mock: requests_mock.mocker.Mocker):
        """
        Send a message with sections

        Expected payload:
        {
            'sections': [
                {
                    'activityImage': 'https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_1.jpg',
                    'activitySubtitle': 'my activity subtitle 1',
                    'activityText': 'section 1 activity text',
                    'activityTitle': 'my activity title 1',
                    'facts': [
                        {
                            'name': 'Fact 1',
                            'value': 'Penguins are cool'
                        },
                        {'name': 'Fact 2', 'value': 'polar bears are also cool'}
                    ],
                    'title': 'This is section 1'
                },
                {
                    'images': [
                        {
                            'image': 'https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_2.jpg',
                            'title': 'Pew Pew Pew'
                        }
                    ],
                    'text': 'This is section 2'
                }
            ],
            'text': 'this is a message text field',
            'title': 'This is a message Title'
        }
        """

        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        section_1_title = "This is section 1"
        section_1_activity_title = "my activity title 1"
        section_1_activity_subtitle = "my activity subtitle 1"
        section_1_activity_image = "https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_1.jpg"
        section_1_activity_text = "section 1 activity text"
        fact_1_key = "Fact 1"
        fact_1_value = "Penguins are cool"
        fact_2_key = "Fact 2"
        fact_2_value = "polar bears are also cool"

        section_1 = (
            pymsteams.cardsection()
            .title(section_1_title)
            .activityTitle(section_1_activity_title)
            .activitySubtitle(section_1_activity_subtitle)
            .activityImage(section_1_activity_image)
            .activityText(section_1_activity_text)
            .addFact(fact_1_key, fact_1_value)
            .addFact(fact_2_key, fact_2_value)
        )

        section_2_text = "This is section 2"
        section_2_image = "https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_2.jpg"
        section_2_ititle = "Pew Pew Pew"

        section_2 = (
            pymsteams.cardsection()
            .text(section_2_text)
            .addImage(section_2_image, ititle=section_2_ititle)
        )

        teams_message = (
            pymsteams.connectorcard(FAKE_URL)
            .text(self.CARD_TEXT)
            .title(self.CARD_TITLE)
            .addSection(section_1)
            .addSection(section_2)
        )

        teams_message.send()
        self.assertEqual(teams_message.last_http_response, 200)

        self.assertEqual(teams_message.payload.get("text"), self.CARD_TEXT)
        self.assertEqual(teams_message.payload.get("title"), self.CARD_TITLE)

        self.assertIn("sections", teams_message.payload.keys())
        self.assertIsInstance(teams_message.payload.get("sections"), list)
        self.assertEqual(len(teams_message.payload.get("sections")), 2)

        section_1_pl = teams_message.payload.get("sections")[0]
        self.assertEqual(section_1_pl.get("activityImage"), section_1_activity_image)
        self.assertEqual(
            section_1_pl.get("activitySubtitle"), section_1_activity_subtitle
        )
        self.assertEqual(section_1_pl.get("activityText"), section_1_activity_text)
        self.assertEqual(section_1_pl.get("activityTitle"), section_1_activity_title)

        self.assertIn("facts", section_1_pl.keys())
        facts_pl = section_1_pl.get("facts")
        self.assertIsInstance(facts_pl, list)
        self.assertEqual(len(facts_pl), 2)
        self.assertEqual(facts_pl[0].get("name"), fact_1_key)
        self.assertEqual(facts_pl[0].get("value"), fact_1_value)
        self.assertEqual(facts_pl[1].get("name"), fact_2_key)
        self.assertEqual(facts_pl[1].get("value"), fact_2_value)

        section_2_pl = teams_message.payload.get("sections")[1]
        self.assertEqual(section_2_pl.get("text"), section_2_text)
        self.assertIsInstance(section_2_pl.get("images"), list)
        self.assertEqual(len(section_2_pl.get("images")), 1)
        self.assertEqual(section_2_pl.get("images")[0].get("image"), section_2_image)
        self.assertEqual(section_2_pl.get("images")[0].get("title"), section_2_ititle)

    @requests_mock.Mocker()
    def test_send_potential_action(self, req_mock: requests_mock.mocker.Mocker):
        """
        Send a message with a potential action
        """
        req_mock.register_uri(
            "POST",
            FAKE_URL,
            text="1",
            status_code=200,
        )

        placeholder_url = "https://jsonplaceholder.typicode.com/posts"

        action1 = (
            pymsteams.potentialaction("Action1")
            .addInput("TextInput", "input1", "Input Title 1", False)
            .addAction("HttpPost", "Add Comment", placeholder_url)
        )

        action2 = (
            pymsteams.potentialaction("Action2")
            .addInput("DateInput", "dueDate", "Enter a date")
            .addAction("HttpPost", "save", placeholder_url)
        )

        action3 = pymsteams.potentialaction("Action3")
        action3.choices.addChoices("Choice 1", "1").addChoices("Choice 2", "2")
        action3.addInput(
            "MultichoiceInput", "list", "Select a status", False
        ).addAction("HttpPost", "Save", placeholder_url)

        action4 = pymsteams.potentialaction("Download pymsteams").addOpenURI(
            "Links",
            [
                {
                    "os": "default",
                    "uri": "https://pypi.org/project/pymsteams/",
                }
            ],
        )

        msg = (
            pymsteams.connectorcard(FAKE_URL)
            .title(self.CARD_TITLE)
            .text(self.CARD_TEXT)
            .addPotentialAction(action1)
            .addPotentialAction(action2)
            .addPotentialAction(action3)
            .addPotentialAction(action4)
            .send()
        )

        self.assertEqual(msg.last_http_response, 200)

        self.assertEqual(msg.payload.get("text"), self.CARD_TEXT)
        self.assertEqual(msg.payload.get("title"), self.CARD_TITLE)

        self.assertIn("potentialAction", msg.payload.keys())
        self.assertIsInstance(msg.payload.get("potentialAction"), list)
        self.assertEqual(len(msg.payload.get("potentialAction")), 4)

        for action_num, action_pl in enumerate(
            msg.payload.get("potentialAction"), start=1
        ):

            if action_num in {1, 2, 3}:
                self.assertEqual(action_pl.get("@type"), "ActionCard")
                self.assertIn("inputs", action_pl.keys())
                self.assertIsInstance(action_pl.get("inputs"), list)
                self.assertEqual(action_pl.get("name"), f"Action{action_num}")

                action_action_pl = action_pl.get("actions")
                action_input_pl = action_pl.get("inputs")

                if action_num == 1:
                    self.assertEqual(
                        action_action_pl,
                        [
                            {
                                "@type": "HttpPost",
                                "name": "Add Comment",
                                "target": placeholder_url,
                            }
                        ],
                    )

                    self.assertEqual(
                        action_input_pl,
                        [
                            {
                                "@type": "TextInput",
                                "id": "input1",
                                "isMultiline": False,
                                "title": "Input Title 1",
                            }
                        ],
                    )

                elif action_num == 2:
                    self.assertEqual(
                        action_action_pl,
                        [
                            {
                                "@type": "HttpPost",
                                "name": "save",
                                "target": placeholder_url,
                            }
                        ],
                    )

                    self.assertEqual(
                        action_input_pl,
                        [
                            {
                                "@type": "DateInput",
                                "id": "dueDate",
                                "isMultiline": None,
                                "title": "Enter a date",
                            }
                        ],
                    )

                elif action_num == 3:

                    self.assertEqual(
                        action_action_pl,
                        [
                            {
                                "@type": "HttpPost",
                                "name": "Save",
                                "target": placeholder_url,
                            }
                        ],
                    )

                    self.assertEqual(
                        action_input_pl,
                        [
                            {
                                "@type": "MultichoiceInput",
                                "choices": [
                                    {"display": "Choice 1", "value": "1"},
                                    {"display": "Choice 2", "value": "2"},
                                ],
                                "id": "list",
                                "isMultiline": "false",
                                "title": "Select a status",
                            }
                        ],
                    )

            elif action_num == 4:
                self.assertEqual(action_pl.get("@type"), "OpenUri")
                self.assertEqual(action_pl.get("name"), "Links")
                self.assertEqual(
                    action_pl.get("targets"),
                    [{"os": "default", "uri": "https://pypi.org/project/pymsteams/"}],
                )
