# SSD 2023 Prototype
Prototype for The International Space Station (ISS) and NASA by The B Team (Group 2), as part of the Secure Software Development module.

Note: [Dev] indicates that it is relevant for development in relation to the source code. [Tip] is a reminder or helpful hint. If a few different `python` versions are installed, the `python` commands may need to be `python3` or another equivalent instead.

<b>Prerequisites:</b> Python 3.11+

## Initial setup

The initial setup includes creating a virtual environment which in this case is calld `.venv`, then activating the virtual environment, then within the virtual environment, installing the required packages from the `requirements.txt` file. This is performed by running the following commands in a terminal such as Windows PowerShell or bash:

```powershell
python -m venv ./.venv
./.venv/scripts/Activate.ps1
pip install -r requirements.txt
```

[Tip] Always make sure to activate the virtual environment before running any other commands:

```powershell
./.venv/scripts/Activate.ps1
```

Run initial migrations and start server:

```powershell
cd ssd2023
python manage.py migrate
python manage.py runserver
```

To log in to the backend database via `http://localhost:8000/admin`, a super user needs to be created:

```powershell
python manage.py createsuperuser
```

## [Dev] Database migrations

Every time there are changes to the models that need to be propagated into the database, run the following commands:

```powershell
python manage.py makemigrations missions
python manage.py migrate
```

## Testing
To run the unit and integration tests:

```powershell
python manage.py test
```

# References
* https://docs.djangoproject.com/en/4.2/intro/tutorial01/
* https://docs.djangoproject.com/en/4.1/topics/forms/
* https://learndjango.com/tutorials/django-login-and-logout-tutorial