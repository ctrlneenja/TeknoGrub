from django.contrib import admin
from .models import Role, Users, Staff

# Register your models here.
admin.site.register(Role)
admin.site.register(Users)
admin.site.register(Staff)