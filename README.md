# Simploo Server

The RESTful API for Simploo.

## Tech Stack

The server was created using the following:

- Python (tested on v3.5.1)

## Setup

**Note**: On Mac machines, every instance of the `python` command must be replaced with `python3`.

1. Create the virtual environment by running `python -m venv env` from the project root).
2. Activate the virtual environment with `env/bin/activate` in Linux,  `env\Scripts\activate.bat` on Windows, or `source env/bin/activate` on Mac.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Create a database called "simploo" in MySQL that can be accessed by a user named "simploo" with the password "password." Alternatively, set up your own database name/credentials and set your `DATABASE_URL` environment variable.
5. Run `python manage.py db upgrade` to create the database.
6. Run `python manage.py runserver` to start the server.

## Environment Variables

There are several environment variables that can be used to configure the application for your local machine.

### Required Variables

- `FACEBOOK_APP_ID` - The APP ID from Facebook for OAuth login.
- `FACEBOOK_APP_SECRET` - The APP Secret from Facebook for OAuth login.

### Optional Variables

- `DATABASE_URL` - Overrides the default database connection URL.
