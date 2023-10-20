from playwright.sync_api import sync_playwright
import os

def claude_authenticator():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://claude.ai/login')

        input('Press "enter" after you are logged into the account.')

        cookies = page.context.cookies()

        cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        os.environ["COOKIE"] = cookies_str
        with open('.env', 'w') as env_file:
            env_file.write(f"COOKIE={os.environ['COOKIE']}")