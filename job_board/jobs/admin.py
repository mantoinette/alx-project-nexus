from django.contrib import admin
from .models import Job, Application, Category

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'employment_type', 'is_available', 'created_at')
    list_filter = ('is_available', 'employment_type', 'location', 'category')
    search_fields = ('title', 'company_name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__title', 'first_name', 'last_name', 'email')
    date_hierarchy = 'applied_at'
    ordering = ('-applied_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
