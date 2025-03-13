from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import FileExtensionValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    LOCATION_CHOICES = [
        ('Remote', 'Remote - Work from anywhere'),
        ('On-site: New York, NY, USA', 'On-site: New York, NY, USA'),
        ('On-site: San Francisco, CA, USA', 'On-site: San Francisco, CA, USA'),
        ('On-site: Austin, TX, USA', 'On-site: Austin, TX, USA'),
        ('On-site: Chicago, IL, USA', 'On-site: Chicago, IL, USA'),
        ('Hybrid: San Francisco, CA, USA', 'Hybrid: San Francisco, CA, USA'),
        ('Hybrid: New York, NY, USA', 'Hybrid: New York, NY, USA'),
        ('On-site: Kigali, Rwanda', 'On-site: Kigali, Rwanda'),
        ('On-site: Nairobi, Kenya', 'On-site: Nairobi, Kenya'),
        ('On-site: Lagos, Nigeria', 'On-site: Lagos, Nigeria'),
        ('On-site: Accra, Ghana', 'On-site: Accra, Ghana'),
        ('Hybrid: Kigali, Rwanda', 'Hybrid: Kigali, Rwanda'),
        ('Hybrid: Nairobi, Kenya', 'Hybrid: Nairobi, Kenya'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200, default='Unknown Company')  # Set a default value
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='Remote')  # Set a default value
    employment_type = models.CharField(max_length=50, default='Full-time')  # Set a default value
    salary_range = models.CharField(max_length=100, blank=True)  # Optional
    application_deadline = models.DateField(default=datetime.date.today)  # Set a default value
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)  # Indicates if the job is still open for applications

    def __str__(self):
        return self.title

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)  # Made optional
    last_name = models.CharField(max_length=100, null=True, blank=True)   # Made optional
    email = models.EmailField(null=True, blank=True)                      # Made optional
    phone = models.CharField(max_length=20, null=True, blank=True)        # Made optional
    experience = models.CharField(max_length=20, null=True, blank=True)   # Made optional
    current_position = models.CharField(max_length=100, blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    cover_letter = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('reviewing', 'Reviewing'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s application for {self.job.title}"

    class Meta:
        ordering = ['-applied_at']
