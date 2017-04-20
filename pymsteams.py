#!/usr/bin/env python

# https://github.com/rveachkc/pymsteams/

import requests

class section:

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
			self.payload["facts"] = [ { factname : factvalue } ]
		else:
			self.payload["facts"].append({ factname : factvalue })

	def addImage(self, simage, stitle=None):
		if "images" not in self.payload.keys():
			self.payload["images"] = []
		imobj = {}
		imobj["image"] = simage
		if stitle:
			imobj["title"] = stitle
		self.payload["images"].append(imobj)

	def text(self, stext):
		self.payload["text"] = stext

	def linkbutton(self, buttontext, buttonurl):
		self.payload["potentialAction"] = [
			{
			"@context" : "http://schema.org",
			"@type" : "ViewAction",
			"name" : buttontext,
			"target" : [ buttonurl ]
			}
		]

	def disablemarkdown():
		self.payload["markdown"] = False

	def enablemarkdown():
		self.payload["markdown"] = True

	def __init__(self, sslug):
		self.slug=sslug
		self.payload = {}


class connectorcard:

	def text(self, mtext):
		self.payload["text"] = mtext

	def title(self, mtitle):
		self.payload["title"] = mtitle

	def color(self, mcolor):
		if mcolor.lower() == "red":
			self.payload["themeColor"] = "E81123"
		else:
			self.payload["themeColor"] = themeColor

	def linkbutton(self, buttontext, buttonurl):
		self.payload["potentialAction"] = [
			{
			"@context" : "http://schema.org",
			"@type" : "ViewAction",
			"name" : buttontext,
			"target" : [ buttonurl ]
			}
		]

	def newhookurl(self, nhookurl):
		self.hookurl = nhookurl

	def printme(self):
		print("hookurl: %s" % self.hookurl)
		print("payload: %s" % self.payload)

	def send(self):
		headers = {"Content-Type":"application/json"}
		r = requests.post(self.hookurl, json=self.payload, headers=headers)

		if r.status_code == requests.codes.ok:
			return True
		else:
			print(r.text)
			return False

	def __init__(self, hookurl):
		self.payload = {}
		self.hookurl = hookurl

def formaturl(display, url):
	mdurl = "[%s](%s)" % (display, url)
	return mdurl
