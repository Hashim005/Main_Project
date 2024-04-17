from django.contrib import admin
from . models import Users,Schedule
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display=('username','email','phone_number','role')

admin.site.register(Users,CustomUserAdmin)
admin.site.register(Schedule)
