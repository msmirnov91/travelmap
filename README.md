# Travelmap

Travel data storage

# How to contribute

## Requirements

This project is guaranteed to work with following configuration:

- Ubuntu 24.04.3 LTS
- Python 3.12.3
- Pip 24.0
- psql (PostgreSQL) 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

## Before first run

- Install required packages (Python, Pip, PostgreSQL etc.)
- Clone this repo
- Launch venv using `utils/env_utils/activate_venv.*`
- Apply requirements (`pip3 install -r requirements.txt`)
- Create file named `.env` in the project root (see example below)
- Create DB and user using `utils/db/create_db.py`
- Make initital migration (`python manage.py migrate`)
- Create superuser (`python manage.py createsuperuser`)

## Run and debug

- Make sure venv is active
- Run debug server (`python manage.py runserver <optional:PORT>`), default port is 8000
- Wait for success message in terminal
- Go to http://127.0.0.1:<PORT>/main/ and see hello world page

## Example of .env file

The `.env` file contains secret data, therefore is not present in this repo. It must be created manually.
This file must be located in the root of the project near the `.env.common`, which is just the same configuration
file without any sensitive data. The example of `.env` file with all used keys provided below.

```sh
# Db settings
DB_PASSWORD=some_db_pass
DB_ADMIN_PASSWORD=some_db_admin_pass

# Django settings
DJANGO_DEBUG="True"  # omit this key in production
DJANGO_SECRET_KEY="django-insecure-#=!b%y5c0j&5#+7%=du%++@c=z!@0!jppy#d@_5jnsd8i(#8x6"
```

Secret key can be generated as follows:
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
