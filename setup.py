from setuptools import setup

setup(
    name='python_claude_web_authenticator',
    version='1.1.2',
    author='Immortal Tapok',
    author_email='irisa1704@gmail.com',
    py_modules=['authenticator', 'dialog'],
    install_requires=['playwright', 'python-dotenv', 'claude-api']
)
