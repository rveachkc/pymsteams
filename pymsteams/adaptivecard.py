from .base import Base
import re


class AdaptiveCard(Base):
    def __init__(self, hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None):
        super().__init__(hookurl, http_proxy, https_proxy, http_timeout, verify)
        payload = self.payload
        payload['type'] = 'message'
        payload['attachments'] = [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [],
                    "msteams": {
                        "entities": []
                    }
                }
            }
        ]

        self.payload = payload
        return

    def mention_check_and_update_entities(self):
        """
        For mention on adaptive card, mention entitiy(s) are necessary for each of them.
        On this function, it is checking if those mention blocks are included in text.
        If it's included, mention entity(s) will be created with those information.
        For mention, required information is id(Microsoft UPN or AAD) and name.
        Name is used for display on Teams which you posts.
        If you use following syntax, inside of [] is used for name and inside of () is used for id.

        e.g1) <at>AdeleV@contoso.onmicrosoft.com</at>
            name : AdeleV
            id   : AdeleV@contoso.onmicrosoft.com
        e.g2) <at>[Adele Vance](AdeleV@contoso.onmicrosoft.com)</at>
            name : Adele Vance
            id   : AdeleV@contoso.onmicrosoft.com


        https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cconnector-html#user-mention-in-incoming-webhook-with-adaptive-cards
        {
            "type": "message",
            "attachments": [
                {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Sample Adaptive Card with User Mention"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Hi <at>Adele UPN</at>, <at>Adele AAD</at>"
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                    "msteams": {
                        "entities": [
                            {
                                "type": "mention",
                                "text": "<at>Adele UPN</at>",
                                "mentioned": {
                                "id": "AdeleV@contoso.onmicrosoft.com",
                                "name": "Adele Vance"
                                }
                            },
                            {
                                "type": "mention",
                                "text": "<at>Adele AAD</at>",
                                "mentioned": {
                                "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
                                "name": "Adele Vance"
                                }
                            }
                        ]
                    }
                }
            }]
        }


        """

        # check if mention blocks are on text section
        body = self.payload['attachments'][0]['content']['body']
        mention_user_keys = []
        regex_mention = r'\<at\>([^<]*?)\<\/at\>'
        for body_row in body:
            body_row_text = body_row['text']
            mention_text = re.findall(regex_mention, body_row_text)  # search <at>~</at>
            mention_user_keys.extend(mention_text)
        # delete duplicated mention user key
        mention_user_keys = list(set(mention_user_keys))
        # delete mention user key if it already exists in entities section
        current_entities = self.payload['attachments'][0]['content']['msteams']['entities']
        for entitiy in current_entities:
            try:
                existing_mention_user_key = entitiy['text'].replace('<at>', '').replace('</at>', '')
                mention_user_keys.remove(existing_mention_user_key)
            except BaseException:
                pass

        """
        On this section, it will create mention user key/id/name.
        When it's [User name](User id) syntax, [User name] is used for user name and (User id) is used for user id.
        When it's user.email@abc.com syntax, user.email is used for user name and user.email@abc.com is used for user id.
        """
        mention_user_info_list = []
        for mention_user_key in mention_user_keys:
            mention_user_key_list = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', mention_user_key)

            if len(mention_user_key_list) == 1:
                mention_user_key = mention_user_key
                mention_user_name = mention_user_key_list[0][0]
                mention_user_id = mention_user_key_list[0][1]
            else:
                mention_user_key = mention_user_key
                mention_user_id = mention_user_key
                print(mention_user_key)
                mention_user_name = mention_user_key.split('@')[0]
                print(mention_user_name)
            mention_user_info_list.append(
                {
                    'mention_user_key': mention_user_key,
                    'mention_user_id': mention_user_id,
                    'mention_user_name': mention_user_name
                }
            )

        additional_entities = []
        for mention_user_info in mention_user_info_list:
            additional_entities.append(
                {
                    "type": "mention",
                    "text": f"<at>{mention_user_info['mention_user_key']}</at>",
                    "mentioned": {
                        "id": mention_user_info['mention_user_id'],
                        "name": mention_user_info['mention_user_name']
                    }
                }
            )
        self.payload['attachments'][0]['content']['msteams']['entities'].extend(additional_entities)
        return

    def text(self, mtext):
        message = {
            'type': 'TextBlock'
        }
        message['text'] = str(mtext)
        self.payload['attachments'][0]['content']['body'].append(message)
        self.mention_check_and_update_entities()
        return
