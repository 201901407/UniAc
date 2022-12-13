from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .import HodViews, StaffViews, StudentViews

urlpatterns = [
	path('admin/', admin.site.urls,name="admin"),
	path('', views.home, name="home"),
	path('contact', views.contact, name="contact"),
	path('login', views.loginUser, name="login"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('registration', views.registration, name="registration"),
	path('doLogin', views.doLogin, name="doLogin"),
	path('doRegistration', views.doRegistration, name="doRegistration"),
	path('inreg',views.inreg,name="inreg"),
	path('doInstReg', views.doInstReg, name="doInstReg"),
	
	# URLS for Student
	path('student_home/', StudentViews.student_home, name="student_home"),
	path('student_profile/', StudentViews.student_profile, name="student_profile"),
	path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
	path('grad_student_fill_accreditation/',StudentViews.grad_student_fill_accreditation,name="grad_student_fill_accreditation"),
	path('grad_student_fill_acc_save/',StudentViews.grad_student_fill_acc_save,name="grad_student_fill_acc_save"),

	# URLS for Staff
	path('staff_home/', StaffViews.staff_home, name="staff_home"),
	path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
	path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
	path('staff_fill_accreditation/',StaffViews.staff_fill_accreditation,name="staff_fill_accreditation"),
	path('staff_fill_acc_save',StaffViews.staff_fill_acc_save,name="staff_fill_acc_save"),

	# URL for Admin
	path('admin_home/', HodViews.admin_home, name="admin_home"),
	path('add_staff/', HodViews.add_staff, name="add_staff"),
	path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
	path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
	path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
	path('edit_staff_save/<staff_id>/', HodViews.edit_staff_save, name="edit_staff_save"),
	path('delete_staff/<staff_id>/', HodViews.delete_staff, name="delete_staff"),
	path('add_student/', HodViews.add_student, name="add_student"),
	path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
	path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
	path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
	path('manage_student/', HodViews.manage_student, name="manage_student"),
	path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
	path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
	path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
	path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
	path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
	path('res_proj_details/',HodViews.add_research_project,name="res_proj_details"),
	path('res_proj_details_save/',HodViews.add_research_project_save,name="res_proj_details_save"),
	path('add_comb/',HodViews.add_comb,name="add_comb"),
	path('add_comb_save/',HodViews.add_comb_save,name="add_comb_save"),
	path('staff_print_form/',HodViews.staff_print_form,name="staff_print_form"),
	path('gen_pdf_staff/',HodViews.gen_pdf_staff,name="gen_pdf_staff"),
	path('student_print_form/',HodViews.student_print_form,name="student_print_form"),
	path('gen_pdf_student/',HodViews.gen_pdf_student,name="gen_pdf_student"),
	path('res_print_form/',HodViews.res_print_form,name="res_print_form"),
	path('gen_pdf_res/',HodViews.gen_pdf_res,name="gen_pdf_res"),
	path('iqac_print_form/',HodViews.iqac_print_form,name="iqac_print_form"),
	path('gen_pdf_iqac/',HodViews.gen_pdf_iqac,name="gen_pdf_iqac"),
	path('ta_details/',HodViews.ta_details,name="ta_details"),
	path('ta_print_form/',HodViews.ta_print_form,name="ta_print_form"),
	path('gen_pdf_ta/',HodViews.gen_pdf_ta,name="gen_pdf_ta"),
	path('search_student/',HodViews.search_student,name="search_student"),
	path('search_staff/',HodViews.search_staff,name="search_staff"),
	path('edit_inst/',HodViews.edit_inst,name="edit_inst"),
	path('edit_inst_save/',HodViews.edit_inst_save,name="edit_inst_save"),
	path('view_expense/',HodViews.view_expense,name="view_expense"),
	path('add_expense_save/',HodViews.add_expense_save,name="add_expense_save"),
	path('edit_expense/<expense_id>/',HodViews.edit_expense,name="edit_expense"),
	path('delete_expense/<expense_id>/',HodViews.delete_expense,name="delete_expense"),
	path('edit_expense_save/<expense_id>/',HodViews.edit_expense_save,name="edit_expense_save"),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
