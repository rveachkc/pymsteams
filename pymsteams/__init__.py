#!/usr/bin/env python

# https://github.com/rveachkc/pymsteams/
# reference: https://dev.outlook.com/connectors/reference

"""
pymsteams
~~~~~~~~~

Python Wrapper Library to send requests to Microsoft Teams Webhooks. Microsoft refers to these messages as Connector Cards. A message can be sent with only the main Connector Card, or additional sections can be included into the message.

This library uses Webhook Connectors for Microsoft Teams. Please visit the following Microsoft Documentation link for instructions on how to obtain the correct url for your Channel: https://dev.outlook.com/Connectors/GetStarted#creating-messages-through-office-365-connectors-in-microsoft-teams

Please refer to the Microsoft Documentation for the most up to date screenshots. https://dev.outlook.com/connectors/reference
"""

from .errors import *
from .abc import Link
from .ui import Card, Choice, UI, View, Connector, AsyncConnector