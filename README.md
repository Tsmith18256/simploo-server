# Simploo Server

The RESTful API for Simploo.

## Tech Stack

The server was created using the following:

- _Python_ (tested on v3.5.1)
- _Flask_ framework with _Flask-Script_
- _SQLAlchemy_ (tested with _PyMySQL_)
- _Flask-Migrate_ for database migrations
- _Flask-HTTPAuth_ for access token generation and validation
- _requests_ for sending HTTP requests

## Setup

**Note**: On Mac machines, every instance of the `python` command must be replaced with `python3`.

1. Create the virtual environment by running `python -m venv env` from the project root).
2. Activate the virtual environment with `env/bin/activate` in Linux,  `env\Scripts\activate.bat` on Windows, or `source env/bin/activate` on Mac.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Create a database called "simploo" in MySQL that can be accessed by a user named "simploo" with the password "password." Alternatively, set up your own database name/credentials and set your `DATABASE_URL` environment variable.
5. Run `python manage.py db upgrade` to create the database.
6. Populate the washrooms table in the database by running the seed.sql script.
7. Run `python manage.py runserver` to start the server. (To make the server accessible to other devices, use `python manage.py runserver -h 0.0.0.0`)

## Environment Variables

There are several environment variables that can be used to configure the application for your local machine.

### Required Variables

- `FACEBOOK_APP_ID` - The APP ID from Facebook for OAuth login.
- `FACEBOOK_APP_SECRET` - The APP Secret from Facebook for OAuth login.

### Optional Variables

- `DATABASE_URL` - Overrides the default database connection URL.
- `TEST_DATABASE_URL` - Overrides the default database connection URL for tests.
- `SECRET_KEY` - Override the default secret key for generating access tokens (required for production).

## APIDoc

To use the auto-generated API docs, install apiDoc (`npm install -g apidoc`) and run `apidoc` from the project root.

After you have run the `apidoc` command, the documentation will be in the _doc/_ folder (open the _index.html_ file). You will have to run `apidoc` again each time the API changes for the docs to update.
