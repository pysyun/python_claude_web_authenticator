import os

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


class ClaudeAuthenticator:

    def process(self, _):

        if 'CLAUDE_COOKIE' in os.environ:
            return

        print("Please, authenticate to https://claude.ai/ in the Web browser.\nOpening the browser...")

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
            with open('.env', 'r') as env_file:
                existing_env = env_file.read()
                if not f"CLAUDE_COOKIE=" in existing_env:
                    with open('.env', 'a') as env_file:
                        env_file.write(f"\nCLAUDE_COOKIE={cookies_str}")

    async def process_async(self, _):

        if 'CLAUDE_COOKIE' in os.environ:
            return

        print("Please, authenticate to https://claude.ai/ in the Web browser.\nOpening the browser...")

        async with async_playwright() as p:

            browser = await p.firefox.launch(headless=False, slow_mo=50)
            page = await browser.new_page()
            await page.goto('https://claude.ai/login')

            while True:
                cookies = await page.context.cookies()
                cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
                if "sessionKey" in cookies_str:
                    break

            os.environ["CLAUDE_COOKIE"] = cookies_str
            with open('.env', 'r') as env_file:
                existing_env = env_file.read()
                if not f"CLAUDE_COOKIE=" in existing_env:
                    with open('.env', 'a') as env_file:
                        env_file.write(f"\nCLAUDE_COOKIE={cookies_str}")

