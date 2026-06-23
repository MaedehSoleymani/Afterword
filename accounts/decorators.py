# decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def c_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to log in first to access this page.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def author_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_author or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard') # Redirect to their normal dashboard
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Admin access required.')
            return redirect('accounts:login')
    return wrapper