from unittest import TestCase
from pymsteams.templating.simple_card import simple_card


class TestSimpleCard(TestCase):

    SAMPLE_TITLE_TEXT = "This is my title"
    SAMPLE_BODY_TEXT = "This is my text"

    URL1_TITLE = "url1"
    URL1_URL = "http://127.0.0.1"

    URL2_TITLE = "url2"
    URL2_URL = "http://localhost"

    def validate_common_card_elements(self, card: dict, has_actions=False):

        for i in ("type", "attachments"):
            self.assertIn(i, card.keys())

        self.assertIsInstance(card["attachments"], list)

        first_attachment = card.get("attachments", [])[0]
        self.assertIsInstance(first_attachment, dict)

        for i in ("contentType", "contentUrl", "content"):
            self.assertIn(i, first_attachment.keys())

        content = first_attachment.get("content", {})

        for i in ("type", "body", "$schema", "version"):
            self.assertIn(i, content.keys())

        if has_actions:
            self.assertIn("actions", content.keys())
        else:
            self.assertNotIn("actions", content.keys())

        return content

    def test_text_only(self):

        card = simple_card(self.SAMPLE_BODY_TEXT)

        card_content = self.validate_common_card_elements(card)

        self.assertEqual(len(card_content.get("body", [])), 1)

        text_content = card_content.get("body", [])[0]

        self.assertEqual(text_content.get("text"), self.SAMPLE_BODY_TEXT)

        self.assertNotIn("actions", card_content.keys())

    def test_text_and_body(self):

        card = simple_card(
            body_text=self.SAMPLE_BODY_TEXT, title_text=self.SAMPLE_TITLE_TEXT
        )

        card_content = self.validate_common_card_elements(card)

        self.assertEqual(len(card_content.get("body", [])), 2)

        title_content = card_content.get("body", [])[0]
        self.assertEqual(title_content.get("text"), self.SAMPLE_TITLE_TEXT)

        text_content = card_content.get("body", [])[1]
        self.assertEqual(text_content.get("text"), self.SAMPLE_BODY_TEXT)

    def test_w_one_url(self):

        card = simple_card(
            body_text=self.SAMPLE_BODY_TEXT,
            title_text=self.SAMPLE_TITLE_TEXT,
            action_urls=[(self.URL1_TITLE, self.URL1_URL)],
        )

        card_content = self.validate_common_card_elements(card, has_actions=True)

        card_actions = card_content.get("actions")
        self.assertEqual(len(card_actions), 1)
        self.assertIsInstance(card_actions, list)

        first_url = card_actions[0]
        self.assertIsInstance(first_url, dict)
        self.assertEqual(first_url.get("title"), self.URL1_TITLE)
        self.assertEqual(first_url.get("url"), self.URL1_URL)

    def test_w_two_urls(self):

        card = simple_card(
            body_text=self.SAMPLE_BODY_TEXT,
            title_text=self.SAMPLE_TITLE_TEXT,
            action_urls=[
                (self.URL1_TITLE, self.URL1_URL),
                (self.URL2_TITLE, self.URL2_URL),
            ],
        )

        card_content = self.validate_common_card_elements(card, has_actions=True)

        card_actions = card_content.get("actions")

        self.assertEqual(card_actions[0].get("title"), self.URL1_TITLE)
        self.assertEqual(card_actions[1].get("title"), self.URL2_TITLE)
