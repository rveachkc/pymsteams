# pymsteams

[![CircleCI](https://circleci.com/gh/rveachkc/pymsteams/tree/master.svg?style=shield)](https://circleci.com/gh/rveachkc/pymsteams/tree/master) [![PyPI version](https://badge.fury.io/py/pymsteams.svg)](https://badge.fury.io/py/pymsteams)

Python Wrapper Library to send requests to Microsoft Teams Webhooks.
Microsoft refers to these messages as Connector Cards.  A message can be sent with only the main Connector Card, or additional sections can be included into the message.

This library uses Webhook Connectors for Microsoft Teams.  Please visit the following Microsoft Documentation link for instructions on how to obtain the correct url for your Channel: https://dev.outlook.com/Connectors/GetStarted#creating-messages-through-office-365-connectors-in-microsoft-teams

Please refer to the Microsoft Documentation for the most up to date screenshots.
https://dev.outlook.com/connectors/reference

## Installation

Install with pip:

```bash
pip install pymsteams
```

Install with async capabilities (python 3.6+):

```bash
pip install pymsteams[async]
```

#### Python 2 Installation

At time of writing, the latest release supported by Python 2 is [Version 0.1.16](https://github.com/rveachkc/pymsteams/releases/tag/0.1.16)

## Usage

### Creating ConnectorCard Messages

This is the simplest implementation of pymsteams.  It will send a message to the teams webhook url with plain text in the message.

```python
import pymsteams

# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")

# Add text to the message.
myTeamsMessage.text("this is my text")

# send the message.
myTeamsMessage.send()
```

### Creating CreatorCard Messages to send via async loop

```python
import asyncio
import pymsteams

loop = asyncio.get_event_loop()

# the async_connectorcard object is used instead of the normal one.
myTeamsMessage = pymsteams.async_connectorcard("<Microsoft Webhook URL>")

# all formatting for the message should be the same
myTeamsMessage.text("This is my message")

# to send the message, pass to the event loop
loop.run_until_complete(myTeamsMessage.send())
```

Please visit the python asyncio documentation for more info on using asyncio and the event loop: https://docs.python.org/3/library/asyncio-eventloop.html


### Optional Formatting Methods for Cards

#### Add a title
```python
myTeamsMessage.title("This is my message title")
```

#### Add a link button
```python
myTeamsMessage.addLinkButton("This is the button Text", "https://github.com/rveachkc/pymsteams/")
```

#### Change URL
This is useful in the event you need to post the same message to multiple rooms.
```python
myTeamsMessage.newhookurl("<My New URL>")
```

#### Set Color Theme
This sets the theme color of the card. The parameter is expected to be a hex color code without the hash or the string red.
```python
myTeamsMessage.color("<Hex Color Code>")
```

#### Preview your object
This is a simple print command to view your connector card message object before sending.
```python
myTeamsMessage.printme()
```

### Adding sections to the Connector Card Message
To create a section and add various formatting elements
```python
# create the section
myMessageSection = pymsteams.cardsection()

# Section Title
myMessageSection.title("Section title")

# Activity Elements
myMessageSection.activityTitle("my activity title")
myMessageSection.activitySubtitle("my activity subtitle")
myMessageSection.activityImage("http://i.imgur.com/c4jt321l.png")
myMessageSection.activityText("This is my activity Text")

# Facts are key value pairs displayed in a list.
myMessageSection.addFact("this", "is fine")
myMessageSection.addFact("this is", "also fine")

# Section Text
myMessageSection.text("This is my section text")

# Section Images
myMessageSection.addImage("http://i.imgur.com/c4jt321l.png", ititle="This Is Fine")

# Add your section to the connector card object before sending
myTeamsMessage.addSection(myMessageSection)
```
You may also add multiple sections to a connector card message as well.
```python
# Create Section 1
Section1 = pymsteams.cardsection()
Section1.text("My First Section")

# Create Section 2
Section2 = pymsteams.cardsection()
Section2.text("My Second Section")

# Add both Sections to the main card object
myTeamsMessage.addSection(Section1)
myTeamsMessage.addSection(Section2)

# Then send the card
myTeamsMessage.send()
```
### Adding potential actions to the Connector Card Message
To create a actions on which the user can interect with in MS Teams
To find out more information on what actions can be used, please visit https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/connectors/connectors-using#setting-up-a-custom-incoming-webhook

```python
myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")

myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment here",False)
myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://..."") 

myTeamsPotentialAction2 = pymsteams.potentialaction(_name = "Set due date")
myTeamsPotentialAction2.addInput("DateInput","dueDate","Enter due date")
myTeamsPotentialAction2.addAction("HttpPost","save","https://...")

myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
myTeamsPotentialAction3.choices.addChoices("In progress","0")
myTeamsPotentialAction3.choices.addChoices("Active","1")
myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select a status",False)
myTeamsPotentialAction3.addAction("HttpPost","Save","https://...")

myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)

myTeamsMessage.summary("Test Message")

myTeamsMessage.send()
```
### Adding HTTP Post to potential actions in the Connector Card Message

```python
myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")

myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
# You can add a TextInput to your potential action like below - Please note the 2nd argment below as the id name
myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment here",False)
# we use the 2nd argument above as the id name to parse the values into the body post like below.
myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://...", "{{comment.value}}") 
myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)


myTeamsMessage.summary("Test Message")

myTeamsMessage.send()

# Notes:
# If you post anything via teams, you will get some Javascript encoding happening via the post - For example:
# Posting this:  {"name":"john", "comment" : "nice"}
# Output will be:  b'{\\u0022name\\u0022:\\u0022john\\u0022, \\u0022comment\\u0022 : \\u0022nice\\u0022}'
# i solved this issue by decoding unicode escape for a custom rest backend.
```

Please use Github issues to report any bugs or request enhancements.

## Troubleshooting HTTP response

This module is really just a nice wrapper pointed at the Microsoft API. To help troubleshoot missing messages, the requests response content is saved to the connectorcard class attribute `last_http_response`.

To get the last http status code:
```python
import pymsteams

myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")
myTeamsMessage.text("this is my text")
myTeamsMessage.send()

last_status_code = myTeamsMessage.last_http_response.status_code
```

More info on the Response Content is available in the requests documentation, [link](https://2.python-requests.org/en/master/user/quickstart/#response-content).

## Exceptions

If the call to the Microsoft Teams webhook service fails, a `TeamsWebhookException` will be thrown.

## Testing

In order to test in your environment with pytest, set the environment variable `MS_TEAMS_WEBHOOK` to the Microsoft Teams Webhook url you would like to use.

Then, from the root of the repo, install the requirements and run pytest.

```bash
pip install -r dev-requirements.txt
MS_TEAMS_WEBHOOK=MicrosoftWebhookURL
export MS_TEAMS_WEBHOOK
pytest --cov=./pymsteams --cov-report=term-missing --cov-branch
```

This will send two MS Teams messages describing how they are formatted.  Manually validate that the message comes through as expected.

## Certificate Validation

In some situations, a custom CA bundle must be used.  This can be set on class initialization, by setting the verify parameter.

```python
import pymsteams

# set custom ca bundle
msg = pymsteams.connectorcard("<Microsoft Webhook URL>", verify="/path/to/file")

# disable CA validation
msg = pymsteams.connectorcard("<Microsoft Webhook URL>", verify=False)
```

Set to either the path of a custom CA bundle or False to disable.

The requests documentation can be referenced for full details: https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification
