# pymsteams

* Master: [![CircleCI](https://circleci.com/gh/rveachkc/pymsteams/tree/master.svg?style=svg)](https://circleci.com/gh/rveachkc/pymsteams/tree/master)
* Develop: [![CircleCI](https://circleci.com/gh/rveachkc/pymsteams/tree/develop.svg?style=svg)](https://circleci.com/gh/rveachkc/pymsteams/tree/develop)

Python Wrapper Library to send requests to Microsoft Teams Webhooks.
Microsoft refers to these messages as Connector Cards.  A message can be sent with only the main Connector Card, or additional sections can be included into the message.

This library uses Webhook Connectors for Microsoft Teams.  Please visit the following Microsoft Documentation link for instructions on how to obtain the correct url for your Channel: https://dev.outlook.com/Connectors/GetStarted#creating-messages-through-office-365-connectors-in-microsoft-teams

Please refer to the Microsoft Documentation for the most up to date screenshots.
https://dev.outlook.com/connectors/reference

## Creating ConnectorCard Messages
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

## Optional Formatting Methods for Cards

### Add a title
```python
myTeamsMessage.title("This is my message title")
```

### Add a link button
```python
myTeamsMessage.addLinkButton("This is the button Text", "https://github.com/rveachkc/pymsteams/")
```

### Change URL
This is useful in the event you need to post the same message to multiple rooms.
```python
myTeamsMessage.newhookurl("<My New URL>")
```

### Preview your object
This is a simple print command to view your connector card message object before sending.
```python
myTeamsMessage.printme()
```

## Adding sections to the Connector Card Message
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
Section2.text("My First Section")

# Add both Sections to the main card object
myTeamsMessage.addSection(Section1)
myTeamsMessage.addSection(Section2)

# Then send the card
myTeamsMessage.send()
```

Please use Github issues to report any bugs or request enhancements.
