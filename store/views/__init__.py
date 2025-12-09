# views/__init__.py (optional)
from .home import Index, store
from .login import Login, logout
from .signup import Signup
from .cart import Cart
from .checkout import CheckOut
from .orders import OrderView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# This function must be here for Python to find it
def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Superuser created successfully! <br>Username: <b>admin</b><br>Password: <b>admin123</b>")
    else:
        return HttpResponse("Superuser 'admin' already exists.")
__all__ = ['Index','store','Login','logout','Signup','Cart','CheckOut','OrderView']
