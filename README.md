**Code was written on Fedora Linux using Python 3.10; should also run on 3.9.**

## Setup

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

./manage.py migrate && ./manage.py runserver
```

To run unit tests:

> ./manage.py test

## Notes

Frontend is rendered entirely in Django templates and HTMX. CSS is rendered with Bootstrap 5.

Code has been formatted using Black, Isort and Flake8.




