# Python Claude Web Authenticator

This library provides a way to authenticate and interact with the Claude AI API through a web browser. It allows you to send messages to Claude, create new chats, rename chats, and more.

## Installation

To install the library, run the following command:

```
pip install git+https://github.com/pysyun/python_claude_web_authenticator.git
```

If you want to use the optional `authenticator` module for web-based authentication, you can install it with the following command:

```
pip install git+https://github.com/pysyun/python_claude_web_authenticator.git[authenticator]
```

## Usage

### Authentication

To authenticate with the Claude AI API, you need to provide your Claude cookie. The library supports two methods of authentication:

1. **Environment Variable**: Set the `CLAUDE_COOKIE` environment variable with your Claude cookie value.

2. **Web-based Authentication** (requires the `authenticator` module):
   - Run the `ClaudeAuthenticator().process(_)` method to open a web browser and prompt you to log in to https://claude.ai/.
   - The library will automatically retrieve the necessary cookie and store it in the environment variable and `.env` file.

### Interacting with Claude

The library provides the following methods to interact with Claude:

- `send_message(prompt, conversation_id, attachment=None, timeout=500)`: Sends a message to Claude and returns the response.
- `rename_chat(title, conversation_id)`: Renames a chat conversation with the specified title.
- `create_new_chat()`: Creates a new chat conversation and returns the conversation information.

### Example

Here's an example of how to use the library to send a message to Claude and create a new chat:

```python
from claude_client_override import Client

claude_api = Client(claude_cookie)
prompt = "Hello, Claude!"
conversation_id = claude_api.create_new_chat()['uuid']
response = claude_api.send_message(prompt, conversation_id)
print(response)
```

## Modules

The library consists of the following modules:

- `authenticator.py`: Provides web-based authentication functionality using Playwright.
- `claude_client_override.py`: Overrides the default Claude API client to add additional functionality.
- `dialog.py`: Implements a dialog class for interacting with Claude.

## Dependencies

The library has the following dependencies:

- `python-dotenv`: For loading environment variables from a `.env` file.
- `claude-api`: The official Claude API library.
- `playwright` (optional): Required for web-based authentication using the `authenticator` module.

Please refer to the source code and docstrings for more detailed information on each module and its functionality.