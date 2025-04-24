from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Click
# Register your models here.

# unregiserd
admin.site.unregister(Group)

# mixprof info in2 usr info
class ProfileInline(admin.StackedInline):
    model = Profile

# xtend usr model
class UserAdmin(admin.ModelAdmin):
    model = User
# user fields
    fields = ["username"]
    inlines = [ProfileInline]

# unregi initial usr
admin.site.unregister(User)
# regi user&prfl
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# register clicks
admin.site.register(Click)