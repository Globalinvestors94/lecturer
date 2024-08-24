from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile,Lecturer_View,Assignment_Answers,Quiz_Answers,Scratch_Pin


admin.site.register(Lecturer_View)
admin.site.register(Assignment_Answers)
admin.site.register(Quiz_Answers)
admin.site.register(Scratch_Pin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'pics', 'phone', 'degree','gender')
admin.site.register(Profile, ProfileAdmin)


# Register your models here.
