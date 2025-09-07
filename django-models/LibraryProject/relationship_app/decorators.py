from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")
            
            if not hasattr(request.user, 'profile'):
                return HttpResponseForbidden("User profile not found.")
            
            if request.user.profile.role != role_name:
                return HttpResponseForbidden(f"You must be a {role_name} to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Specific role decorators
admin_required = role_required('admin')
librarian_required = role_required('librarian')
member_required = role_required('member')