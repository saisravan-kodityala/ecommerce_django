from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User # Import User model

# ... keep your existing imports and views ...

def create_admin(request):
    # Check if a superuser already exists to prevent duplicate errors
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Superuser created successfully! <br>Username: <b>admin</b><br>Password: <b>admin123</b>")
    else:
        return HttpResponse("Superuser 'admin' already exists.")
