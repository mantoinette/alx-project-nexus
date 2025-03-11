from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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
    # Fetch all available jobs
    jobs = Job.objects.filter(is_available=True)  # Only fetch jobs that are available
    return render(request, 'user_dashboard.html', {'jobs': jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        # Handle application logic here (e.g., save application details)
        # For example, you could create an Application model to store user applications
        # Application.objects.create(user=request.user, job=job)

        return redirect('user_dashboard')  # Redirect to the dashboard after applying

    return render(request, 'apply_job.html', {'job': job})  # Render an application form if needed

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

@api_view(['POST'])
def user_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return Response(
        UserSerializer(user).data,
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
