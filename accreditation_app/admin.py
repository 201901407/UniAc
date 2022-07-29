from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, committee_and_board,  Staffs,  Students, ta,research_area
# Register your models here.
class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser, UserModel)
admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Students)

admin.site.register(research_area)
admin.site.register(ta)
admin.site.register(committee_and_board)
