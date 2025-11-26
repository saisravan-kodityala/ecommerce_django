# store/middlewares/auth.py
from django.shortcuts import redirect

def auth_middleware(view_func):
    """
    A simple wrapper that ensures a customer is logged in (session 'customer' exists).
    It's written to accept a view callable (function-based or result of ClassView.as_view()).
    Usage in urls.py: path('cart', auth_middleware(Cart.as_view()), name='cart')
    """
    def wrapper(request, *args, **kwargs):
        # If not logged in, redirect to login page with return_url to come back after login
        if not request.session.get('customer'):
            return redirect(f"/login?return_url={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper
