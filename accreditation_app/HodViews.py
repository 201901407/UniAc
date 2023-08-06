from ast import keyword
from datetime import datetime
from distutils.log import error
from turtle import position, title
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count,Sum
import json

from .forms import AddStudentForm, EditStudentForm

from .models import CustomUser, Staffs, Students, committee_and_board, research_area,ta,AdminHOD,institute_details,expenditure_details,revenue_details


def admin_home(request):
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
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

	exp_det_year = []
	exp_det = []
	y_exp = expenditure_details.objects.all()
	op_exp = y_exp.values('fiscal_year').annotate(dcount = Sum('total_expense')).order_by()
	
	for i in op_exp:
		exp_det_year.append(i['fiscal_year'])
		exp_det.append((i['dcount']))
	print(op_exp)

	rev_det_year = []
	rev_det = []
	yr_exp = revenue_details.objects.all()
	opr_exp = yr_exp.values('fiscal_year').annotate(dcount = Sum('total_revenue')).order_by()

	for i in opr_exp:
		rev_det_year.append(i['fiscal_year'])
		rev_det.append((i['dcount']))
	
	pro_det = []
	for i in range(len(rev_det)):
		pro_det.append(rev_det[i]-exp_det[i])
	context={
		"all_student_count": all_student_count,
		"staff_count": staff_count,
		"staff_name_list": staff_name_list,
		"student_name_list": student_name_list,
		"exp_det_year":exp_det_year,
		"exp_det":exp_det,
		"rev_det_year":rev_det_year,
		"rev_det":rev_det,
		"pro_det":pro_det,
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
		admin_obj = AdminHOD.objects.get(admin=request.user.id)

		op = CustomUser.objects.filter(email=email).exists()
		isboth = CustomUser.objects.filter(email=email,username=username).exists()
		isuser = CustomUser.objects.filter(username=username).exists()

		if op or isboth or isuser:
			messages.error(request, "Staff with following credentials already exists!")
			return redirect('add_staff')

		mp = institute_details.objects.all().first()
		pref = email.split('@')[1].split('.')[0]

		if pref != mp.mail_prefix:
			messages.error(request, "Please enter valid e-mail ID!!")
			return redirect('add_staff')


		try:
			user = CustomUser.objects.create(username=username,
												password=password,
												email=email,
												first_name=first_name,
												last_name=last_name,
												user_type="staff")
			user.save()
			admin_obj = AdminHOD.objects.get(admin=request.user.id)
			staff_obj = Staffs.objects.get(admin=user.id)
			staff_obj.name = first_name+" "+last_name
			staff_obj.save()
			messages.success(request, "Staff Added Successfully!")
			return redirect('add_staff')
		except:
			messages.error(request, "Failed to Add Staff!")
			return redirect('add_staff')



def manage_staff(request):
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
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


def edit_staff_save(request,staff_id):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		print("kop")
		username = request.POST.get('username')
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
			print("kop")
			user = CustomUser.objects.get(id=staff_id)
			print("kop")
			user.first_name = first_name
			user.last_name = last_name
			user.username = user.username
			user.password = user.password
			print("kop")
			user.save()
			print("kop")
			# INSERTING into Staff Model
			staff_obj = Staffs.objects.get(admin=staff_id)
			print("kop")
			if quali is None:
				quali = staff_obj.qualifications
			if des is None:
				des = staff_obj.designation
			#staff_obj.name = staff_obj.name
			staff_obj.qualifications = quali
			staff_obj.designation = des
			staff_obj.area_of_specialisation = area
			staff_obj.experience = exp
			staff_obj.number_of_doctorate_students_guided = doct
			staff_obj.number_of_graduate_students_guided = grad
			print(des)
			staff_obj.save()
			print("kop")
			messages.success(request, "Staff Updated Successfully.")
			return redirect('/edit_staff/'+staff_id)
		except:
			messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)
	user = CustomUser.objects.get(id=staff_id)
	try:
		staff.delete()
		user.delete()
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
		
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		address = request.POST.get('address')
		gender = request.POST.get('gender')
		admin_obj = AdminHOD.objects.get(admin=request.user.id)

		if not first_name or not last_name or not username or not email or not password:
			messages.error(request, "Please fill all fields!")
			return redirect('add_student')

		op = CustomUser.objects.filter(email=email).exists()
		isboth = CustomUser.objects.filter(email=email,username=username).exists()
		isuser = CustomUser.objects.filter(username=username).exists()

		if op or isboth or isuser:
			messages.error(request, "Student with following credentials already exists!")
			return redirect('add_student')

		if len(request.FILES) != 0:
			profile_pic = request.FILES['profile_pic']
			fs = FileSystemStorage()
			filename = fs.save(profile_pic.name, profile_pic)
			profile_pic_url = fs.url(filename)
			print("lfvoprm")
		else:
			profile_pic_url = None


		try:
			#print("letsgo")
			print(password)
			user = CustomUser.objects.create(username=username,
													password=password,
													email=email,
													first_name=first_name,
													last_name=last_name,
													user_type="student")
			user.save()
			user.students.address = address
			user.students.gender = gender
			user.students.profile_pic = profile_pic_url
			user.save()
			messages.success(request, "Student Added Successfully!")
			return redirect('add_student')
		except:
			messages.error(request, "Failed to Add Student!")
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
				user.username = user.username
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
				messages.error(request, "Failed to Update Student.")
				return redirect('/edit_student/'+student_id)
		else:
			messages.error(request,"Please enter the details correctly.")
			print(form.errors)
			return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
	student = Students.objects.get(admin=student_id)
	user = CustomUser.objects.get(id = student_id)
	try:
		student.delete()
		user.delete()
		messages.success(request, "Student Deleted Successfully.")
		return redirect('manage_student')
	except:
		messages.error(request, "Failed to Delete Student.")
		return redirect('manage_student')

