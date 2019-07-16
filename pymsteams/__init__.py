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

    def activityTitle(self, sactivityTitle):
        # Title of the event or action. Often this will be the name of the "actor".
        self.payload["activityTitle"] = sactivityTitle

    def activitySubtitle(self, sactivitySubtitle):
        # A subtitle describing the event or action. Often this will be a summary of the action.
        self.payload["activitySubtitle"] = sactivitySubtitle

    def activityImage(self, sactivityImage):
        # URL to image or a data URI with the base64-encoded image inline.
        # An image representing the action. Often this is an avatar of the "actor" of the activity.
        self.payload["activityImage"] = sactivityImage

    def activityText(self, sactivityText):
        # A full description of the action.
        self.payload["activityText"] = sactivityText

    def addFact(self, factname, factvalue):
        if "facts" not in self.payload.keys():
            self.payload["facts"] = []

        newfact = {
            "name" : factname,
            "value" : factvalue
        }
        self.payload["facts"].append(newfact)

    def addImage(self, simage, ititle=None):
        if "images" not in self.payload.keys():
            self.payload["images"] = []
        imobj = {}
        imobj["image"] = simage
        if ititle:
            imobj["title"] = ititle
        self.payload["images"].append(imobj)


    def text(self, stext):
        self.payload["text"] = stext

    def linkButton(self, buttontext, buttonurl):
        self.payload["potentialAction"] = [
            {
            "@context" : "http://schema.org",
            "@type" : "ViewAction",
            "name" : buttontext,
            "target" : [ buttonurl ]
            }
        ]

    def disableMarkdown(self):
        self.payload["markdown"] = False

    def enableMarkdown(self):
        self.payload["markdown"] = True

    def dumpSection(self):
        return self.payload

    def __init__(self):
        self.payload = {}
        


class potentialaction:
    
    def addInput(self,_type,_id,title, isMultiline = None):
        if "inputs" not in self.payload.keys():
            self.payload["inputs"] = []
        if(self.choices.dumpChoices() == []):
            input = {
                "@type": _type,
                "id": _id,
                "isMultiline" :isMultiline,
                "title": title
            }
        else:
             input = {
                "@type": _type,
                "id": _id,
                "isMultiline" :str(isMultiline).lower(),
                "choices":self.choices.dumpChoices(),
                "title": title
            }

        self.payload["inputs"].append(input)

    def addAction(self,_type,_name,_target):
        if "actions" not in self.payload.keys():
            self.payload["actions"] = []
        action = {
             "@type": _type,
             "name": _name,
             "target": _target
        }

        self.payload["actions"].append(action)

   

    def dumpPotentialAction(self):
        return self.payload

    def __init__(self, _name, _type = "ActionCard"):
        self.payload = {}
        self.payload["@type"] = _type
        self.payload["name"] = _name
        self.choices = choice()

class choice:
    def __init__(self):
        self.choices = []
    
    def addChoices(self,_display,_value):
        self.choices.append({
                                "display": _display,
                                "value": _value
                            })
    def dumpChoices(self):
        return self.choices

class connectorcard:

    def text(self, mtext):
        self.payload["text"] = mtext

    def title(self, mtitle):
        self.payload["title"] = mtitle

    def summary(self, msummary):
        self.payload["summary"] = msummary

    def color(self, mcolor):
        if mcolor.lower() == "red":
            self.payload["themeColor"] = "E81123"
        else:
            self.payload["themeColor"] = mcolor

    def addLinkButton(self, buttontext, buttonurl):
        if "potentialAction" not in self.payload:
            self.payload["potentialAction"] = []

        thisbutton = {
            "@context" : "http://schema.org",
            "@type" : "ViewAction",
            "name" : buttontext,
            "target" : [ buttonurl ]
        }

        self.payload["potentialAction"].append(thisbutton)

    def newhookurl(self, nhookurl):
        self.hookurl = nhookurl

    def addSection(self, newsection):
        # this function expects a cardsection object
        if "sections" not in self.payload.keys():
            self.payload["sections"] = []

        self.payload["sections"].append(newsection.dumpSection())

    def addPotentialAction(self, newaction):
        # this function expects a potential action object
        if "potentialAction" not in self.payload.keys():
            self.payload["potentialAction"] = []

        self.payload["potentialAction"].append(newaction.dumpPotentialAction())

    def printme(self):
        print("hookurl: %s" % self.hookurl)
        print("payload: %s" % self.payload)

    def send(self):
        headers = {"Content-Type":"application/json"}
        r = requests.post(
            self.hookurl,
            json=self.payload,
            headers=headers,
            proxies=self.proxies,
            timeout=self.http_timeout,
            verify=self.verify
        )

        if r.status_code == requests.codes.ok:
            return True
        else:
            raise TeamsWebhookException(r.text)

    def __init__(self, hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None):
        self.payload = {}
        self.hookurl = hookurl
        self.proxies = {}
        self.http_timeout = http_timeout
        self.verify = verify

        if http_proxy:
            self.proxies['http'] = http_proxy

        if https_proxy:
            self.proxies['https'] = https_proxy

        if not self.proxies:
            self.proxies = None


def formaturl(display, url):
    mdurl = "[%s](%s)" % (display, url)
    return mdurl
