# decorators.py
from django.contrib.auth.decorators import user_passes_test

def superuser_required(function=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a superuser.
    """
    def test_func(user):
        return user.is_authenticated and user.is_superuser

    return user_passes_test(test_func, login_url=login_url)(function)