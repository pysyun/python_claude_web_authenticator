from setuptools import setup

setup(
    name='python_claude_web_authenticator',
    version='1.2.3',
    author='Immortal Tapok',
    author_email='irisa1704@gmail.com',
    py_modules=['authenticator', 'dialog', 'claude_client_override'],
    install_requires=['python-dotenv', 'requests', 'httpx'],
    extras_require={
        'authenticator': ['playwright']
    }
)
