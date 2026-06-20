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

def author_required(function=None):
    def check(user):
        return user.is_authenticated and (user.is_author or user.is_superuser)
    return user_passes_test(check, login_url='accounts:login')(function)