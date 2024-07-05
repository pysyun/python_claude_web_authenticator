import os
import re

from claude_client_override import Client


class ClaudeDialog:

    def __init__(self):
        self.claude_cookie = os.environ['CLAUDE_COOKIE']
        self.organization_id = os.environ.get('ORGANIZATION_ID')

    def process(self, data):
        claude_api = Client(self.claude_cookie, self.organization_id)
        prompt = data[0]
        conversation_id = claude_api.create_new_chat()['uuid']
        response = claude_api.send_message(prompt, conversation_id)
        if re.match(r'^ERROR', response):
            return [response]
        title_chat_id = claude_api.create_new_chat()['uuid']
        title = claude_api.send_message(f'Generate only a title for this text: {response}', title_chat_id)
        claude_api.rename_chat(title, conversation_id)
        claude_api.delete_conversation(title_chat_id)
        return [response]