from django.contrib import admin
from .models import Job, Category

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'employment_type', 'created_at')
    search_fields = ('title', 'company_name', 'location')

admin.site.register(Job, JobAdmin)
admin.site.register(Category)
