import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Optional

import util.db


console = Console()


def cli_add_user(username):
    """Displays the cli interface when signing up. ~ramy"""

    user_exist = util.db.sql_select(
        f"SELECT * from users WHERE user_name = '{username}'")

    if user_exist:
        typer.secho(f'Username {username} is NOT available!', fg='red')
    else:

        typer.secho(f"Username '{username}' is available!", fg='green')
        pwd = console.input('Enter your password: ', password=True)
        pwd2 = console.input('Enter your password (again): ', password=True)

        if pwd == pwd2:

            sql = f"INSERT INTO users (user_name, user_password) VALUES('{username}', '{pwd2}')"
            add_user = util.db.sql_insert(sql)
            typer.secho(f'Signup complete! You may login!', fg='green')
            return add_user
        else:
            typer.secho(f'password doesnt match. Try again.', fg='red')


def cli_login(username, password):
    """Displays the cli interface whe loging in a user. ~ramy"""

    user = util.db.sql_select(
        f"SELECT * from users WHERE user_name = '{username}'")

    if user:
        user_password = user[0][2]

        if password == user_password:  # Check if the password match the one in the database
            typer.secho(f'Logged in! Welcome back {username}!', fg='green')
            return username
        else:
            typer.secho(
                f'The password for user {username} is incorrect!', fg='red')
            return False

    else:

        typer.secho(f'Username {username} does not exist.', fg='red')
        return False
