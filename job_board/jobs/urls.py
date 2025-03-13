from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, ApplicationViewSet, CategoryViewSet, 
    job_list, user_dashboard, admin_dashboard, apply_job, 
    user_login, user_signup, search_jobs, home
)

# API Routes
router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='api-jobs')
router.register(r'applications', ApplicationViewSet, basename='api-applications')
router.register(r'categories', CategoryViewSet, basename='api-categories')

# Frontend Routes
urlpatterns = [
    path('', home, name='home'),  # Landing page
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('jobs/', job_list, name='job-list'),
    path('search/', search_jobs, name='search-jobs'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('login/', user_login, name='user_login'),
    path('signup/', user_signup, name='user_signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
] + router.urls