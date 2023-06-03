# UniAc (University Accreditation System)
# Created and built by Darshil Parikh
## Steps to install and run University Accreditation System on your machine:
Step 1: Install [Django](https://www.djangoproject.com/download/) and [xhtml2pdf](https://pypi.org/project/xhtml2pdf/). <br/>
Step 2: Install bcrypt library by running the following command in terminal: <br/>
```python -m pip install bcrypt```
Step 3: Clone this repository in the desired folder by using the following command.<br/>
```git clone https://github.com/201901407/University_accreditation_system.git```
Step 4: Create a file named .env in the accreditation_system folder.
Step 5 Add the following environment variables in the .env file:
```SECRET_KEY = <YOUR_SECRET_KEY> <br/>```
Step 4: Migrate the schema to the database using the following commands:<br/>
```python manage.py makemigrations``` and then, ```python manage.py migrate```<br/>
Step 5: Now, fire up the development server at 127.0.0.1:8000 using the following command:<br/>
```python manage.py runserver```<br/>
<br/>
<br/>
NOTE: Clear sqlite3 database in order to initiate fresh copy.




