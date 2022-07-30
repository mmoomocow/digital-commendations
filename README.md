# Digital Commendations

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A digital commendation system being developed for use at Bayfield High School

## Install Instructions

This project uses Python version 3.9.9 which is a prerequisite to install.

### Cloning the repo

Clone the repository using git

```cmd
git clone https://github.com/mmoomocow/digital-commendations.git
```

or download from the [GitHub releases](https://github.com/mmoomocow/digital-commendations/releases)

### Installing the virtual environment

Create a virtual environment using VENV.

```cmd
python -m venv venv
```

### Activate the virtual environment

with windows:

```cmd
<venv path>\Scripts\activate.bat
```

### Install the dependencies

```cmd
pip install -r requirements.txt
```

If you are going to generate dummy data for the database, also install faker

```cmd
pip install faker
```

### Configuration

Create a `.env` file in the root directory of the project and add the following variables:

- ALLOWED_HOSTS - A comma separated list of the allowed hosts

  - Example: *,localhost,www.example.com

- Secret key - A secret key used to encrypt and decrypt data

  - Example: `<random string>`

- DEBUG - A boolean value indicating if the application should be in debug mode

  - Example: True

- ADMINS - A comma separated list of admins who will receive emails for 500 errors

  - Example: `John:johndoe@example.com,Jane:janedoe@example.com`

- MANAGERS - A comma separated list of managers who will receive emails for 404 errors

  - Example: `John:johndoe@example.com,Jane:janedoe@example.com`

- DB_NAME - The name of the MySQL database schema to use

  - Example: `commendations`

- DB_USER - The username to use to connect to the MySQL database

  - Example: `root`

- DB_PASSWORD - The password to use to connect to the MySQL database

  - Example: `password123`

- DB_HOST - The hostname of the MySQL database server

  - Example: `localhost`

- DB_PORT - The port of the MySQL database server

  - Example: `3306`

- CONN_MAX_AGE - The number of seconds a database connection should be kept alive

  - Example: `60`

- KAMAR_AUTH_USERNAME - The username that the Kamar API will use to access the site

  - Example: `Kamar`

- KAMAR_AUTH_PASSWORD - The password that the Kamar API will use to access the site

  - Example: `password`

### Migrate the database

```cmd
python manage.py migrate
```

### Generate dummy data (optional)

```cmd
python manage.py populate_DB
```

### Run the application

```cmd
python manage.py runserver
```

## Development

### New Branches

Branches are used to track changes to the code. When a new branch is created, the name should be in the format of `<name>-DCS-<cardID>`. For example, `Jdoe-DCS-123`. The card ID is taken from the trello board.

### Testing

To test the application, run the following command:

```cmd
python manage.py test
```

As the project is developed, add new tests to the corresponding `tests.py` file.
