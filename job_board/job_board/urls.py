from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from jobs import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Job Board API",
        default_version='v1',
        description="""
        Job Board API documentation with detailed endpoints for:
        * User Authentication
        * Job Listings
        * Job Applications
        * User Management
        * Search Functionality
        """,
        terms_of_service="https://www.jobboard.com/terms/",
        contact=openapi.Contact(email="contact@jobboard.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)