from typing import Optional


class choice:
    def __init__(self):
        self.choices = []

    def addChoices(self, _display: str, _value: str):
        self.choices.append({"display": _display, "value": _value})
        return self

    def dumpChoices(self):
        return self.choices


class potentialaction:
    def addInput(
        self, _type: str, _id: str, title: str, isMultiline: Optional[bool] = None
    ):
        if "inputs" not in self.payload.keys():
            self.payload["inputs"] = []
        if self.choices.dumpChoices() == []:
            input = {
                "@type": _type,
                "id": _id,
                "isMultiline": isMultiline,
                "title": title,
            }
        else:
            input = {
                "@type": _type,
                "id": _id,
                "isMultiline": str(isMultiline).lower(),
                "choices": self.choices.dumpChoices(),
                "title": title,
            }

        self.payload["inputs"].append(input)
        return self

    def addAction(self, _type, _name, _target, _body=None):
        if "actions" not in self.payload.keys():
            self.payload["actions"] = []
        action = {"@type": _type, "name": _name, "target": _target}
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
