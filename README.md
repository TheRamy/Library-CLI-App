# Library CLI App

Library CLI App is a Python-based library management system that allows you to manage your book collection from the terminal. With this app, you can add books, borrow books, return books, mark them as favorite, and mark them as read.

## One-liner clone, install and run:

    git clone https://github.com/TheRamy/Library-CLI-App.git && cd Library-CLI-App && python3 main.py



## Installation

To use Library CLI App, you will need to install the following pip packages:

- Faker==18.3.1
- inquirer==3.1.3
- psycopg2==2.9.5
- pytz==2022.1
- rich==13.3.3
- typer==0.7.0

You can either use the included requirements file to install them or  allow the main.py file to automatically install it for you. To automatically install the packages, run the following command:

    python3 main.py

This will ask you if you want to install the pip packages in your global environment or inside of a virtual environment.

Alternatively, you can use the requirements file by running the following command:

    pip install -r requirements.txt

## Usage

To use Library CLI App, navigate to the root directory of the project and run the following command:

    python3 main.py


You will be presented with a series of prompts that will guide you through the process of managing your library. For more information on the available commands and their usage, run the --help command:

    python3 main.py --help


## License

Library CLI App is released under the MIT License. See LICENSE for more information.`
