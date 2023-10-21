from claude_api import Client


class ClaudeDialog:

    def __init__(self, claude_cookie):
        self.claude_cookie = claude_cookie

    def process(self, data):
        claude_api = Client(self.claude_cookie)
        prompt = data[0]
        conversation_id = claude_api.create_new_chat()['uuid']
        response = claude_api.send_message(prompt, conversation_id)
        return [response]
