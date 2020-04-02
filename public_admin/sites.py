from functools import update_wrapper

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect


class DummyUser(AnonymousUser):
    def __init__(self, *args, public_apps=(), public_models=(), **kwargs):
        self.public_apps = set(public_apps)
        self.public_models = set(
            f"{public_app}.change_{public_model}"
            for public_app in self.public_apps
            for public_model in self.public_models
        )
        super().__init__(*args, **kwargs)

    def has_module_perms(self, app_label):
        return app_label in self.public_apps

    def has_perm(self, permission, obj=None):
        return permission in self.public_models


class PublicAdminSite(AdminSite):
    def __init__(self, name="public_admin", public_apps=(), public_models=()):
        super().__init__(name=name)
        self._actions, self._global_actions = {}, {}
        self.dummy_user = DummyUser(public_apps=public_apps, public_models=public_models)

    @staticmethod
    def valid_url(url):
        forbidden = (
            "auth",
            "login",
            "logout",
            "password",
            "add",
            "delete",
        )
        return all(label not in url.pattern.regex.pattern for label in forbidden)

    @property
    def urls(self):
        urls = (url for url in self.get_urls() if self.valid_url(url))
        return list(urls), "admin", self.name

    def has_permission(self, request):
        return request.method == "GET"

    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            request.user = self.dummy_user
            if not self.has_permission(request):
                return HttpResponseForbidden()
            return view(request, *args, **kwargs)

        if not getattr(view, "csrf_exempt", False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)
