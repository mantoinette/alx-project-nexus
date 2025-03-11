from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, ApplicationViewSet, CategoryViewSet, 
    job_list, user_dashboard, apply_job, 
    user_login, user_signup, search_jobs
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls + [
    path('jobs/', job_list, name='job-list'),
    path('search/', search_jobs, name='search-jobs'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('login/', user_login, name='user_login'),
    path('signup/', user_signup, name='user_signup'),
]
