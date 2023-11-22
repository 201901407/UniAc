# UniAc (University Accreditation System)
Tired of maintaining bundles and old-school files of accreditation data for submission to NAAC every year? UniAc is freely-available open source digitized repository of storing all accreditation data. UniAc has three access personas in order to govern access to the data namely:
1. Admin/HoD
2. Staff
3. Student

UniAc supports fully automated bulk upload of data from other data sources like Google Sheets and MS Excel. UniAc has interactive charts to visualize the data in an interactive way. UniAc also provides the fuctionality to construct automated PDF reports from the accreditation data which can be directly used for submission.
### The project is live at [UniAc](https://dobbyhacker54.pythonanywhere.com/).
## Steps to install and run University Accreditation System on your machine:
Prerequisites: Python and Pip <br/><br/> 
Step 1: Clone this repository in the desired folder by using the following command.<br/>
```git
git clone https://github.com/201901407/University_accreditation_system.git
```
Step 2: Install all dependencies by running the following command in terminal. <br/>
```python
pip install -r requirements.txt
```
Step 3: Create a file named .env in the accreditation_system folder.<br/>
Step 4: Add the following environment variables in the .env file:<br/>
```python
SECRET_KEY = <YOUR_DJANGO_SECRET_KEY>
DEBUG = True/False
ALLOWED_HOSTS = []
POSTGRES_DB_NAME = <NAME_OF_POSTGRES_DATABASE>
POSTGRES_DB_USER = <USERNAME_OF_POSTGRES_DATABASE_USER>
POSTGRES_DB_PASSWORD = <DATABASE_PASSWORD>
POSTGRES_DB_HOST = <HOST_ON_WHICH_POSTGRES_IS_RUNNING> (Can be localhost or some Deployed URL)
POSTGRES_DB_PORT = <PORT_ON_WHICH_DB_IS_ACCESSIBLE>
```
Step 5: Migrate the schema to the database using the following commands:<br/>
```python
python manage.py makemigrations
``` 
and then, 
```python
python manage.py migrate
```
Step 6: Now, fire up the development server at 127.0.0.1:8000 using the following command:<br/>
```python
python manage.py runserver
```
<br/>
<br/>
<br/>
NOTE: Create fresh PostgreSQL Database for running this application.




