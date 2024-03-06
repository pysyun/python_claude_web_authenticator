import json
import re
from curl_cffi import requests
from claude_api import Client


class ClaudeClientOverride(Client):

    def get_organization_id(self):
        url = "https://claude.ai//api/auth/current_account"

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/login',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}'
        }

        response = requests.get(url, headers=headers, impersonate="chrome110")
        res = json.loads(response.text)
        uuid = next(iter(res['messageLimits']))

        return uuid

    # Send Message to Claude
    def send_message(self, prompt, conversation_id, attachment=None, timeout=500):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}/completion"


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

            "prompt": f"{prompt}",
            "attachments": attachments,
            "files": [],
            "timezone": "Asia/Kolkata"

        })

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
           'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/event-stream, text/event-stream',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3',
            'Alt-Used': 'claude.ai',
            'Referer': f'https://claude.ai/chat/{self.organization_id}',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
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
            if data_string != 'event: completion' and data_string != 'event: ping':
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
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/122.0',
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
        if response.status_code == 200:
            return True
        else:
            return False

    def create_new_chat(self):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"
        uuid = self.generate_uuid()

        payload = json.dumps({"uuid": uuid, "name": ""})
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'anthropic-client-sha': 'unknown',
            'anthropic-client-version': 'unknown',
            'Alt-Used': 'claude.ai',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'Cookie': f'{self.cookie}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            }

        response = requests.post(url, headers=headers, data=payload, impersonate="chrome110")


        # Returns JSON of the newly created conversation information
        return response.json()
