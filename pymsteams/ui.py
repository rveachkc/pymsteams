"""
pymsteams.ui
~~~~~~~~~~~~

A file that includes the UI elements for a message.
"""

from typing import TYPE_CHECKING, Union, Literal

from pymsteams.abc import MISSING

if TYPE_CHECKING:
    from typing_extensions import Self
    from .abc import Link, MISSING
    from .errors import TeamsWebhookException, RateLimited

class UI:
    """
    Base class for all UI Teams components.
    """
    pass

class Card(UI):
    """
    Represents a card component.
    """

    _payload: dict[str, Union[str, list[dict[str, str]], bool]] = {}

    def title(self, title: str) -> Self:
        """
        The title of the card section.
        """

        self._payload["title"] = title
        return self
    
    def start_group(self, start_group: bool) -> Self:
        """
        Tries to set a group for the given section to start a logical group
        of information
        """
        self._payload["startGroup"] = start_group
        return self
    
    def activityTitle(self, activity_title: str) -> Self:
        """
        The title of the event or action.
        Often this will be the name of the 'actor'
        """

        self._payload["activityTitle"] = activity_title
        return self
    
    def activitySubtitle(self, activity_subtitle: str) -> Self:
        """
        A subtitle describing the event or action.
        Often this will be a summary of the action.
        """
        
        self._payload["activitySubtitle"] = activity_subtitle
        return self
    
    def activityImage(self, link: str) -> Self:
        """
        > URL to image or a data URI with the base64-encoded image inline.
        
        An image representing the action. Often this is an avatar of the 'actor'
        of the activity

        Parameters
        ----------
        link: :cls:`str`
            The URL or data URI for the image.
            Tries to encode it and if it fails raises error.

        Raises
        ------
        UnicodeEncodeError:
            When a unicode character failed to convert.
        """

        res = Link.convert(link, encode = 'utf-8')
        
        self._payload["activityImage"] = res
        return self
    
    def activityText(self, text: str) -> Self:
        """
        A full description for the action.

        Parameters
        ----------
        text: :cls:`str`
            The activity text.
        """

        self._payload["activityText"] = text
        return self
    
    def add_fact(self, fact: str, description: str) -> Self:
        """
        Adds a fact to the action.

        Parameters
        ----------
        fact: :cls:`str`
            The fact name.

        description: :cls:`str`
            The fact value or short description.
        """

        if "facts" not in self._payload.keys():
            self._payload["facts"] = []

        newFact = {
            "name": fact,
            "value": description
        }

        self._payload["facts"].append(newFact)
        return self
    
    def add_image(self, image: str, title: Union[str, None] = None) -> Self:
        """
        Adds an image to the Card.

        Parameters
        ----------
        image: :cls:`str`
            The image link, can be encoded or decoded.

        title: :cls:`str`
            The image title.

        Raises
        ------
        UnicodeEncodeError
            When a unicode character failed to convert.
        """

        if "images" not in self._payload.keys():
            self._payload["images"] = []

        res = Link.convert(image, encode = 'utf-8')

        imobj = {}

        imobj["image"] = res

        if title:
            imobj["title"] = title

        self._payload["images"].append(imobj)
        return self
    
    def add_link_button(self, *, label: str, url: str) -> Self:
        """
        Adds a link button object to the card.
        """

        if "potentialAction" not in self._payload.keys():
            self._payload["potentialAction"] = []

        url = Link.convert(url, encode = 'utf-8')

        self._payload["potentialAction"].append({
            "@context": "http://schema.org",
            "@type": "ViewAction",
            "name": label,
            "target": [url]
        })
        return self
    
    def disable_md(self) -> Self:
        """
        Disables Markdown of the text.
        """
        self._payload["markdown"] = False

        return self
    
    def enable_md(self) -> Self:
        """
        Enables Markdown of the text.
        """
        self._payload["markdown"] = True
        return self
    
    @property
    def dump_section(self) -> dict[str, Union[str, list[dict[str, str]], bool]]:
        """
        Dumps the current section and returns its dict (JSON).
        """
        return self._payload
    
