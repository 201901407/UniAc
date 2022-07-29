from turtle import position, title
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xhtml2pdf import pisa
import json

from .forms import AddStudentForm, EditStudentForm

from .models import CustomUser, Staffs, Students, committee_and_board, research_area,ta


def admin_home(request):
	
	all_student_count = Students.objects.all().count()
	staff_count = Staffs.objects.all().count()
	
	# For Saffs
	staff_name_list=[]

	staffs = Staffs.objects.all()
	for staff in staffs:
		staff_name_list.append(staff.admin.first_name)

	# For Students
	student_name_list=[]

	students = Students.objects.all()
	for student in students:
		student_name_list.append(student.admin.first_name)


	context={
		"all_student_count": all_student_count,
		"staff_count": staff_count,
		"staff_name_list": staff_name_list,
		"student_name_list": student_name_list,
	}
	return render(request, "hod_template/home_content.html", context)


def add_staff(request):
	return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_staff')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		#address = request.POST.get('address')

		try:
			user = CustomUser.objects.create_user(username=username,
												password=password,
												email=email,
												first_name=first_name,
												last_name=last_name,
												user_type=2)
			user.save()
			messages.success(request, "Staff Added Successfully!")
			return redirect('add_staff')
		except:
			messages.error(request, "Failed to Add Staff!")
			return redirect('add_staff')



def manage_staff(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)

	context = {
		"staff": staff,
		"id": staff_id
	}
	return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		staff_id = request.POST.get('staff_id')
		username = request.POST.get('username')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		quali = request.POST.get('quali')
		des = request.POST.get('des')
		area = request.POST.get('area')
		exp = request.POST.get('exp')
		doct = request.POST.get('doct')
		grad = request.POST.get('grad')

		try:
			# INSERTING into Customuser Model
			user = CustomUser.objects.get(id=staff_id)
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.username = username
			user.save()
			
			# INSERTING into Staff Model
			staff_obj = Staffs.objects.get(admin=staff_id)
			staff_obj.qualifications = quali
			staff_obj.designation = des
			staff_obj.area_of_specialisation = area
			staff_obj.experience = exp
			staff_obj.number_of_doctorate_students_guided = doct
			staff_obj.number_of_graduate_students_guided = grad
			staff_obj.save()

			messages.success(request, "Staff Updated Successfully.")
			return redirect('/edit_staff/'+staff_id)

		except:
			messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')


def add_student(request):
	form = AddStudentForm()
	context = {
		"form": form
	}
	return render(request, 'hod_template/add_student_template.html', context)




def add_student_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('add_student')
	else:
		form = AddStudentForm(request.POST, request.FILES)

		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			gender = form.cleaned_data['gender']

			
			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None


			try:
				user = CustomUser.objects.create_user(username=username,
													password=password,
													email=email,
													first_name=first_name,
													last_name=last_name,
													user_type=3)
				user.students.address = address

	

				user.students.gender = gender
				user.students.profile_pic = profile_pic_url
				user.save()
				messages.success(request, "Student Added Successfully!")
				return redirect('add_student')
			except:
				messages.error(request, "Failed to Add Student!")
				return redirect('add_student')
		else:
			return redirect('add_student')


def manage_student(request):
	students = Students.objects.all()
	context = {
		"students": students
	}
	return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):

	# Adding Student ID into Session Variable
	request.session['student_id'] = student_id

	student = Students.objects.get(admin=student_id)
	form = EditStudentForm()
	
	# Filling the form with Data from Database
	form.fields['username'].initial = student.admin.username
	form.fields['first_name'].initial = student.admin.first_name
	form.fields['last_name'].initial = student.admin.last_name
	form.fields['address'].initial = student.address
	
	form.fields['gender'].initial = student.gender
	

	context = {
		"id": student_id,
		"username": student.admin.username,
		"form": form
	}
	return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
	if request.method != "POST":
		return HttpResponse("Invalid Method!")
	else:
		student_id = request.session.get('student_id')
		if student_id == None:
			return redirect('/manage_student')

		form = EditStudentForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			address = form.cleaned_data['address']
			gender = form.cleaned_data['gender']
			

			# Getting Profile Pic first
			# First Check whether the file is selected or not
			# Upload only if file is selected
			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None

			try:
				# First Update into Custom User Model
				user = CustomUser.objects.get(id=student_id)
				user.first_name = first_name
				user.last_name = last_name
				user.username = username
				user.save()

				# Then Update Students Table
				student_model = Students.objects.get(admin=student_id)
				student_model.address = address

				

				student_model.gender = gender
				if profile_pic_url != None:
					student_model.profile_pic = profile_pic_url
				student_model.save()
				# Delete student_id SESSION after the data is updated
				del request.session['student_id']

				messages.success(request, "Student Updated Successfully!")
				return redirect('/edit_student/'+student_id)
			except:
				messages.error(request, "Failed to Uupdate Student.")
				return redirect('/edit_student/'+student_id)
		else:
			messages.error(request,"Please enter the details correctly.")
			print(form.errors)
			return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
	student = Students.objects.get(admin=student_id)
	try:
		student.delete()
		messages.success(request, "Student Deleted Successfully.")
		return redirect('manage_student')
	except:
		messages.error(request, "Failed to Delete Student.")
		return redirect('manage_student')

