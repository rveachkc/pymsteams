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
    teams_message.send()


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
    teams_message.send()


def test_send_potential_action():
    """
        This sends a message with a potential action
    """

    myTeamsMessage = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
    myTeamsMessage.text("This message should have three potential actions.")
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

    myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)
    myTeamsMessage.summary("Message Summary")
    myTeamsMessage.send()

def test_bad_webhook_call():
    with pytest.raises(pymsteams.TeamsWebhookException):
        #myTeamsMessage = pymsteams.connectorcard(os.getenv("MS_TEAMS_WEBHOOK"))
        myTeamsMessage = pymsteams.connectorcard("https://httpstat.us/500")
        myTeamsMessage.text("This is a simple text message.")
        myTeamsMessage.title("Simple Message Title")
        myTeamsMessage.send()
        #myTeamsMessage.hookurl = "https://httpstat.us/500"
    