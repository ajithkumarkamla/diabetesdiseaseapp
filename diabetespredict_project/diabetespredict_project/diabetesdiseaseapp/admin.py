from django.contrib import admin

from .models import LoginUser,DiabetesRecord

admin.site.register(LoginUser)
admin.site.register(DiabetesRecord)
