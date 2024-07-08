import json
import os
import uuid
import requests
import httpx
import re


class Client:

    def __init__(self, cookie, organization_id=None):
        self.cookie = cookie
        if not organization_id:
            self.organization_id = self.get_organization_id()
            os.environ["ORGANIZATION_ID"] = self.organization_id
            with open('.env', 'r') as env_file:
                existing_env = env_file.read()
                if not f"ORGANIZATION_ID=" in existing_env:
                    with open('.env', 'a') as env_file:
                        env_file.write(f"\nORGANIZATION_ID={self.organization_id}")
        else:
            self.organization_id = organization_id

    def get_organization_id(self):
        url = "https://claude.ai/api/bootstrap"

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://claude.ai/login',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}'
        }

        response = httpx.get(url, headers=headers)
        res = json.loads(response.text)
        uuid = res['account']['memberships'][0]['organization']['uuid']

        return uuid

    def get_content_type(self, file_path):
        # Function to determine content type based on file extension
        extension = os.path.splitext(file_path)[-1].lower()
        if extension == '.pdf':
            return 'application/pdf'
        elif extension == '.txt':
            return 'text/plain'
        elif extension == '.csv':
            return 'text/csv'
        # Add more content types as needed for other file types
        else:
            return 'application/octet-stream'

    # Lists all the conversations you had with Claude
    def list_all_conversations(self):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}'
        }

        response = httpx.get(url, headers=headers)
        conversations = response.json()

        # Returns all conversation information in a list
        if response.status_code == 200:
            return conversations
        else:
            print(f"Error: {response.status_code} - {response.text}")

    # Send Message to Claude
    def send_message(self, prompt, conversation_id, attachment=None):
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

        response = httpx.post(url, headers=headers, data=payload, timeout=500)
        if not response.status_code == 200:
            return f'ERROR: {response.text}'
        decoded_data = response.content.decode(response.encoding)
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

    # Deletes the conversation
    def delete_conversation(self, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        payload = json.dumps(f"{conversation_id}")
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Content-Length': '38',
            'Referer': 'https://claude.ai/chats',
            'Origin': 'https://claude.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
            'TE': 'trailers'
        }

        response = requests.delete(url, headers=headers, data=payload)

        # Returns True if deleted or False if any error in deleting
        if response.status_code == 204:
            return True
        else:
            return False

    # Returns all the messages in conversation
    def chat_conversation_history(self, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}'
        }

        response = httpx.get(url, headers=headers)

        # List all the conversations in JSON
        return response.json()

    def generate_uuid(self):
        random_uuid = uuid.uuid4()
        random_uuid_str = str(random_uuid)
        formatted_uuid = f"{random_uuid_str[0:8]}-{random_uuid_str[9:13]}-{random_uuid_str[14:18]}-{random_uuid_str[19:23]}-{random_uuid_str[24:]}"
        return formatted_uuid

    def create_new_chat(self):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"
        uuid = self.generate_uuid()

        payload = json.dumps({"uuid": uuid, "name": ""})
        headers = {
            'Accept': '*/*',
            'anthropic-client-sha': 'unknown',
            'anthropic-client-version': 'unknown',
            'Alt-Used': 'claude.ai',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://claude.ai/chats',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'Cookie': f'{self.cookie}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }

        response = httpx.post(url, headers=headers, data=payload)
        # Returns JSON of the newly created conversation information
        return response.json()

    # Resets all the conversations
    def reset_all(self):
        conversations = self.list_all_conversations()

        for conversation in conversations:
            conversation_id = conversation['uuid']
            delete_id = self.delete_conversation(conversation_id)

        return True

    def upload_attachment(self, file_path):
        if file_path.endswith('.txt'):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = "text/plain"
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            return {
                "file_name": file_name,
                "file_type": file_type,
                "file_size": file_size,
                "extracted_content": file_content
            }
        url = 'https://claude.ai/api/convert_document'
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://claude.ai/chats',
            'Origin': 'https://claude.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
            'TE': 'trailers'
        }

        file_name = os.path.basename(file_path)
        content_type = self.get_content_type(file_path)

        files = {
            'file': (file_name, open(file_path, 'rb'), content_type),
            'orgUuid': (None, self.organization_id)
        }

        response = httpx.post(url, headers=headers, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    def get_title(self, conversation_id, bot_message, prompt):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}/title"

        data = {
            'message': f"Message 1:\n\n{prompt}\n\nMessage 2:\n\n{bot_message}",
            'recent_titles': []
        }

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3',
            'Referer': f'https://claude.ai/chat/{conversation_id}',
            'Content-Type': 'application/json',
            'Origin': 'https://claude.ai',
            'Cookie': f'{self.cookie}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        response = httpx.post(url, headers=headers, data=data, timeout=500)
        return response

    # Renames the chat conversation title
    def rename_chat(self, title, conversation_id):
        url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

        payload = json.dumps({
            "name": f"{title}"
        })
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'Referer': f'https://claude.ai/chat/{conversation_id}',
            'Origin': 'https://claude.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cookie': f'{self.cookie}',
        }

        response = httpx.put(url, headers=headers, data=payload, timeout=500)
        if response.status_code == 200:
            return True
        else:
            return False
