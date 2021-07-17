import asyncio
import os
import sys
import pytest

# add scripts to the path
sys.path.append(
    os.path.split(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )[0]
)

import pymsteams

def test_env_webhook_url():
    """
        Test that we have the webhook set as an environment variable.
        This is testing our test environment, not the code.
    """
    webhook_url = os.getenv("MS_TEAMS_WEBHOOK", None)
    assert webhook_url
    assert webhook_url.find("https") == 0

def test_send_message():
    """
        This sends a simple text message with a title and link button.
    """

    teams_message = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    teams_message.text("This is a simple text message.")
    teams_message.title("Simple Message Title")
    teams_message.addLinkButton("Go to the Repo", "https://github.com/rveachkc/pymsteams")
    # teams_message.send()

    # assert isinstance(teams_message.last_http_response.status_code, int)


def test_async_send_message():
    """
        This asynchronously send a simple text message with a title and link button.
    """

    loop = asyncio.get_event_loop()

    teams_message = pymsteams.async_connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    teams_message.text("This is a simple text message.")
    teams_message.title("Simple Message Title")
    teams_message.addLinkButton("Go to the Repo", "https://github.com/rveachkc/pymsteams")
    # loop.run_until_complete(teams_message.send())

    # assert isinstance(teams_message.last_http_response.status_code, int)


def test_send_sectioned_message():
    """
        This sends a message with sections.
    """

    # start the message
    teams_message = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    teams_message.text("This is the main title.")
    teams_message.title("Sectioned Message Title")

    # section 1
    section_1 = pymsteams.cardsection()
    section_1.title("Section 1 title")
    section_1.activityTitle("my activity title")
    section_1.activitySubtitle("my activity subtitle")
    section_1.activityImage("https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_1.jpg")
    section_1.activityText("This is my activity Text.  You should see an activity image, activity title, activity subtitle, and this text (of course).")
    section_1.addFact("Fact", "this is fine")
    section_1.addFact("Fact", "this is also fine")
    section_1.text("This is my section 1 text.  This section has an activity above and two facts below.")
    teams_message.addSection(section_1)

    # section 2
    section_2 = pymsteams.cardsection()
    section_2.text("This is section 2.  You should see an image.  This section does not have facts or a title.")
    section_2.addImage("https://raw.githubusercontent.com/rveachkc/pymsteams/develop/test/desk_toys_2.jpg", ititle="Pew Pew Pew")
    teams_message.addSection(section_2)


    # send
    # teams_message.send()
    # assert isinstance(teams_message.last_http_response.status_code, int)


def test_send_potential_action():
    """
        This sends a message with a potential action
    """

    myTeamsMessage = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    myTeamsMessage.text("This message should have four potential actions.")
    myTeamsMessage.title("Action Message Title")

    myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
    myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment",False)
    myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction2 = pymsteams.potentialaction(_name = "Get Users")
    myTeamsPotentialAction2.addInput("DateInput","dueDate","Enter due date")
    myTeamsPotentialAction2.addAction("HttpPost","save","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
    myTeamsPotentialAction3.choices.addChoices("In progress","0")
    myTeamsPotentialAction3.choices.addChoices("Active","1")
    myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select a status",False)
    myTeamsPotentialAction3.addAction("HttpPost","Save","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction4 = pymsteams.potentialaction(_name = "Download pymsteams")
    myTeamsPotentialAction4.addOpenURI("Links", [
        {
            "os": "default",
            "uri": "https://pypi.org/project/pymsteams/",
        },
    ])

    myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)
    myTeamsMessage.summary("Message Summary")

    # myTeamsMessage.send()
    # assert isinstance(myTeamsMessage.last_http_response.status_code, int)


def test_http_500():
    with pytest.raises(pymsteams.TeamsWebhookException):
        #myTeamsMessage = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
        myTeamsMessage = pymsteams.connectorcard("https://httpstat.us/500")
        myTeamsMessage.text("This is a simple text message.")
        myTeamsMessage.title("Simple Message Title")
        myTeamsMessage.send()
        #myTeamsMessage.hookurl = "https://httpstat.us/500"
    

def test_http_403():
    with pytest.raises(pymsteams.TeamsWebhookException):
        myTeamsMessage = pymsteams.connectorcard("http://httpstat.us/403")
        myTeamsMessage.text("This is a simple text message.")
        myTeamsMessage.title("Simple Message Title")
        myTeamsMessage.send()

def test_message_size():
    def getMsg(card):
        msg = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
        msg.title('Simple Message Title')
        msg.summary('Simple Summary')
        msg.addSection(card)
        return msg

    # setup text that's too large
    failure_char_count = 21000
    text = 'a' * failure_char_count

    card = pymsteams.cardsection()
    card.text(text)
    msg = getMsg(card)
    with pytest.raises(pymsteams.TeamsWebhookException):
        msg.send()

    card1 = pymsteams.cardsection()
    card2 = pymsteams.cardsection()
    card1.text(text[:int(len(text)/2)])
    card2.text(text[int(len(text)/2):])
    msg = getMsg(card1)
    # assert msg.send()
    msg = getMsg(card2)
    # assert msg.send()


def test_chaining():
    card = pymsteams.cardsection()
    card.title("Foo").activityTitle("Bar").activitySubtitle("Baz")
    assert card.payload["title"] == "Foo"
    assert card.payload["activityTitle"] == "Bar"
    assert card.payload["activitySubtitle"] == "Baz"

    connector_card = pymsteams.connectorcard("https://example.org")
    connector_card.text("Big text").title("Cool title").summary("Something happened")
    assert connector_card.payload["title"] == "Cool title"
    assert connector_card.payload["text"] == "Big text"
    assert connector_card.payload["summary"] == "Something happened"
