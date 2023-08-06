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

	user_type_data = ((HOD, "hod"), (STAFF, "staff"), (STUDENT, "student"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class institute_details(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField(max_length=255)
	address = models.TextField(default="")
	city = models.TextField(default="")
	state = models.TextField(default="")
	pin = models.BigIntegerField(default=0)
	website = models.URLField(max_length=400,default="")
	area = models.BigIntegerField(default=0)
	builtup_area = models.BigIntegerField(default=0)
	recognition_date = models.DateField(default=datetime.date.today)
	campus_type = models.TextField(default="")
	institute_type = models.TextField(default="")
	institute_nature = models.TextField(default="")
	establishment_date = models.DateField(default=datetime.date.today)
	mail_prefix = models.TextField(default="")
	objects = models.Manager()

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
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	gender = models.TextField(max_length=50,default="")
	profile_pic = models.FileField(upload_to='images/',null=True)
	address = models.TextField(default="")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
	def __str__(self):
		return self.admin.username + ": " + str(self.profile_pic)

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
		if instance.user_type == "hod":
			AdminHOD.objects.create(admin=instance)
		if instance.user_type == "staff":
			Staffs.objects.create(admin=instance)
		if instance.user_type == "student":
			Students.objects.create(admin=instance,
									address="",
									profile_pic="",
									gender="")
	

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	if instance.user_type == "hod":
		instance.adminhod.save()
	if instance.user_type == "staff":
		instance.staffs.save()
	if instance.user_type == "student":
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
	objects = models.Manager()

class expenditure_details(models.Model):
	id = models.AutoField(primary_key=True)
	vendor = models.TextField(default="")
	gstnum = models.TextField(default="",max_length=15)
	fiscal_year = models.IntegerField(default=0)
	units = models.BigIntegerField(default=0)
	purpose = models.TextField(default="")
	price_per_unit = models.BigIntegerField(default=0)
	ordering_person = models.ForeignKey(Staffs,on_delete=models.CASCADE,default=1)
	paymode = models.TextField(default="")
	cheque_number = models.TextField(default="")
	total_expense = models.BigIntegerField(default=0)
	objects = models.Manager()

class revenue_details(models.Model):
	id = models.AutoField(primary_key=True)
	source = models.TextField(default="")
	fiscal_year = models.IntegerField(default=0)
	purpose = models.TextField(default="")
	paymode = models.TextField(default="")
	cheque_number = models.TextField(default="")
	total_revenue = models.BigIntegerField(default=0)
	objects = models.Manager()