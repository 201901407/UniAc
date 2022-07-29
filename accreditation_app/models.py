from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator,MinValueValidator 


# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
	HOD = '1'
	STAFF = '2'
	STUDENT = '3'
	
	EMAIL_TO_USER_TYPE_MAP = {
		'hod': HOD,
		'staff': STAFF,
		'student': STUDENT
	}

	user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	name = models.TextField(max_length=255,default="")
	qualifications = models.TextField(max_length=1000,default="")
	designation = models.TextField(max_length=255,default="")
	area_of_specialisation = models.CharField(max_length=1000,default="")
	experience = models.IntegerField(default=0) 
	number_of_doctorate_students_guided = models.BigIntegerField(default=0)
	number_of_graduate_students_guided = models.BigIntegerField(default=0)
	#address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	gender = models.CharField(max_length=50,default="")
	profile_pic = models.FileField(default="")
	address = models.TextField(default="")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class ta(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students,on_delete=models.CASCADE,default=1)
	name = models.TextField(max_length=255)
	guide = models.ForeignKey(Staffs,on_delete=models.CASCADE,default=1)
	area_of_work = models.TextField(max_length=1000)
	year_of_registration = models.IntegerField(validators=[MinValueValidator(2002),MaxValueValidator(datetime.date.today().year)])
	type = models.CharField(max_length=255)
	objects = models.Manager()

#Creating Django Signals
@receiver(post_save, sender=CustomUser)

# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
	# if Created is true (Means Data Inserted)
	if created:
	
		# Check the user_type and insert the data in respective tables
		if instance.user_type == 1:
			AdminHOD.objects.create(admin=instance)
		if instance.user_type == 2:
			Staffs.objects.create(admin=instance)
		if instance.user_type == 3:
			Students.objects.create(admin=instance,
									address="",
									profile_pic="",
									gender="")
	

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	if instance.user_type == 1:
		instance.adminhod.save()
	if instance.user_type == 2:
		instance.staffs.save()
	if instance.user_type == 3:
		instance.students.save()

class research_area(models.Model):
	id = models.AutoField(primary_key=True)
	year_completed = models.IntegerField(validators=[MinValueValidator(1999),MaxValueValidator(datetime.date.today().year)])
	title = models.TextField(max_length=1000)
	spron_auth = models.TextField(max_length=255)
	cost = models.BigIntegerField(default=1,validators=[MinValueValidator(1)])
	objects = models.Manager()

class committee_and_board(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField(max_length=255)
	position = models.TextField(max_length=255)
	address = models.CharField(max_length=600)
	committee = models.CharField(max_length=255)