#!/usr/bin/env python

# https://github.com/rveachkc/pymsteams/
# reference: https://dev.outlook.com/connectors/reference
import requests


class TeamsWebhookException(Exception):
    """custom exception for failed webhook call"""
    pass


class cardsection:

    def title(self, stitle):
        # title of the section
        self.payload["title"] = stitle
        return self

    def activityTitle(self, sactivityTitle):
        # Title of the event or action. Often this will be the name of the "actor".
        self.payload["activityTitle"] = sactivityTitle
        return self

    def activitySubtitle(self, sactivitySubtitle):
        # A subtitle describing the event or action. Often this will be a summary of the action.
        self.payload["activitySubtitle"] = sactivitySubtitle
        return self

    def activityImage(self, sactivityImage):
        # URL to image or a data URI with the base64-encoded image inline.
        # An image representing the action. Often this is an avatar of the "actor" of the activity.
        self.payload["activityImage"] = sactivityImage
        return self

    def activityText(self, sactivityText):
        # A full description of the action.
        self.payload["activityText"] = sactivityText
        return self

    def addFact(self, factname, factvalue):
        if "facts" not in self.payload.keys():
            self.payload["facts"] = []

        newfact = {
            "name": factname,
            "value": factvalue
        }
        self.payload["facts"].append(newfact)
        return self

    def addImage(self, simage, ititle=None):
        if "images" not in self.payload.keys():
            self.payload["images"] = []
        imobj = {}
        imobj["image"] = simage
        if ititle:
            imobj["title"] = ititle
        self.payload["images"].append(imobj)
        return self

    def text(self, stext):
        self.payload["text"] = stext
        return self

    def linkButton(self, buttontext, buttonurl):
        self.payload["potentialAction"] = [
            {
                "@context": "http://schema.org",
                "@type": "ViewAction",
                "name": buttontext,
                "target": [buttonurl]
            }
        ]
        return self

    def disableMarkdown(self):
        self.payload["markdown"] = False
        return self

    def enableMarkdown(self):
        self.payload["markdown"] = True
        return self

    def dumpSection(self):
        return self.payload

    def __init__(self):
        self.payload = {}


class potentialaction:

    def addInput(self, _type, _id, title, isMultiline=None):
        if "inputs" not in self.payload.keys():
            self.payload["inputs"] = []
        if (self.choices.dumpChoices() == []):
            input = {
                "@type": _type,
                "id": _id,
                "isMultiline": isMultiline,
                "title": title
            }
        else:
            input = {
                "@type": _type,
                "id": _id,
                "isMultiline": str(isMultiline).lower(),
                "choices": self.choices.dumpChoices(),
                "title": title
            }

        self.payload["inputs"].append(input)
        return self

    def addAction(self, _type, _name, _target,_body=None):
        if "actions" not in self.payload.keys():
            self.payload["actions"] = []
        action = {
            "@type": _type,
            "name": _name,
            "target": _target
        }
        if _body:
            action["body"] = _body

        self.payload["actions"].append(action)
        return self

    def addOpenURI(self, _name, _targets):
        """
        Creates a OpenURI action

        https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference#openuri-action

        :param _name: *Name of the text to appear inside the ActionCard*
        :type _name: str
        :param _targets: *A list of dictionaries, ex: `{"os": "default", "uri": "https://www..."}`*
        :type _targets: list(dict())
        """
        self.payload["@type"] = "OpenUri"
        self.payload["name"] = _name
        if not isinstance(_targets, list):
            raise TypeError("Target must be of type list(dict())")
        self.payload["targets"] = _targets
        return self

    def dumpPotentialAction(self):
        return self.payload

    def __init__(self, _name, _type="ActionCard"):
        self.payload = {}
        self.payload["@type"] = _type
        self.payload["name"] = _name
        self.choices = choice()


class choice:
    def __init__(self):
        self.choices = []

    def addChoices(self, _display, _value):
        self.choices.append({
            "display": _display,
            "value": _value
        })

    def dumpChoices(self):
        return self.choices


class connectorcard:

    def text(self, mtext):
        self.payload["text"] = mtext
        return self

    def title(self, mtitle):
        self.payload["title"] = mtitle
        return self

    def summary(self, msummary):
        self.payload["summary"] = msummary
        return self

    def color(self, mcolor):
        if mcolor.lower() == "red":
            self.payload["themeColor"] = "E81123"
        else:
            self.payload["themeColor"] = mcolor
        return self

    def addLinkButton(self, buttontext, buttonurl):
        if "potentialAction" not in self.payload:
            self.payload["potentialAction"] = []

        thisbutton = {
            "@context": "http://schema.org",
            "@type": "ViewAction",
            "name": buttontext,
            "target": [buttonurl]
        }

        self.payload["potentialAction"].append(thisbutton)
        return self

    def newhookurl(self, nhookurl):
        self.hookurl = nhookurl
        return self

    def addSection(self, newsection):
        # this function expects a cardsection object
        if "sections" not in self.payload.keys():
            self.payload["sections"] = []

        self.payload["sections"].append(newsection.dumpSection())
        return self

    def addPotentialAction(self, newaction):
        # this function expects a potential action object
        if "potentialAction" not in self.payload.keys():
            self.payload["potentialAction"] = []

        self.payload["potentialAction"].append(newaction.dumpPotentialAction())
        return self

    def printme(self):
        print("hookurl: %s" % self.hookurl)
        print("payload: %s" % self.payload)

    def send(self):
        headers = {"Content-Type": "application/json"}
        r = requests.post(
            self.hookurl,
            json=self.payload,
            headers=headers,
            proxies=self.proxies,
            timeout=self.http_timeout,
            verify=self.verify,
        )
        self.last_http_response = r

        if r.status_code == requests.codes.ok and r.text == '1':  # pylint: disable=no-member
            return True
        else:
            raise TeamsWebhookException(r.text)

    def __init__(self, hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None):
        self.payload = {}
        self.hookurl = hookurl
        self.proxies = {}
        self.http_timeout = http_timeout
        self.verify = verify
        self.last_http_response = None

        if http_proxy:
            self.proxies['http'] = http_proxy

        if https_proxy:
            self.proxies['https'] = https_proxy

        if not self.proxies:
            self.proxies = None


class async_connectorcard(connectorcard):

    async def send(self):
        try:
            import httpx
        except ImportError as e:
            print("For use the asynchronous connector card, "
                  "install the asynchronous version of the library via pip: pip install pymsteams[async]")
            raise e

        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient(proxies=self.proxies, verify=self.verify) as client:
            resp = await client.post(self.hookurl,
                                     json=self.payload,
                                     headers=headers,
                                     timeout=self.http_timeout)
            self.last_http_response = resp
            if resp.status_code == httpx.codes.OK and resp.text == '1':
                return True
            else:
                raise TeamsWebhookException(resp.text)


def formaturl(display, url):
    mdurl = "[%s](%s)" % (display, url)
    return mdurl
