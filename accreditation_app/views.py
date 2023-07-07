from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.forms import ValidationError
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, Staffs, Students, AdminHOD, institute_details
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, password_validators_help_texts
from django.core.validators import validate_email
from .email_ver import account_activation_token
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes, force_str
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import environ, smtplib

env = environ.Env()
environ.Env.read_env()

def home(request):
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')


def loginUser(request):
	return render(request, 'login_page.html')

def doLogin(request):
	
	email_id = request.GET.get('email')
	password = request.GET.get('password')

	if not (email_id and password):
		messages.error(request, "Please provide both username and password!!")
		return render(request, 'login_page.html')
	
	op = CustomUser.objects.filter(email=email_id).last()
	if not op.check_password(password):
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login_page.html')

	login(request, op)

	if op.user_type == "student":
		return redirect('student_home/')
	elif op.user_type == "staff":
		return redirect('staff_home/')
	elif op.user_type == "hod":
		return redirect('admin_home/')

	return render(request, 'home.html')

	
def registration(request):
	all_institutes = institute_details.objects.all()
	obj = NumericPasswordValidator()
	obj2 = MinimumLengthValidator()
	obj3 = CommonPasswordValidator()
	context = {
		'institutes':all_institutes,
		'helptext': password_validators_help_texts([obj, obj2, obj3])
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
	obj = NumericPasswordValidator()
	obj2 = MinimumLengthValidator()
	obj3 = CommonPasswordValidator()
	helptext = password_validators_help_texts([obj, obj2, obj3])
	context = {
		'institutes':all_institutes,
		'helptext': helptext
	}

	
	if not (email_id and password and confirm_password and user_type and first_name and last_name):
		messages.error(request, 'Please provide all the details!!')
		return render(request, 'registration.html',context)
	
	if password != confirm_password:
		messages.error(request, 'Both passwords should match!!')
		return render(request, 'registration.html',context)
	
	try:
		validate_email(email_id)
	except ValidationError as e:
		messages.error(request, 'Please enter valid email address!!')
		return render(request, 'registration.html',context)

	try:
		isValid = validate_password(password, CustomUser, [obj, obj2, obj3])
	except ValidationError:
		messages.error(request, "Please enter valid password!!")
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
	user_type = user_type,
	first_name = first_name,
	last_name = last_name,
	)

	user.set_password(password)
	user.is_active = False
	user.save()

	current_site = get_current_site(request)
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	token = account_activation_token.make_token(user)

	email_message = MIMEMultipart()
	email_message['From'] = str(env('EMAIL_HOST_USER'))
	email_message['To'] = email_id
	email_message['Subject'] = 'Verify your email address for creation of your account in UniAc'
	email_message.attach(MIMEText(render_to_string('email_template.html',{
			'header': "Welcome to UniAc",
			'domain': current_site.domain,
			'uid': uid,
			'token': token,
			'text': "Hi " + first_name + " " + last_name + "! Welcome to UniAc. We are very excited to have you. To finish activating your account please click the link below.",
			'c2a_button':"Activate Account"
		}),"html"))
	
	email_as_string = email_message.as_string()
	smtpObj = smtplib.SMTP(str(env('EMAIL_HOST')),int(env('EMAIL_PORT')))
	smtpObj.starttls()

	smtpObj.login(str(env('EMAIL_HOST_USER')),str(env('EMAIL_HOST_PASSWORD')))
	
	smtpObj.sendmail(str(env('EMAIL_HOST_USER')), email_id, email_as_string)     
	smtpObj.quit()

	user_obj = CustomUser.objects.get(email=email_id)
	if user_type == "staff":
		Staffs.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj,'name':first_name+" "+last_name})
	elif user_type == "student":
		Students.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj})
		print("boom")
	elif user_type == "hod":
		AdminHOD.objects.update_or_create(admin=user_obj,defaults={'institute_to_belong':inst_obj})
	messages.success(request,'An email with the activation link has been sent to your email address. Please follow the steps to activate your account!!')
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

def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = CustomUser.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):  
		print("here")
		user = None  

	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()  
		messages.success(request,"Thank you for your email confirmation. Please proceed to login.")
		return render(request,'login_page.html')

	else:  
		messages.error(request,"Activation link is not valid!!")
		return redirect('registration')  