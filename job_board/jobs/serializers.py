from rest_framework import serializers
from .models import Job, Application, Category
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    posted_by_username = serializers.CharField(source='posted_by.username', read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('views_count', 'created_at', 'updated_at')

    def get_application_count(self, obj):
        return obj.application_set.count()

class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company_name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('applied_at', 'updated_at')

    def validate(self, data):
        # Check if user has already applied to this job
        user = self.context['request'].user
        job = data.get('job')
        if Application.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        return data
