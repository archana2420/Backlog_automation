from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Departments)
admin.site.register(Semesters)
admin.site.register(Subjects)
admin.site.register(subject_code_table)
admin.site.register(final)