class View(UI):
    """
    Represents potential actions as a View.
    """

    def __init__(self, name: str, type_: Literal['ActionCard']) -> None:
        self._payload: dict = {}
        self._choices: Choice = Choice
        self._payload["@type"] = "OpenUri"
        self._payload["name"] = name


    def add_input(self, type_: str, id_: str, title: str, *, multiline: Union[bool, None] = None) -> Self:
        """
        Adds an input action.

        Parameters
        ----------
        type_: :cls:`str`
            The input type.

        id_: :cls:`str`
            The ID for the input.

        title: :cls:`str`
            The input's title.

        multiline: Optional[:cls:`bool`]
            If the input should be in multiline.
        """

        if "inputs" not in self._payload.keys():
            self._payload["inputs"] = []

        if(self._choices.dump_choices == []):
            input_ = {
                "@type": type_,
                "id": id_,
                "isMultiline": multiline,
                "title": title
            }

        else:
            input_ = {
                "@type": type_,
                "id": id_,
                "isMultiline": str(multiline).lower(),
                "choices": self._choices.dump_choices(),
                "title": title
            }

        self._payload["inputs"].append(input_)
        return self
    
    def add_action(self, type_: str, name: str, target: str, body: Union[str, None] = None) -> Self:
        """
        Adds an action type to the potential actions.

        Parameters
        ----------
        type_: :cls:`str`
            The action type.

        name: :cls:`str`
            The action name.

        target: :cls:`str`
            The target that is affected with this action.

        body: Optional[:cls:`str`]
            The body of the action.
            By default is None.
        """

        if "actions" not in self._payload.keys():
            self._payload["actions"] = []

        action = {
            "@type": type_,
            "name": name,
            "taget": target
        }

        if body:
            action["body"] = body

        self._payload["actions"].append(action)

    def add_uri(self, name: str, targets: list) -> Self:
        """
        Adds a URI type.

        Parameters
        ----------
        name: :cls:`str`
            The URI name.

        targets: :cls:`list`:
            The list of the targets that are affected with this URI.
        """

        self._payload["@type"] = "OpenUri"
        self._payload["name"] = name
        self._payload["targets"] = targets

        return self
    
    @property
    def dump_view(self) -> dict:
        """
        Returns the dict (JSON) of the view.
        """

        return self._payload
    
class Choice(UI):
    """
    Represents an input's choices.
    """

    _choices = []

    def add_choice(self, label: str, value: str) -> None:
        """
        Adds a choice to the input.

        Parameters
        ----------
        label: :cls:`str`
            The choice display label.

        value: :cls:`str`
            The choice value.
        """
        self._choices.append(
            {
                "display": label,
                "value": value
            }
        )

    @property
    def dump_choices(self) -> list[dict[str, str]]:
        """
        Returns the dict (JSON) of the choices added.
        """
        return self._choices
    
class Connector(Card):
    """
    Represents a connector for a card.

    .. subclass of Card.
    """

    def __init__(self, hookUrl: str, *, http_proxy: Union[str, None] = None, https_proxy: Union[str, None] = None, timeout: int = 60, verify = None) -> None:
        self._payload: dict = {}
        self.hook_url: str = Link.convert(hookUrl)
        self.proxies: Union[dict, None] = {}
        self.timeout: int = timeout
        self.verify = verify
        self.lastHttp = None

        if http_proxy:
            self.proxies['http'] = http_proxy

        if https_proxy:
            self.proxies['https'] = https_proxy

        if not self.proxies:
            self.proxies = None

    def send(self, content: str = MISSING) -> Literal[True]:
        """
        Sends a message.

        Parameters
        ----------
        content: :cls:`str`
            The message content.
        """

        headers = {
            "Content-Type": "application/json"
        }

        from requests import post, Response

        request = post(
            self.hook_url,
            json = self._payload,
            headers = headers,
            proxies = self.proxies,
            timeout = self.timeout,
            verify = self.verify
        )

        self.lastHttp: Response = request

        json_res = request.json()

        if "status" in json_res.keys():
            status = json_res.pop("satus")

        if int(status) == 200:
            return True
        
        elif int(status) == 429:
            raise RateLimited(json_res.pop("retry_after"))
        
        else:
            raise TeamsWebhookException()

        
class AsyncConnector(Connector):
    """
    Represents a conncetor for a card.

    This class functions and definitions are coros.

    .. subclass of Connector
    """

    async def send(self, content: str = MISSING) -> Literal[True]:
        try:
            import httpx

        except ImportError as e:
            print(
                "In order to use the asynchronous connector card, "
                "install the asynchronous version of the library via pip:"
                "pip install pymsteams[async]"
            )

            raise e
        
        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(
            proxies = self.proxies,
            verify = self.verify,
        ) as client:
            response = await client.post(
                self.hook_url,
                json = self._payload,
                headers = headers,
                timeout = self.timeout
            )

            self.lastHttp: httpx.Response = response

            if response.status_code == httpx.codes.OK and response.text == '1':
                return True
            
            else:
                raise TeamsWebhookException(response.text)