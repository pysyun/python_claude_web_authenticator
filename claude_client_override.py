import json
import re

from curl_cffi import requests
from claude_api import Client


class ClaudeClientOverride(Client):

    # Send Message to Claude
    def send_message(self, prompt, conversation_id, attachment=None, timeout=500):
        url = "https://claude.ai/api/append_message"

        # Upload attachment if provided
        attachments = []
        if attachment:
            attachment_response = self.upload_attachment(attachment)
            if attachment_response:
                attachments = [attachment_response]
            else:
                return {"Error: Invalid file format. Please try again."}

        # Ensure attachments is an empty list when no attachment is provided
        if not attachment:
            attachments = []

        payload = json.dumps({
            "completion": {
                "prompt": f"{prompt}",
                "timezone": "Asia/Kolkata",
                "model": "claude-2.1"
            },
            "organization_uuid": f"{self.organization_id}",
            "conversation_uuid": f"{conversation_id}",
            "text": f"{prompt}",
            "attachments": attachments
        })

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/event-stream, text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        response = requests.post(url, headers=headers, data=payload, impersonate="chrome110", timeout=500)
        decoded_data = response.content.decode("utf-8")
        decoded_data = re.sub('\n+', '\n', decoded_data).strip()
        data_strings = decoded_data.split('\n')
        completions = []
        for data_string in data_strings:
            json_str = data_string[6:].strip()
            data = json.loads(json_str)
            if 'completion' in data:
                completions.append(data['completion'])

        answer = ''.join(completions)

        # Returns answer
        return answer

        # Renames the chat conversation title

    def rename_chat(self, title, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        payload = json.dumps({
            "name": f"{title}"
        })
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Referer': f'https://claude.ai/chat/{self.organization_id}',
            'Origin': 'https://claude.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
            'TE': 'trailers'
        }

        response = requests.put(url, headers=headers, data=payload, impersonate="chrome110")
        print(response)
        print(response.content)

        if response.status_code == 200:
            return True
        else:
            return False
