from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from jobs import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('search-jobs/', views.search_jobs, name='search-jobs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)