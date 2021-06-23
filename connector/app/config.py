from os import environ
from dotenv import load_dotenv

load_dotenv()

# get the list of hosts, empty values filtered out
HOSTS = list(filter(
    lambda x: x != '', map(
        str.strip, environ.get('HOSTS', '').split(','))))

TIMEOUT = int(environ.get('TIMEOUT', 15))
