#!/usr/bin/env python

from pathlib import Path
from django.core.management.utils import get_random_secret_key
import re


BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILEPATH = next(BASE_DIR.glob("**/settings.py"))
SETTINGS_DIR = SETTINGS_FILEPATH.parent
SETTINGS_DIR_NAME = SETTINGS_DIR.name


definitions = [
    {
        "path": "Procfile",
        "text": f"web: gunicorn {SETTINGS_DIR_NAME}.wsgi",
    },
    {
        "path": "Procfile.windows",
        "text": "web: python manage.py runserver 0.0.0.0:5000",
    },
    {
        "path": "runtime.txt",
        "text": "python-3.10.1",
    },
    {
        "path": "requirements.txt",
        "text": "\n".join(
            [
                "django",
                "django-heroku",
                "djangorestframework",
                "gunicorn",
            ]
        ),
    },
]


def create_files():
    for definition in definitions:
        with open(definition["path"], "w") as f:
            f.write(definition["text"])


def set_secret_key():
    key = get_random_secret_key()
    with open(SETTINGS_FILEPATH, "r") as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        if line.startswith("SECRET_KEY"):
            lines[index] = f'SECRET_KEY = "{key}"\n'
    with open(SETTINGS_FILEPATH, "w") as f:
        f.writelines(lines)


def main():
    create_files()
    set_secret_key()


if __name__ == "__main__":
    main()
