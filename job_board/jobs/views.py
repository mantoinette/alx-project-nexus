from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job, Application, Category
from .serializers import JobSerializer, ApplicationSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import status

# Create your views here.

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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


@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'signup.html')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Log the user in after signing up
        login(request, user)

        # Redirect to the login page after signing up
        messages.success(request, "Sign up successful! Please log in.")
        return redirect('user_login')  # Redirect to the login page

    return render(request, 'signup.html')
