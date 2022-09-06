import warnings
from pymsteams.webhook import send_webhook_sync
from pymsteams.exceptions import TeamsWebhookException
from pymsteams.legacy.potentialaction import PotentialAction


class ConnectorCard:
    def text(self, mtext: str):
        self.payload["text"] = mtext
        return self

    def title(self, mtitle: str):
        self.payload["title"] = mtitle
        return self

    def summary(self, msummary: str):
        self.payload["summary"] = msummary
        return self

    def color(self, mcolor: str):
        if mcolor.lower() == "red":
            self.payload["themeColor"] = "E81123"
        else:
            self.payload["themeColor"] = mcolor
        return self

    def addLinkButton(self, buttontext: str, buttonurl: str):
        if "potentialAction" not in self.payload:
            self.payload["potentialAction"] = []

        thisbutton = {
            "@context": "http://schema.org",
            "@type": "ViewAction",
            "name": buttontext,
            "target": [buttonurl],
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

    def addPotentialAction(self, newaction: PotentialAction):
        # this function expects a potential action object
        if "potentialAction" not in self.payload.keys():
            self.payload["potentialAction"] = []

        self.payload["potentialAction"].append(newaction.dumpPotentialAction())
        return self

    def printme(self):
        """prints hook url and payload - not super useful"""

        warnings.warn(
            "The connectorcard.printme class method will be removed in future releases",
            DeprecationWarning,
        )

        print("hookurl: %s" % self.hookurl)
        print("payload: %s" % self.payload)

    def send(self):

        self.last_http_response = send_webhook_sync(
            self.hookurl,
            payload=self.payload,
            proxies=self.proxies,
            timeout=self.http_timeout,
            verify=self.verify,
            legacy_check=True,
        )
        return self

    def __init__(
        self, hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None
    ):
        self.payload = {}
        self.hookurl = hookurl
        self.proxies = {}
        self.http_timeout = http_timeout
        self.verify = verify
        self.last_http_response = None

        if http_proxy:
            self.proxies["http"] = http_proxy

        if https_proxy:
            self.proxies["https"] = https_proxy

        if not self.proxies:
            self.proxies = None


class AsyncConnectorCard(ConnectorCard):
    async def send(self):
        try:
            import httpx
        except ImportError as e:
            print(
                "For use the asynchronous connector card, "
                "install the asynchronous version of the library via pip: pip install pymsteams[async]"
            )
            raise e

        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient(
            proxies=self.proxies, verify=self.verify
        ) as client:
            resp = await client.post(
                self.hookurl,
                payload=self.payload,
                headers=headers,
                timeout=self.http_timeout,
            )
            self.last_http_response = resp
            if resp.status_code == httpx.codes.OK and resp.text == "1":
                return True
            else:
                raise TeamsWebhookException(resp.text)
