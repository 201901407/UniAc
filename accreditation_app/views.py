from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, Staffs, Students, AdminHOD, institute_details
from django.contrib import messages

def home(request):
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')


def loginUser(request):
	return render(request, 'login_page.html')

def doLogin(request):
	
	print("here")
	email_id = request.GET.get('email')
	password = request.GET.get('password')
	# user_type = request.GET.get('user_type')
	print(email_id)
	print(password)
	print(request.user)
	if not (email_id and password):
		messages.error(request, "Please provide all the details!!")
		return render(request, 'login_page.html')

	user = CustomUser.objects.filter(email=email_id,password=password).last()
	op = CustomUser.objects.filter(email=email_id).last()
	if not user and not op.check_password(password):
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login_page.html')

	login(request, user)
	print(request.user)
	print(user.user_type)

	if user.user_type == "student":
		return redirect('student_home/')
	elif user.user_type == "staff":
		return redirect('staff_home/')
	elif user.user_type == "hod":
		return redirect('admin_home/')

	return render(request, 'home.html')

	
def registration(request):
	all_institutes = institute_details.objects.all()
	context = {
		'institutes':all_institutes,
	}
	return render(request, 'registration.html',context)
	

def doRegistration(request):
	first_name = request.GET.get('first_name')
	last_name = request.GET.get('last_name')
	user_type = request.GET.get('user_type')
	email_id = request.GET.get('email')
	institute_name = request.GET.get('institute_name')
	password = request.GET.get('password')
	confirm_password = request.GET.get('confirmPassword')
	all_institutes = institute_details.objects.all()
	context = {
		'institutes':all_institutes,
	}
	print(email_id)
	print(password)
	print(confirm_password)
	print(first_name)
	print(last_name)
	if not (email_id and password and confirm_password and user_type and first_name and last_name):
		messages.error(request, 'Please provide all the details!')
		return render(request, 'registration.html',context)
	
	if password != confirm_password:
		messages.error(request, 'Both passwords should match!!')
		return render(request, 'registration.html',context)

	is_user_exists = CustomUser.objects.filter(email=email_id).exists()

	if is_user_exists:
		messages.error(request, 'User with this email id already exists. Please proceed to login!!')
		return render(request, 'registration.html',context)
	
	inst_obj = institute_details.objects.get(id=institute_name)
	mp = email_id.split('@')[1].split('.')[0]
	if inst_obj.mail_prefix != mp:
		messages.error(request, 'The mail prefix of institute is not valid. Please enter valid mail prefix!')
		return render(request, 'registration.html',context)

	username = email_id.split('@')[0]

	user = CustomUser.objects.create(
	username = username,
	email = email_id,
	password = password,
	user_type = user_type,
	first_name = first_name,
	last_name = last_name,
	)

	user_obj = CustomUser.objects.get(email=email_id)
	if user_type == "staff":
		Staffs.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj,'name':first_name+" "+last_name})
	elif user_type == "student":
		Students.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj})
		print("boom")
	elif user_type == "hod":
		AdminHOD.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj})
	return render(request, 'login_page.html')

	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


def get_user_type_from_email(email_id):
	"""
	Returns CustomUser.user_type corresponding to the given email address
	email_id should be in following format:
	'<username>.<staff|student|hod>@<college_domain>'
	eg.: 'abhishek.staff@jecrc.com'
	"""

	try:
		email_id = email_id.split('@')[0]
		email_user_type = email_id.split('.')[1]
		return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
	except:
		return None

def doInstReg(request):
	name = request.GET.get('name')
	mail_prefix = request.GET.get('mail_prefix')
	institute_type = request.GET.get('institute_type')
	state = request.GET.get('state')

	

	existInst = institute_details.objects.filter(name=name,mail_prefix=mail_prefix,institute_type=institute_type,state=state).exists()
	if existInst:
		messages.error(request,'The institute with following credentials already exists!')
		return render(request,'ireg.html')
	
	issamemp = institute_details.objects.filter(mail_prefix=mail_prefix).exists()
	if issamemp:
		messages.error(request,'The institute with following mail prefix already exists!')
		return render(request,'ireg.html')
	
	institute = institute_details()
	institute.name = name
	institute.mail_prefix = mail_prefix
	institute.institute_type = institute_type
	institute.state = state
	institute.institute_nature = ""
	institute.address = ""
	institute.area = 0
	institute.builtup_area = 0
	institute.city = ""
	institute.pin = 0
	institute.website = ""
	institute.save()
	return render(request,'login_page.html')

def inreg(request):
	return render(request,'ireg.html')