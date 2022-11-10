# UniAc (University Accreditation System)
# Created and built by Darshil Parikh
## Steps to install and run University Accreditation System on your machine
Step 1: Install Django. <br/>
Step 2: Create a folder with name University_accreditation_system and open it with VS Code.<br/>
Step 3: Open the terminal and create a new project “Accreditation_system” using the below command.<br/>
``` django-admin startproject Accreditation_system```<br/>
Step 4: Enter inside the folder “Accreditation_system” and create the app “accreditation_app”.<br/>
```python manage.py startapp accreditation_app```<br/>
Step 5: Go to Accreditation_system -> settings.py -> INSTALLED_APPS and add our app ‘accreditation_app’.<br/>
Step 6: Go to urls.py of Accreditation_system and add the below path in urlpatterns.<br/>
```path('', include('accreditation_app.urls'))```<br/>
Step 7: Now clone and import the respective files and folders in your app.<br/>
Step 8: Migrate the schema to the database using the following commands:<br/>
```python manage.py makemigrations``` and then, ```python manage.py migrate```<br/>
Step 9: Now, fire up the development server at 127.0.0.1:8000 using the following command:<br/>
```python manage.py runserver```<br/>


