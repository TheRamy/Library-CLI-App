import time
import uuid
import json

SESSION_FILE = 'cookie.json'


def load():
    """Loads the session IF its not timed out already. ~ramy"""

    try:  # To catch any errors if the file is not there. ~ramy
        with open(SESSION_FILE, 'r') as f:
            session = json.load(f)
        timestamp = session.get('timestamp', 0)
        timeout_minutes = 5
        if time.time() - timestamp < timeout_minutes * 60:
            return session
    except FileNotFoundError:
        pass
    return {}


def save(session):
    """Saves the session string to the json file. ~ramy"""

    with open(SESSION_FILE, 'w') as f:
        json.dump(session, f)


def login(username):
    """Logging in the user and creating the string(dict) that will be save to the json.
    Returns the session id (which is a random uuid). ~ramy"""

    session = {'id': str(uuid.uuid4()), 'username': username,
               'timestamp': time.time()}
    save(session)
    return session['id']