@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	mp = institute_details.objects.all().first()
	pref = email.split('@')[1].split('.')[0]
	print(pref)
	if pref != mp.mail_prefix:
		return HttpResponse(True)
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
				customuser.password = password
			customuser.save()
			messages.success(request, "Profile Updated Successfully!")
			return redirect('admin_profile')
		except:
			messages.error(request, "Failed to Update Profile!")
			return redirect('admin_profile')
	


def staff_profile(request):
	pass


def student_profile(request):
	pass

def add_research_project(request):
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
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
		admin_obj = AdminHOD.objects.get(admin=request.user.id)
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
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
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
		admin_obj = AdminHOD.objects.get(admin=request.user.id)
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
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = Staffs.objects.all().values(*req_fields)
	req_headers = request.POST.getlist('headers[]')
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
		'headers':req_headers,
	})

def staff_print_form(request):
	return render(request,'hod_template/staff_print_form.html')

def gen_pdf_student(request):
	req_fields = request.POST.getlist('fields[]')
	q_list = request.POST.getlist('genderq')
	if len(q_list) == 0:
		q_list.append("male")
		q_list.append("female")
	for f in req_fields:
		if f == "adminname":
			f = "admin.name"
		elif f == "adminemail":
			f = "admin.email"
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = Students.objects.filter(gender__in = q_list).values(*req_fields)
	req_headers = request.POST.getlist('headers[]')
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
		'headers':req_headers,
	})

def student_print_form(request):
	return render(request,'hod_template/student_print_form.html')

def gen_pdf_res(request):
	req_fields = request.POST.getlist('fields[]')
	rec = research_area.objects.all().values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def res_print_form(request):
	return render(request,'hod_template/res_print_form.html')

def gen_pdf_iqac(request):
	req_fields = request.POST.getlist('fields[]')
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = committee_and_board.objects.all().values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def iqac_print_form(request):
	return render(request,'hod_template/iqac_print_form.html')

def ta_details(request):
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	ta_det = ta.objects.all()
	context ={
		'ta_det':ta_det,
	}
	return render(request,'hod_template/ta_det.html',context)

def ta_print_form(request):
	return render(request,'hod_template/ta_print_form.html')

def gen_pdf_ta(request):
	req_fields = request.POST.getlist('fields[]')
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = ta.objects.all().values(*req_fields)
	return render_to_pdf('hod_template/pdf.html',
	{
		'record':rec,
	})

def search_student(request):
	keyword = request.POST.get("table_search")
	""" count = 0
	print(keyword)
	for i in keyword:
		count = count + 1
		print(i)
	if count == 0:
		keyword.append(" ")
		keyword.append(" ")
	if count == 1:
		keyword.append(" ") """
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = Students.objects.filter(admin__first_name__contains = keyword)
	context = {
		"students": rec
	}
	return render(request, 'hod_template/manage_student_template.html', context)

def search_staff(request):
	keyword = request.POST.get("table_search")
	""" count = 0
	print(keyword)
	for i in keyword:
		count = count + 1
		print(i)
	if count == 0:
		keyword.append(" ")
		keyword.append(" ")
	if count == 1:
		keyword.append(" ") """
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	rec = Staffs.objects.filter(admin__first_name__contains = keyword)
	context = {
		"staffs": rec
	}
	return render(request, 'hod_template/manage_staff_template.html', context)

def edit_inst(request):
	inst_det = institute_details.objects.all().first()
	context = {
		"inst_det":inst_det,
	}
	return render(request,'hod_template/edit_institute.html',context)

