from django.middleware.common import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings


class RequireLoginMiddleware(MiddlewareMixin):
    def process_request(self, r):
        if not r.user.is_authenticated and not [True for p in ["signup", "login", "admin"] if p in r.path.replace("/", "")]:
            return redirect(settings.LOGIN_URL)
        return
