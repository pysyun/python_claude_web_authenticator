from claude_api import Client
from dotenv import load_dotenv
import os

def claude_api_connect():
    load_dotenv()
    cookie = os.getenv('COOKIE')
    claude_api = Client(cookie)

    prompt = "Hello, Claude!"
    conversation_id = claude_api.create_new_chat()['uuid']
    response = claude_api.send_message(prompt, conversation_id)
    print(response)

    return claude_api