def edit_inst_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('edit_inst')
	else:
		name = request.POST.get('name')
		address = request.POST.get('address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		pin = request.POST.get('pin')
		website = request.POST.get('website')
		area = request.POST.get('area')
		builtup_area = request.POST.get('builtup_area')
		recognition_date = request.POST.get('recognition_date')
		campus_type = request.POST.get('campus_type')
		institute_type = request.POST.get('institute_type')
		institute_nature = request.POST.get('institute_nature')
		establishment_date = request.POST.get('establishment_date')
		mail_prefix = request.POST.get('mail_prefix')
		
		if not recognition_date or not establishment_date: 
			messages.error(request, "Please fill all details!")
			return redirect('edit_inst')
		
		if establishment_date > datetime.now().date().strftime("%Y-%m-%d") or recognition_date > datetime.now().date().strftime("%Y-%m-%d"):
			messages.error(request, "Recognition and Establishment Dates should be before current date!")
			return redirect('edit_inst')

		admin_obj = AdminHOD.objects.get(admin=request.user.id)
		#inst_det = institute_details.objects.get(id = admin_obj.institute_to_belong.id)
		try:
			inst_det = institute_details.objects.all().first()
			
			inst_det.name = name
			inst_det.address = address
			inst_det.city = city
			
			#inst_det.state = state
			inst_det.pin = pin
			inst_det.website = website
			
			inst_det.area = area
			inst_det.builtup_area = builtup_area
			inst_det.recognition_date = datetime.strptime(recognition_date,"%Y-%m-%d").date()
			
			inst_det.campus_type = campus_type
			
			inst_det.institute_nature = institute_nature
			
			inst_det.establishment_date = datetime.strptime(establishment_date,"%Y-%m-%d").date()
			#inst_det.mail_prefix = mail_prefix
			
			inst_det.save()

			messages.success(request, "Details uploaded successfully.")
			return redirect('edit_inst')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('edit_inst')

def view_expense(request):
	#admin_obj = AdminHOD.objects.get(admin=request.user.id)
	exp_det = expenditure_details.objects.all()
	all_fac = Staffs.objects.all()
	context = {
		'expense':exp_det,
		'all_fac':all_fac,
	}
	return render(request,'hod_template/manage_expense.html',context)

def add_expense_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('view_expense')
	else:
		vendor = request.POST.get('vendor')
		gstnum = request.POST.get('gstnum')
		purpose = request.POST.get('purpose')
		unit = request.POST.get('units')
		ppu = request.POST.get('price_per_unit')
		op = request.POST.get('ordering_person')
		pm = request.POST.get('paymode')
		cn = request.POST.get('cheque_number')

		if int(ppu) <= 0:
			messages.error(request, "Price must be non-zero positive value!")
			return redirect('view_expense')
		
		if int(unit) <= 0:
			messages.error(request, "Number of Units must be non-zero positive value!")
			return redirect('view_expense')
		
		admin_obj = AdminHOD.objects.get(admin=request.user.id)
		curr_date = datetime.now().date().strftime("%Y")
		try:
			kop = Staffs.objects.filter(id=op).first()
			print(kop.name)
			exp_det = expenditure_details.objects.update_or_create(
				vendor = vendor,
				gstnum = gstnum,
				fiscal_year = int(curr_date),
				units = int(unit),
				purpose = purpose,
				price_per_unit = int(ppu),
				ordering_person = kop,
				paymode = pm,
				cheque_number = cn,
				total_expense = int(unit)*int(ppu),
			)

			#exp_det.save()
			messages.success(request, "Expense Record added Successfully!")
			return redirect('view_expense')
		except:
			messages.error(request, "Failed to add expense record.")
			return redirect('view_expense')

def edit_expense(request,expense_id):
	exp_obj = expenditure_details.objects.filter(id=expense_id).first()
	#admin_obj = AdminHOD.objects.get(admin=request.user.id)
	all_fac = Staffs.objects.all()
	context = {
		'row':exp_obj,
		'all_fac':all_fac,
	}
	return render(request,'hod_template/edit_expense.html',context)

def edit_expense_save(request,expense_id):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('/edit_expense/'+expense_id)
	else:
		vendor = request.POST.get('vendor')
		gstnum = request.POST.get('gstnum')
		purpose = request.POST.get('purpose')
		unit = request.POST.get('units')
		ppu = request.POST.get('price_per_unit')
		op = request.POST.get('ordering_person')
		pm = request.POST.get('paymode')
		cn = request.POST.get('cheque_number')

		if int(ppu) <= 0:
			messages.error(request, "Price must be non-zero positive value!")
			return redirect('/edit_expense/'+expense_id)
		
		if int(unit) <= 0:
			messages.error(request, "Number of Units must be non-zero positive value!")
			return redirect('/edit_expense/'+expense_id)
		
		if pm is None:
			temp = expenditure_details.objects.filter(id=expense_id).first()
			pm = temp.paymode
		
		if op is None:
			temp = expenditure_details.objects.filter(id=expense_id).first()
			op = temp.ordering_person.id

		admin_obj = AdminHOD.objects.get(admin=request.user.id)
		curr_date = datetime.now().date().strftime("%Y")
		try:
			kop = Staffs.objects.filter(id=op).first()
	
			exp_det = expenditure_details.objects.update_or_create(
				id = expense_id,defaults={
				'vendor':vendor,
				'gstnum': gstnum,
				'units' : int(unit),
				'purpose' : purpose,
				'price_per_unit' : int(ppu),
				'ordering_person' : kop,
				'paymode' : pm,
				'cheque_number' : cn,
				'total_expense' : int(unit)*int(ppu),
				}
			)
			
			#exp_det.save()
			messages.success(request, "Expense Record updated Successfully!")
			return redirect('/edit_expense/'+expense_id)
		except:
			messages.error(request, "Failed to update expense record.")
			return redirect('/edit_expense/'+expense_id)

def delete_expense(request,expense_id):
	exp_det = expenditure_details.objects.get(id=expense_id)
	try:
		exp_det.delete()
		messages.success(request, "Expense record Deleted Successfully.")
		return redirect('view_expense')
	except:
		messages.error(request, "Failed to Delete the record.")
		return redirect('view_expense')


def view_revenue(request):
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	exp_det = revenue_details.objects.all()
	context = {
		'expense':exp_det,
	}
	return render(request,'hod_template/manage_revenue.html',context)


def add_revenue_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('view_revenue')
	else:
		source = request.POST.get('source')
		purpose = request.POST.get('purpose')
		pm = request.POST.get('paymode')
		cn = request.POST.get('cheque_number')
		rvobt = request.POST.get('rvobt')

		if int(rvobt) <= 0:
			messages.error(request, "Price must be non-zero positive value!")
			return redirect('view_revenue')
		
		#admin_obj = AdminHOD.objects.get(admin=request.user.id)
		curr_date = datetime.now().date().strftime("%Y")
		try:
			exp_det = revenue_details.objects.update_or_create(
				source = source,
				fiscal_year = int(curr_date),
				purpose = purpose,
				paymode = pm,
				cheque_number = cn,
				total_revenue = int(rvobt),
			)

			exp_det.save()
			messages.success(request, "Revenue Record added Successfully!")
			return redirect('view_revenue')
		except:
			messages.error(request, "Failed to add Revenue record.")
			return redirect('view_revenue')

def delete_revenue(request,revenue_id):
	exp_det = revenue_details.objects.get(id=revenue_id)
	try:
		exp_det.delete()
		messages.success(request, "Revenue record Deleted Successfully.")
		return redirect('view_revenue')
	except:
		messages.error(request, "Failed to Delete the record.")
		return redirect('view_revenue')

def edit_revenue(request,revenue_id):
	exp_obj = revenue_details.objects.filter(id=revenue_id).first()
	admin_obj = AdminHOD.objects.get(admin=request.user.id)
	context = {
		'row':exp_obj,
	}
	return render(request,'hod_template/edit_revenue.html',context)

def edit_revenue_save(request,revenue_id):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('/edit_revenue/'+revenue_id)
	else:
		source = request.POST.get('source')
		purpose = request.POST.get('purpose')
		pm = request.POST.get('paymode')
		cn = request.POST.get('cheque_number')
		rvobt = request.POST.get('rvobt')

		if int(rvobt) <= 0:
			messages.error(request, "Price must be non-zero positive value!")
			return redirect('/edit_revenue/'+revenue_id)
	
		
		if source is None:
			temp = revenue_details.objects.filter(id=revenue_id).first()
			source = temp.source
		
		if pm is None:
			temp = revenue_details.objects.filter(id=revenue_id).first()
			pm = temp.paymode

		admin_obj = AdminHOD.objects.get(admin=request.user.id)
		curr_date = datetime.now().date().strftime("%Y")
		try:
			
			exp_det = revenue_details.objects.update_or_create(
				id = revenue_id,defaults={
				'source':source,
				'purpose' : purpose,
				'paymode' : pm,
				'cheque_number' : cn,
				'total_revenue' : int(rvobt),
				}
			)
			
			#exp_det.save()
			messages.success(request, "Revenue Record updated Successfully!")
			return redirect('/edit_revenue/'+revenue_id)
		except:
			messages.error(request, "Failed to update revenue record.")
			return redirect('/edit_revenue/'+revenue_id)