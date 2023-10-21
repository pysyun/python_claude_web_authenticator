import os
from authenticator import ClaudeAuthenticator
from dialog import ClaudeDialog

from dotenv import load_dotenv

load_dotenv()

# Authenticate using the automated Browser or saved token
ClaudeAuthenticator().process([])

# Create the Claude API client
dialog = ClaudeDialog()
data = dialog.process(["Please, generate an advanced Rust 'Hello, world' application."])
print(data)
