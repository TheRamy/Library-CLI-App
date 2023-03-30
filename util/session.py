
import base64
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

            # here i am decoding the username string with base64 ~ramy
            txt2 = session['username']
            dec = base64.b64decode(txt2.encode('utf-8')).decode('utf-8')

            session['username'] = dec
            return session
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}


def save(session):
    """Saves the session string to the json file. ~ramy"""

    with open(SESSION_FILE, 'w') as f:
        json.dump(session, f)


def login(username):
    """Logging in the user and creating the string(dict) that will be save to the json.
    Returns the session id (which is a random uuid). ~ramy"""

    # here i am encoding the username strin using base64
    # to hide the username from plain view
    # and to prevent users from logging in as other users
    # by editing the json file. ~ramy

    txt = username
    username = base64.b64encode(txt.encode('utf-8')).decode('utf-8')

    session = {'id': str(uuid.uuid4()), 'username': username,
               'timestamp': time.time()}
    save(session)
    return session['id']
