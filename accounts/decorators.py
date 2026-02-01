from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "username" not in request.session or "role" not in request.session:
            return redirect(settings.LOGIN_URL)
        return view_func(request, *args, **kwargs)
    return wrapper
