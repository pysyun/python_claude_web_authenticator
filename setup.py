from setuptools import setup

setup(
    name='python_claude_web_authenticator',
    version='1.1.1',
    author='Immortal Tapok',
    author_email='immortaltapok@lineardev.net',
    py_modules=['authenticator', 'connect'],
    install_requires=['playwright', 'python-dotenv', 'claude-api']
)