@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	user_obj = CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username = request.POST.get("username")
	user_obj = CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)

def admin_profile(request):
	user = CustomUser.objects.get(id=request.user.id)

	context={
		"user": user
	}
	return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('admin_profile')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')

		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.first_name = first_name
			customuser.last_name = last_name
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save()
			messages.success(request, "Profile Updated Successfully")
			return redirect('admin_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('admin_profile')
	


def staff_profile(request):
	pass


def student_profile(request):
	pass

def add_research_project(request):
	op = research_area.objects.all()
	context = {
		'research_area':op
	}
	return render(request,'hod_template/fill_res_details.html',context)

def add_research_project_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('res_proj_details')
	else:
		title = request.POST.get('title')
		spron_auth = request.POST.get('sa')
		cost = request.POST.get('cost')
		yc = request.POST.get('yc')
		op = research_area.objects.filter(
			title=title,
			spron_auth=spron_auth,
			cost=cost,
			year_completed=yc,
		)
		if op:
			messages.error(request, "This Project already exists.")
			return redirect('res_proj_details')
		try:
			research_area.objects.create(
				title=title,
				spron_auth=spron_auth,
				cost=cost,
				year_completed=yc,
			)
			messages.success(request, "Details uploaded successfully.")
			return redirect('res_proj_details')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('res_proj_details')

def add_comb(request):
	op = committee_and_board.objects.all()
	context = {
		'cab':op
	}
	return render(request,'hod_template/fill_iqac.html',context)

def add_comb_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('add_comb')
	else:
		name = request.POST.get('name')
		pos = request.POST.get('pos')
		add = request.POST.get('add')
		com = request.POST.get('com')
		op = committee_and_board.objects.filter(
			name=name,
			position=pos,
			address=add,
			committee=com,
		)
		if op:
			messages.error(request, "This Member already exists.")
			return redirect('add_comb')
		try:
			committee_and_board.objects.create(
				name=name,
				position=pos,
				address=add,
				committee=com,
			)
			messages.success(request, "Details uploaded successfully.")
			return redirect('add_comb')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('add_comb')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)

    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

    return response

def gen_pdf_staff(request):
	req_fields = request.POST.getlist('fields[]')
	rec = Staffs.objects.values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def staff_print_form(request):
	return render(request,'hod_template/staff_print_form.html')

def gen_pdf_student(request):
	req_fields = request.POST.getlist('fields[]')
	rec = Students.objects.values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def student_print_form(request):
	return render(request,'hod_template/student_print_form.html')

def gen_pdf_res(request):
	req_fields = request.POST.getlist('fields[]')
	rec = research_area.objects.values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def res_print_form(request):
	return render(request,'hod_template/res_print_form.html')

def gen_pdf_iqac(request):
	req_fields = request.POST.getlist('fields[]')
	rec = committee_and_board.objects.values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def iqac_print_form(request):
	return render(request,'hod_template/iqac_print_form.html')

def ta_details(request):
	ta_det = ta.objects.all()
	context ={
		'ta_det':ta_det,
	}
	return render(request,'hod_template/ta_det.html',context)

def ta_print_form(request):
	return render(request,'hod_template/ta_print_form.html')

def gen_pdf_ta(request):
	req_fields = request.POST.getlist('fields[]')
	rec = ta.objects.values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

