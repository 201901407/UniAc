# UniAc (University Accreditation System)
# Created and built by Darshil Parikh
## Steps to install and run University Accreditation System on your machine:
Step 1: Install [Django](https://www.djangoproject.com/download/) and [xhtml2pdf](https://pypi.org/project/xhtml2pdf/). <br/>
Step 2: Install bcrypt library by running the following command in terminal: <br/>
```python -m pip install bcrypt```<br/>
Step 3: Clone this repository in the desired folder by using the following command.<br/>
```git clone https://github.com/201901407/University_accreditation_system.git```<br/>
Step 4: Create a file named .env in the accreditation_system folder.<br/>
Step 5 Add the following environment variables in the .env file:<br/>
`SECRET_KEY = <YOUR_DJANGO_SECRET_KEY>

DEBUG = True/False

ALLOWED_HOSTS = []

POSTGRES_DB_NAME = <NAME_OF_POSTGRES_DATABASE>
POSTGRES_DB_USER = <USERNAME_OF_POSTGRES_DATABASE_USER>

POSTGRES_DB_PASSWORD = <DATABASE_PASSWORD>
POSTGRES_DB_HOST = <HOST_ON_WHICH_POSTGRES_IS_RUNNING> (Can be localhost or some Deployed URL)

POSTGRES_DB_PORT = <PORT_ON_WHICH_DB_IS_ACCESSIBLE>`
<br/>
Step 4: Migrate the schema to the database using the following commands:<br/>
```python manage.py makemigrations``` and then, ```python manage.py migrate```<br/>
Step 5: Now, fire up the development server at 127.0.0.1:8000 using the following command:<br/>
```python manage.py runserver```<br/>
<br/>
<br/>
NOTE: Clear sqlite3 database in order to initiate fresh copy.




