from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import CustomUser, Staffs, Students, ta

def student_home(request):
	user = CustomUser.objects.get(id=request.user.id)
	st = Students.objects.get(admin=user)
	context = {
		'student':user,
	}
	return render(request, "student_template/student_home_template.html",context)


def student_profile(request):
	try:
		user = CustomUser.objects.get(id=request.user.id)
	except:
		user = None
	try:
		student = Students.objects.get(admin=user)
	except:
		student = None

	context={
		"user": user,
		"student": student
	}
	return render(request, 'student_template/student_profile.html', context)

def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
 
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
			
            customuser.save()
 
            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
             
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')

def grad_student_fill_accreditation(request):
	stud_obj = Students.objects.get(admin=request.user.id)
	op_obj = ta.objects.filter(student_id = stud_obj.id).first()
	all_faculty = Staffs.objects.filter(institute_to_belong = stud_obj.institute_to_belong).all()
	if not op_obj:
		context = {
			'all_faculty': all_faculty,
		}
		return render(request,"student_template/fill_details.html",context)
	else:
		context = {
			'stud_obj' : op_obj,
			'all_faculty': all_faculty,
		}
		return render(request,"student_template/fill_details.html",context)

def grad_student_fill_acc_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('grad_student_fill_accreditation')
	else:
		name = request.POST.get('name')
		temp = request.POST.get('guide')
		spec = request.POST.get('spec')
		yor = request.POST.get('yor')
		sel = request.POST.get('sel')
		stud_obj = Students.objects.get(admin=request.user.id)
		
		print(stud_obj.admin)
		try:
			op = ta.objects.filter(student_id = stud_obj.id).first()
			if not op:
				kyle = ta()
				#print("hello")
				kyle.name = name
				kyle.guide = guide
				kyle.area_of_work = spec
				kyle.year_of_registration = yor
				kyle.student_id = stud_obj
				kyle.type = sel
				#print("hello")
				kyle.save()
			else:
				if not temp:
					op.name = name
					op.area_of_work = spec
					op.year_of_registration = yor
					op.type = sel
					op.save()
				else:
					guide = Staffs.objects.get(id=temp)
					op.name = name
					op.guide = guide
					op.area_of_work = spec
					op.year_of_registration = yor
					op.type = sel
					op.save()
			messages.success(request, "Details uploaded successfully.")
			return redirect('grad_student_fill_accreditation')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('grad_student_fill_accreditation')

