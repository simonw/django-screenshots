from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.http import HttpRequest


class TestUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        username = request.GET.get("_user")
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                login(request, user)
            except User.DoesNotExist:
                # Create that user
                user = User.objects.create_user(username=username)
                if username == "admin":
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                login(request, user)
        else:
            logout(request)

        return self.get_response(request)
