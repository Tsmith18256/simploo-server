# Simploo Server

The RESTful API for Simploo.

## Tech Stack

The server was created using the following:

- Python (tested on v3.5.1)

## Setup

1. Create the virtual environment by running `python -m venv env` from the project root.
2. Activate the virtual environment with `env/bin/activate` in Bash, or `env\Scripts\activate.bat` on Windows.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Create a database called "simploo" in MySQL that can be accessed by a user named "simploo" with the password "password." Alternatively, set up your own database name/credentials and set your `DATABASE_URL` environment variable.
5. Run `python manage.py db upgrade` to create the database.
6. Run `python manage.py runserver` to start the server.