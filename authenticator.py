from playwright.sync_api import sync_playwright
import os


class ClaudeAuthenticator:

    def process(self, _):

        with sync_playwright() as p:

            browser = p.firefox.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://claude.ai/login')

            input('Press "enter" after you are logged into the account.')

            cookies = page.context.cookies()

            cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            os.environ["CLAUDE_COOKIE"] = cookies_str
            with open('.env', 'w') as env_file:
                env_file.write(f"CLAUDE_COOKIE={os.environ['CLAUDE_COOKIE']}")
