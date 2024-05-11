from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    # Add additional settings here if you want to customize the admin interface
    model = MyUser
    list_display = ['username', 'email', 'gender', 'age', 'language']
    search_fields = ['username', 'email']
    # You can add more fields to 'list_display' and 'search_fields' as needed

admin.site.register(MyUser, MyUserAdmin)
