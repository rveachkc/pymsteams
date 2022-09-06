from typing import Optional


class CardSection:
    def title(self, stitle: str):
        # title of the section
        self.payload["title"] = stitle
        return self

    def activityTitle(self, sactivityTitle: str):
        # Title of the event or action. Often this will be the name of the "actor".
        self.payload["activityTitle"] = sactivityTitle
        return self

    def activitySubtitle(self, sactivitySubtitle: str):
        # A subtitle describing the event or action. Often this will be a summary of the action.
        self.payload["activitySubtitle"] = sactivitySubtitle
        return self

    def activityImage(self, sactivityImage: str):
        # URL to image or a data URI with the base64-encoded image inline.
        # An image representing the action. Often this is an avatar of the "actor" of the activity.
        self.payload["activityImage"] = sactivityImage
        return self

    def activityText(self, sactivityText: str):
        # A full description of the action.
        self.payload["activityText"] = sactivityText
        return self

    def addFact(self, factname: str, factvalue: str):
        if "facts" not in self.payload.keys():
            self.payload["facts"] = []

        newfact = {"name": factname, "value": factvalue}
        self.payload["facts"].append(newfact)
        return self

    def addImage(self, simage: str, ititle: Optional[str] = None):
        if "images" not in self.payload.keys():
            self.payload["images"] = []
        imobj = {}
        imobj["image"] = simage
        if ititle:
            imobj["title"] = ititle
        self.payload["images"].append(imobj)
        return self

    def text(self, stext: str):
        self.payload["text"] = stext
        return self

    def linkButton(self, buttontext: str, buttonurl: str):
        self.payload["potentialAction"] = [
            {
                "@context": "http://schema.org",
                "@type": "ViewAction",
                "name": buttontext,
                "target": [buttonurl],
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
