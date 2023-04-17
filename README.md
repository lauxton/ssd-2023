# SSD 2023 Prototype
Prototype for The International Space Station (ISS) and NASA by The B Team (Group 2), as part of the Secure Software Development module.

Note: [Dev] indicates that it is relevant for development in relation to the source code. [Tip] is a reminder or helpful hint. If a few different `python` versions are installed, the `python` commands may need to be `python3` or another equivalent instead.

<b>Prerequisites:</b> Python 3.11+

## Initial setup

The initial setup includes creating a virtual environment which in this case is calld `.venv`, then activating the virtual environment, then within the virtual environment, installing the required packages from the `requirements.txt` file. This is performed by running the following commands in a terminal:

 PowerShell
```powershell
python -m venv ./.venv
./.venv/scripts/Activate.ps1
pip install -r requirements.txt
```
Bash
```bash
sudo apt update
sudo apt install python3.10-venv
python3 -m venv foo_env
source foo_env/bin/activate
pip3 install -r requirements.txt
```
[Tip] Always make sure to activate the virtual environment before running any other commands:

Powershell
```powershell
./.venv/scripts/Activate.ps1
```
Bash
```bash
source foo_env/bin/activate
```
[Tip] If running Linux, make sure to have Django downloaded onto your virtual environment, and to have downloaded django-cryptography and django-csp before trying to migrate the server (Matthes, 2021; crypto, xxxx; csp, xxxx).

Bash
```bash
pip3 install django
pip3 install django-cryptography
pip3 install django-csp
```

Run initial migrations and start server:

Powershell
```powershell
cd ssd2023
python manage.py migrate
python manage.py runserver
```
Bash
```bash
cd ssd2023
python3 manage.py migrate
python3 manage.py runserver
```

### [Dev] Database migrations

Every time there are changes to the models that need to be propagated into the database, run the following commands:

Powershell
```powershell
python manage.py makemigrations missions
python manage.py migrate
```
Bash
```bash
python3 manage.py makemigrations missions
python manage.py migrate
```
### Database
To log in to the backend database, a super user needs to be created:

Powershell
```powershell
python manage.py createsuperuser
```
Bash
```bash
python3 manage.py createsuperuser
```

Backend database (accessible via `http://localhost:8000/admin`)

![Django admin log in page](./screenshots/django-admin.png)


## User credentials
Although it is more secure to share credentials via a password manager such as LastPass (2023), for the purpose of testing this prototype, two sample users' login credentials has been included in the table below. Their (and other users') details can be modified (e.g. resetting passwords) in the backend database when logged in as the superuser, which was created in an earlier step. 

|    Username   |    Password   |  User (Employee) Type  |
|---------------|:-------------:|:----------------------:|
|  justin.thyme |    password   |       ISS Admin        |
|   sam.widge   |    password   |       NASA Admin       |


## User Interface
Navigate to `http://localhost:8000/` on a browser (e.g. Edge, Chrome). Below are screenshots of the ISS and NASA prototype website user interface. The following is an example for the ISS Admin user Justin Thyme (username: justin.thyme).

Log in page 
![Log in page](./screenshots/login.png)

Logging in with username justin.thyme
![Login with username justin.thyme](./screenshots/login-with-justin.png)

Home page view as an authenticated user (Justin Thyme) 
![Home page after logging in as user Justin Thyme](./screenshots/justin-user-view.png)

Create mission
![Create mission page as an ISS Admin](./screenshots/create-mission.png)

Manage mission and optional generate report
![Manage mission and optional generate report page](./screenshots/justin-user-manage-mission-optional-generate-report.png)

## Source code linter (Pylint)
The `pylint` linter is used to analyse the source code.

Output result of the `ssd2023` module:
```powershell
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.81/10, +0.19)
```

Output result of the `missions` module:
```powershell
```

## Testing
To run the unit and integration tests:

```powershell
python manage.py test
```
```bash
python3 manage.py test
'''

Output of the tests:
```powershell
Found 13 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............
----------------------------------------------------------------------
Ran 13 tests in 17.343s

OK
Destroying test database for alias 'default'...
```

# References
* https://docs.djangoproject.com/en/4.2/intro/tutorial01/
* https://docs.djangoproject.com/en/4.1/topics/forms/
* https://learndjango.com/tutorials/django-login-and-logout-tutorial
* LastPass (2023) https://www.lastpass.com/
* https://pypi.org/project/pylint/
* https://pypi.org/project/django-cryptography/
