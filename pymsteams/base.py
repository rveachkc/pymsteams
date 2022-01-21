import requests
import pprint


class Base:
    def __init__(self, hookurl, http_proxy, https_proxy, http_timeout, verify):
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

    def printme(self):
        print(f"hookurl: {self.hookurl}")
        print('payload')
        pprint.pprint(self.payload)

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
        self.last_http_status = r

        if r.status_code == requests.codes.ok and r.text == '1':  # pylint: disable=no-member
            return True
        else:
            raise TeamsWebhookException(r.text)


class TeamsWebhookException(Exception):
    """custom exception for failed webhook call"""
    pass
