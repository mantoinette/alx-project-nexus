from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from .models import Job, Application, Category
from .serializers import JobSerializer, ApplicationSerializer, CategorySerializer, UserSerializer

# Create your views here.

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_available=True)
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company_name', 'description', 'location']
    ordering_fields = ['created_at', 'application_deadline', 'salary_min']

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        if Application.objects.filter(user=request.user, job=job).exists():
            return Response(
                {"error": "You have already applied for this job"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, job=job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        job = self.get_object()
        job.views_count += 1
        job.save()
        return Response({'views_count': job.views_count})

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(Q(user=user) | Q(job__posted_by=user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
def job_list(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@login_required
def user_dashboard(request):
    # Get all available jobs
    jobs = Job.objects.filter(is_available=True).order_by('-created_at')
    
    # Get user's applications if authenticated
    applications = []
    if request.user.is_authenticated:
        applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    
    # Get all categories for the search form
    categories = Category.objects.all()

    context = {
        'jobs': jobs,
        'applications': applications,
        'categories': categories,
    }
    
    return render(request, 'jobs/dashboard/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    # Check if user is staff, if not redirect to home
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin dashboard')
        return redirect('home')
    
    # Get statistics for admin
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_available=True).count()
    total_applications = Application.objects.count()
    recent_applications = Application.objects.order_by('-applied_at')[:10]
    categories = Category.objects.all()
    total_users = User.objects.count()
    active_jobs_list = Job.objects.filter(is_available=True).order_by('-created_at')[:10]
    
    context = {
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
        'categories': categories,
        'total_users': total_users,
        'active_jobs_list': active_jobs_list,
    }
    
    return render(request, 'jobs/dashboard/admin_dashboard.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has already applied
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('user_dashboard')
        
    if request.method == 'POST':
        try:
            # Create application with required fields
            application = Application(
                user=request.user,
                job=job
            )
            
            # Add optional fields if provided
            fields = [
                'first_name', 'last_name', 'email', 'phone', 
                'experience', 'current_position', 'expected_salary',
                'cover_letter', 'linkedin_url', 'portfolio_url'
            ]
            
            for field in fields:
                value = request.POST.get(field)
                if value:
                    setattr(application, field, value)
            
            # Handle resume upload
            if 'resume' in request.FILES:
                application.resume = request.FILES['resume']
                
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('user_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
            
    context = {
        'job': job
    }
    return render(request, 'jobs/apply_job.html', context)

@api_view(['GET'])
def search_jobs(request):
    """
    Advanced search endpoint for jobs with multiple filters
    """
    # Get search parameters
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    employment_type = request.GET.get('employment_type', '')
    experience_level = request.GET.get('experience_level', '')
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    posted_within_days = request.GET.get('posted_within_days')

    # Start with all available jobs
    jobs = Job.objects.filter(is_available=True)

    # Apply filters
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(description__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if category:
        jobs = jobs.filter(category__name__icontains=category)

    if employment_type:
        jobs = jobs.filter(employment_type__iexact=employment_type)

    if experience_level:
        jobs = jobs.filter(experience_level__iexact=experience_level)

    if min_salary:
        jobs = jobs.filter(salary_min__gte=float(min_salary))

    if max_salary:
        jobs = jobs.filter(salary_max__lte=float(max_salary))

    if posted_within_days:
        days_ago = timezone.now() - timezone.timedelta(days=int(posted_within_days))
        jobs = jobs.filter(created_at__gte=days_ago)

    # Order by most recent
    jobs = jobs.order_by('-created_at')

    serializer = JobSerializer(jobs, many=True)
    return Response({
        'count': jobs.count(),
        'results': serializer.data
    })

def home(request):
    """
    Home page view - main entry point for all users
    """
    # Get latest jobs (limit to 6)
    latest_jobs = Job.objects.filter(is_available=True).order_by('-created_at')[:6]
    
    # No automatic redirects - show home page with login/signup options
    context = {
        'latest_jobs': latest_jobs,
    }
    
    return render(request, 'jobs/home.html', context)

def user_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'jobs/auth/login.html')

def user_signup(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'jobs/auth/signup.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'jobs/auth/signup.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'jobs/auth/signup.html')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome to Job Board.')
        return redirect('user_dashboard')
        
    return render(request, 'jobs/auth/signup.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
