import os
import base64
import subprocess
import sys
from time import sleep
import venv
import configparser


######################################
######################################
CONFIG_FILE = 'config.ini'
VENV_NAME = "Venv_LibraryCLI"
# Use this for encoding --> https://base64.guru/converter/encode/text ~ramy
config_file_content = 'W2RhdGFiYXNlXSANCg0KaG9zdD1jbGFzczgubXkudG8NCmRhdGFiYXNlPWxpYnJhcnlfY2xpX2FwcCANCnVzZXI9Y2xhc3M4DQpwYXNzd29yZD0xMjMNCg0KDQpbYXBwXQ0KaW5zdGFsbGVkID0gdHJ1ZQ0K'
######################################
######################################


# Check if the file exists
if os.path.exists(CONFIG_FILE):

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Check if the 'app' section exists in the file
    if 'app' in config.sections():
        # Check if the 'installed' option is set to 'true'
        if config.get('app', 'installed') == 'true':
            APP_IS_INSTALLED = True
        else:
            APP_IS_INSTALLED = False
    else:
        APP_IS_INSTALLED = False
else:
    APP_IS_INSTALLED = False


def install_requirements():
    try:
        # Install the requirements using pip
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def install_requirements_in_venv(VENV_NAME=VENV_NAME):

    print("Setting up a virtual environment.")
    # Define the path to the virtual environment
    venv_path = f"./{VENV_NAME}"

    # Create a new virtual environment using venv module
    venv.create(venv_path, with_pip=True)
    print(f"Virtual environment '{VENV_NAME}' created.")

    # The path
    venv_python_path = f"{venv_path}/bin/python"
    if sys.platform == "win32":
        venv_python_path = f"{venv_path}/Scripts/python.exe"

    # Install the requirements.txt insde the venv
    subprocess.run([venv_python_path, "-m", "pip",
                    "install", "-r", "requirements.txt"])
    print(f"Requirements installed successfully in {venv_python_path}")


def install_config_file(file_content=config_file_content):
    # Check if the file already exists
    if os.path.isfile(CONFIG_FILE):
        print(f"{CONFIG_FILE} file already exists.")
    else:

        # Decode from base64 to plain text
        file_content = base64.b64decode(file_content).decode()

        # Write the contents to the file
        with open(CONFIG_FILE, 'w') as configfile:
            configfile.write(file_content)

        print(f'{CONFIG_FILE} file created successfully!')


if not APP_IS_INSTALLED:

    _ = os.system('cls' if os.name == 'nt' else 'clear')  # clear the terminal
    header = '''
██      ██ ██████  ██████   █████  ██████  ██    ██      ██████ ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██  ██  ██      ██      ██      ██ 
██      ██ ██████  ██████  ███████ ██████    ████       ██      ██      ██ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██    ██        ██      ██      ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██    ██         ██████ ███████ ██  
    '''
    print(header)

    Ask = input("""Missing modules and/or database settings file. Do you want to run the setup?
    (Y)es or (N)o? """)

    if Ask == "y" or Ask == "Y":

        print('')
        Ask = input(f"""Do you want to install the pip modules INSIDE of a python virtual env?
(The virtual env will be created automatically in '{VENV_NAME}' folder.)
            (Y)es or (N)o? """)

        # If yes, then install inside venv
        if Ask == "y" or Ask == "Y":

            install_requirements_in_venv()
            install_config_file()
            sleep(2)

        # if no, then install normally without venv
        elif Ask == "n" or Ask == "N":
            install_requirements()
            install_config_file()
            sleep(2)

    else:
        exit()
