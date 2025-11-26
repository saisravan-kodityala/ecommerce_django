# views/__init__.py (optional)
from .home import Index, store
from .login import Login, logout
from .signup import Signup
from .cart import Cart
from .checkout import CheckOut
from .orders import OrderView

__all__ = ['Index','store','Login','logout','Signup','Cart','CheckOut','OrderView']
