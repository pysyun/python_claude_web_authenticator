import os

from playwright.sync_api import sync_playwright


class ClaudeAuthenticator:

    def process(self, _):

        if 'CLAUDE_COOKIE' in os.environ:
            return

        with sync_playwright() as p:

            browser = p.firefox.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://claude.ai/login')

            while True:
                cookies = page.context.cookies()
                cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
                if "sessionKey" in cookies_str:
                    break

            os.environ["CLAUDE_COOKIE"] = cookies_str
            with open('.env', 'w') as env_file:
                env_file.write(f"CLAUDE_COOKIE={os.environ['CLAUDE_COOKIE']}")
