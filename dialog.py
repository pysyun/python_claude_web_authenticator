import os

from claude_client_override import ClaudeClientOverride


class ClaudeDialog:

    def __init__(self):
        self.claude_cookie = os.environ['CLAUDE_COOKIE']

    def process(self, data):
        claude_api = ClaudeClientOverride(self.claude_cookie)
        prompt = data[0]
        conversation_id = claude_api.create_new_chat()['uuid']
        response = claude_api.send_message(prompt, conversation_id)
        title_chat_id = claude_api.create_new_chat()['uuid']
        title = claude_api.send_message(f'Generate only a title for this text: {response}', title_chat_id)
        claude_api.rename_chat(title, conversation_id)
        claude_api.delete_conversation(title_chat_id)
        return [response]
