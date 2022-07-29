from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Staffs, Students


def staff_home(request):
	user = CustomUser.objects.get(id=request.user.id)
	st = Staffs.objects.get(admin=user)
	context = {
		'staff':st,
	}
	return render(request, "staff_template/staff_home_template.html",context)


def staff_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	staff = Staffs.objects.get(admin=user)

	context={
		"user": user,
		"staff_obj": staff
	}
	return render(request, 'staff_template/staff_profile.html', context)

def staff_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('staff_profile')
	else:
		name = request.POST.get('name')
		quali = request.POST.get('quali')
		des = request.POST.get('des')
		area = request.POST.get('area')
		exp = request.POST.get('exp')
		doct = request.POST.get('doct')
		grad = request.POST.get('grad')
		staff_obj = Staffs.objects.get(admin=request.user.id)
		print(quali)
		try:
			staff_obj.name=name
			if quali:
				staff_obj.qualifications = quali
			if des:
				staff_obj.designation = des
			staff_obj.area_of_specialisation = area
			staff_obj.experience = exp
			staff_obj.number_of_doctorate_students_guided = doct
			staff_obj.number_of_graduate_students_guided = grad
			staff_obj.save()
			messages.success(request, "Details uploaded successfully.")
			return redirect('staff_profile')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('staff_profile')

def staff_fill_accreditation(request):
	staff_obj = Staffs.objects.get(admin=request.user.id)
	context = {
		"staff_obj":staff_obj
	}
	return render(request,"staff_template/fill_details.html",context)

def staff_fill_acc_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('staff_fill_accreditation')
	else:
		name = request.POST.get('name')
		quali = request.POST.get('quali')
		des = request.POST.get('des')
		area = request.POST.get('area')
		exp = request.POST.get('exp')
		doct = request.POST.get('doct')
		grad = request.POST.get('grad')
		staff_obj = Staffs.objects.get(admin=request.user.id)
		print(quali)
		try:
			staff_obj.name=name
			if quali:
				staff_obj.qualifications = quali
			if des:
				staff_obj.designation = des
			staff_obj.area_of_specialisation = area
			staff_obj.experience = exp
			staff_obj.number_of_doctorate_students_guided = doct
			staff_obj.number_of_graduate_students_guided = grad
			staff_obj.save()
			messages.success(request, "Details uploaded successfully.")
			return redirect('staff_fill_accreditation')
		except:
			messages.error(request, "Failed to upload details.")
			return redirect('staff_fill_accreditation')
		

